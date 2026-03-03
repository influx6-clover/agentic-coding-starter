# Docker and Docker-Compose for Testing

This document covers using Docker and docker-compose to run real infrastructure (databases, services) in tests.

## Philosophy

**Test against real databases and services, not mocks.**

The Infrastructure Testing Hierarchy:
1. **Best:** Real service in Docker container (testcontainers or docker-compose)
2. **Good:** Test instance provided by dev team
3. **Acceptable:** In-memory substitute (SQLite for SQL databases)
4. **Last Resort:** Mock (only for proprietary SaaS without local option)

## When to Use Docker for Tests

**✅ USE Docker when:**
- PostgreSQL, MySQL, MongoDB (databases)
- Redis, Memcached (caches)
- RabbitMQ, Kafka (message queues)
- Elasticsearch, S3-compatible storage (MinIO)
- Any service with official Docker image

**❌ DON'T USE Docker when:**
- Service is proprietary SaaS without local version (Snowflake, Salesforce)
- Service requires special hardware/licenses
- **ACTION:** Ask dev team for test instance credentials first!

## Docker-Compose for Test Infrastructure

### Example: PostgreSQL + Redis

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### Running Tests with Docker-Compose

```bash
# Start infrastructure
docker-compose -f docker-compose.test.yml up -d

# Wait for health checks
docker-compose -f docker-compose.test.yml ps

# Run tests
cargo test

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

### Automated Test Script

```bash
#!/bin/bash
# scripts/run-tests.sh

set -e

echo "Starting test infrastructure..."
docker-compose -f docker-compose.test.yml up -d

echo "Waiting for services to be healthy..."
timeout 30 bash -c 'until docker-compose -f docker-compose.test.yml ps | grep -q "(healthy)"; do sleep 1; done'

echo "Running tests..."
cargo test "$@"

echo "Cleaning up..."
docker-compose -f docker-compose.test.yml down -v
```

Make it executable:
```bash
chmod +x scripts/run-tests.sh
./scripts/run-tests.sh
```

## GitHub Actions CI Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Run tests
        run: cargo test
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
```

## Decision Tree for Database Testing

```
Need to test database code?
├─ Can database run in Docker? (PostgreSQL, MySQL, MongoDB, etc.)
│  ├─ YES → Use docker-compose or testcontainers-rs ✅ BEST
│  └─ NO → Continue to next step
├─ Is there a test instance available? (Snowflake test account, etc.)
│  ├─ YES → Ask dev team for credentials, use test instance ✅ GOOD
│  └─ NO → Continue to next step
├─ Can we use SQLite as substitute? (For SQL databases only)
│  ├─ YES → Use SQLite :memory: for fast tests ✅ ACCEPTABLE
│  └─ NO → Continue to next step
└─ Must mock (proprietary SaaS, no local/test options)
   └─ Use trait mock for external database client only ⚠️ LAST RESORT
```

## Benefits of Docker-Based Testing

1. **Real behavior** - Tests validate actual database/service behavior
2. **Production parity** - Same services as production
3. **Isolation** - Each test run gets fresh infrastructure
4. **CI/CD friendly** - Easy to replicate in GitHub Actions/GitLab CI
5. **No mocks** - Test actual integration, not mock configuration

## When Mocking is Acceptable

**ONLY mock when:**
- ✅ Service is proprietary SaaS without Docker image (Snowflake, Salesforce API)
- ✅ Service requires hardware/licensing unavailable in test (special GPU, enterprise license)
- ✅ Service costs money per request (payment gateways in CI - but use test mode if available)

**Before mocking, ask:**
1. "Can I run this in Docker?"
2. "Does the dev team have test instance credentials?"
3. "Is there a free tier or test mode?"
4. "Can I use a compatible open-source alternative?" (MinIO for S3, LocalStack for AWS)

## Using Testcontainers Instead

For programmatic container management, see [`testcontainers-examples.md`](testcontainers-examples.md).

Testcontainers is better when:
- Need different container configurations per test
- Want automatic cleanup
- Prefer Rust code over YAML configuration
