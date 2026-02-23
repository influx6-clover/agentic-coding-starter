# Testing Django Models with Real Databases (Docker)

This guide covers testing Django models against real databases using Docker and testcontainers.

---

## Critical Principle

**NEVER** mock the Django ORM. **ALWAYS** test against real databases.

```python
# ❌ WRONG - Mocking Django ORM
@patch('myapp.models.User.objects.get')
def test_user_fetch(mock_get):
    mock_get.return_value = Mock(name="Alice")
    # This tests NOTHING about actual database behavior!

# ✅ CORRECT - Real database
@pytest.mark.django_db
def test_user_fetch():
    user = UserFactory(name="Alice")
    fetched = User.objects.get(pk=user.pk)
    assert fetched.name == "Alice"
    # Tests actual database operations!
```

---

## Testing Hierarchy

Follow this hierarchy (from best to worst):

1. **Docker/docker-compose** (FIRST) - Real database in container
2. **Test instance credentials** (SECOND) - Managed test environment
3. **pytest-django** (THIRD) - Django's test database
4. **Mock** (LAST RESORT) - External APIs only, NEVER Django ORM

---

## Setup 1: Docker Compose (Recommended)

### docker-compose.test.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - "5433:5432"  # Use different port to avoid conflicts
    tmpfs:
      - /var/lib/postgresql/data  # In-memory for speed

  mysql:
    image: mysql:8
    environment:
      MYSQL_DATABASE: test_db
      MYSQL_USER: test_user
      MYSQL_PASSWORD: test_password
      MYSQL_ROOT_PASSWORD: root_password
    ports:
      - "3307:3306"
    tmpfs:
      - /var/lib/mysql  # In-memory for speed
```

### Running Tests

```bash
# Start test databases
docker-compose -f docker-compose.test.yml up -d

# Run tests
pytest

# Stop test databases
docker-compose -f docker-compose.test.yml down
```

### pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "myproject.settings.test"
addopts = [
    "-v",
    "--reuse-db",           # Reuse test database
    "--create-db",          # Create if doesn't exist
]
```

### Test Settings

```python
# myproject/settings/test.py
from .base import *

# Use Docker PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '5433',
        'TEST': {
            'NAME': 'test_db',  # Use same database for speed
        },
    }
}

# Speed optimizations for tests
DEBUG = False
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # Fast but insecure (test only!)
]
```

---

## Setup 2: Testcontainers (Python API)

Programmatically manage Docker containers from tests.

### Installation

```bash
pip install pytest-django testcontainers[postgres]
# or
poetry add --group dev pytest-django testcontainers[postgres]
```

### conftest.py

```python
# conftest.py
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for entire test session."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def django_db_setup(postgres_container):
    """Configure Django to use containerized PostgreSQL."""
    from django.conf import settings

    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': postgres_container.POSTGRES_DB,
        'USER': postgres_container.POSTGRES_USER,
        'PASSWORD': postgres_container.POSTGRES_PASSWORD,
        'HOST': postgres_container.get_container_host_ip(),
        'PORT': postgres_container.get_exposed_port(5432),
    }


@pytest.fixture
def db_with_data(db):
    """Fixture that provides database with test data."""
    # Database is already created by django_db_setup
    # Additional setup can go here
    yield
```

### Using in Tests

```python
# tests/test_models.py
import pytest
from tests.factories import UserFactory

@pytest.mark.django_db
def test_user_creation():
    """Test user creation in real PostgreSQL.

    Given: Valid user data
    When: Creating user in real database
    Then: User is persisted correctly
    """
    # given/when: Create user
    user = UserFactory(name="Alice", email="alice@example.com")

    # then: User persisted in real database
    from myapp.models import User
    fetched = User.objects.get(pk=user.pk)
    assert fetched.name == "Alice"
    assert fetched.email == "alice@example.com"
```

---

## Setup 3: Factory-Boy for Test Data

Use Factory-Boy to generate realistic test data.

### Installation

```bash
pip install factory-boy faker
# or
poetry add --group dev factory-boy faker
```

### Factory Definitions

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from myapp.models import User, Post, UserRole
from django.utils import timezone

class UserFactory(DjangoModelFactory):
    """Factory for User model.

    Usage:
        # Simple creation
        user = UserFactory()

        # Override fields
        user = UserFactory(name="Alice", email="alice@example.com")

        # Create batch
        users = UserFactory.create_batch(10)

        # Build without saving
        user = UserFactory.build()
    """

    class Meta:
        model = User
        django_get_or_create = ('email',)  # Avoid duplicate emails

    # Basic fields
    name = factory.Faker('name')
    email = factory.Faker('email')
    role = FuzzyChoice([UserRole.USER, UserRole.MODERATOR])

    # Timestamps (if not using TimestampedModelBase)
    # created_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def with_profile(self, create, extracted, **kwargs):
        """Add profile if requested.

        Usage:
            user = UserFactory(with_profile=True)
            user = UserFactory(with_profile=True, bio="Custom bio")
        """
        if not create:
            return

        if extracted:
            ProfileFactory(user=self, **kwargs)


class PostFactory(DjangoModelFactory):
    """Factory for Post model."""

    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=6)
    content = factory.Faker('paragraph', nb_sentences=5)
    author = factory.SubFactory(UserFactory)  # Auto-create author

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags if provided.

        Usage:
            post = PostFactory(tags=['python', 'django'])
        """
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class ProfileFactory(DjangoModelFactory):
    """Factory for Profile model."""

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('paragraph', nb_sentences=3)
    website = factory.Faker('url')
```

---

## Testing Patterns

### Pattern 1: Basic Model Test

```python
import pytest
from tests.factories import UserFactory
from myapp.models import User

@pytest.mark.django_db
def test_user_creation__with_valid_data__persists():
    """Test user creation with valid data.

    Given: Valid user data
    When: User is created
    Then: User is persisted with correct attributes
    """
    # given: User data
    name = "Alice Smith"
    email = "alice@example.com"

    # when: Create user
    user = UserFactory(name=name, email=email)

    # then: User persisted correctly
    assert User.objects.filter(pk=user.pk).exists()
    fetched = User.objects.get(pk=user.pk)
    assert fetched.name == name
    assert fetched.email == email
    assert fetched.created_at is not None
```

### Pattern 2: Query Optimization Test

```python
import pytest
from django.test.utils import CaptureQueriesContext
from django.db import connection
from tests.factories import UserFactory, PostFactory

@pytest.mark.django_db
def test_post_list__with_select_related__no_n_plus_1():
    """Test query optimization prevents N+1 problem.

    Given: Multiple posts with authors
    When: Fetching posts with select_related
    Then: Only 1 query is executed (no N+1)
    """
    # given: 10 posts with different authors
    users = UserFactory.create_batch(10)
    posts = [PostFactory(author=user) for user in users]

    # when: Fetch with select_related
    with CaptureQueriesContext(connection) as context:
        fetched_posts = list(
            Post.objects.select_related('author').all()
        )
        # Access authors (should not cause queries)
        for post in fetched_posts:
            _ = post.author.name

    # then: Only 1 query executed
    assert len(context.captured_queries) == 1
    assert 'JOIN' in context.captured_queries[0]['sql'].upper()
```

### Pattern 3: Soft Delete Test

```python
import pytest
from tests.factories import UserFactory
from myapp.models import User

@pytest.mark.django_db
def test_soft_delete__user__marks_deleted_not_removed():
    """Test soft delete marks user as deleted but keeps in database.

    Given: Active user in database
    When: Soft delete is called
    Then: User is marked deleted but not removed from database
    """
    # given: Active user
    user = UserFactory()
    assert not user.is_deleted()
    user_pk = user.pk

    # when: Soft delete
    user.soft_delete()

    # then: Marked deleted but still exists
    user.refresh_from_db()
    assert user.is_deleted()
    assert user.deleted_at is not None
    assert User.objects.filter(pk=user_pk).exists()

    # Filter active users excludes deleted
    active_users = User.objects.filter(deleted_at__isnull=True)
    assert user not in active_users
```

### Pattern 4: Deterministic Time Test

```python
import pytest
from freezegun import freeze_time
from datetime import timedelta
from django.utils import timezone
from tests.factories import PostFactory
from myapp.models import Post

@pytest.mark.django_db
@freeze_time("2024-01-15 12:00:00")
def test_recent_posts__filters_by_date():
    """Test recent posts filtering with frozen time.

    Given: Posts created at different times
    When: Filtering for posts from last 7 days
    Then: Only recent posts are returned
    """
    # given: Old post
    with freeze_time("2024-01-01"):
        old_post = PostFactory(title="Old Post")

    # given: Recent post (at frozen time)
    recent_post = PostFactory(title="Recent Post")

    # when: Get posts from last 7 days
    cutoff = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=cutoff)

    # then: Only recent post returned
    assert list(recent_posts) == [recent_post]
    assert old_post not in recent_posts
```

### Pattern 5: Transaction Test

```python
import pytest
from django.db import transaction
from tests.factories import UserFactory
from myapp.models import User

@pytest.mark.django_db
def test_atomic_transaction__with_error__rolls_back():
    """Test atomic transaction rolls back on error.

    Given: Multiple operations in atomic transaction
    When: Error occurs mid-transaction
    Then: All operations are rolled back
    """
    # given: Initial user count
    initial_count = User.objects.count()

    # when: Transaction with error
    with pytest.raises(ValueError):
        with transaction.atomic():
            UserFactory(name="Alice")
            UserFactory(name="Bob")
            raise ValueError("Simulated error")

    # then: No users were created (rollback)
    assert User.objects.count() == initial_count
```

### Pattern 6: Bulk Operations Test

```python
import pytest
from tests.factories import UserFactory
from myapp.models import User

@pytest.mark.django_db
def test_bulk_create__many_users__single_query():
    """Test bulk create uses single query.

    Given: Many users to create
    When: Using bulk_create
    Then: Single query is executed
    """
    # given: 100 users to create
    users_data = [
        User(name=f"User {i}", email=f"user{i}@example.com")
        for i in range(100)
    ]

    # when: Bulk create
    from django.test.utils import CaptureQueriesContext
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        User.objects.bulk_create(users_data)

    # then: Only 1 query executed
    assert len(context.captured_queries) == 1

    # Verify all created
    assert User.objects.count() == 100
```

### Pattern 7: Custom Manager Test

```python
import pytest
from tests.factories import UserFactory
from myapp.models import User

@pytest.mark.django_db
def test_active_manager__filters_deleted_users():
    """Test custom active manager excludes deleted users.

    Given: Mix of active and deleted users
    When: Using active manager
    Then: Only active users are returned
    """
    # given: Active and deleted users
    active1 = UserFactory()
    active2 = UserFactory()
    deleted = UserFactory()
    deleted.soft_delete()

    # when: Query with active manager
    active_users = User.active.all()

    # then: Only active users returned
    assert list(active_users) == [active1, active2]
    assert deleted not in active_users

    # Verify default manager includes all
    all_users = User.objects.all()
    assert deleted in all_users
```

---

## Multiple Database Testing

### Test Settings with Multiple Databases

```python
# settings/test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_primary',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '5433',
    },
    'analytics': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_analytics',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '5433',
    },
}
```

### Testing with Multiple Databases

```python
import pytest
from tests.factories import UserFactory, AnalyticsEventFactory

@pytest.mark.django_db(databases=['default', 'analytics'])
def test_cross_database__user_and_analytics__both_persist():
    """Test data persists to correct databases.

    Given: Models using different databases
    When: Creating records
    Then: Each persists to correct database
    """
    # given/when: Create user in default database
    user = UserFactory()

    # given/when: Create analytics event in analytics database
    event = AnalyticsEventFactory(user_id=user.id)

    # then: Both exist in their respective databases
    from myapp.models import User
    from analytics.models import AnalyticsEvent

    assert User.objects.using('default').filter(pk=user.pk).exists()
    assert AnalyticsEvent.objects.using('analytics').filter(pk=event.pk).exists()
```

---

## Performance Testing

### Test Query Performance

```python
import pytest
import time
from tests.factories import PostFactory, UserFactory

@pytest.mark.django_db
@pytest.mark.slow
def test_bulk_operations__performance__faster_than_individual():
    """Test bulk operations are faster than individual saves.

    Given: Many records to create
    When: Comparing bulk vs individual creates
    Then: Bulk is significantly faster
    """
    # Test individual creates
    start = time.time()
    for i in range(100):
        UserFactory()
    individual_time = time.time() - start

    # Clean up
    User.objects.all().delete()

    # Test bulk create
    users = [
        User(name=f"User {i}", email=f"user{i}@example.com")
        for i in range(100)
    ]
    start = time.time()
    User.objects.bulk_create(users)
    bulk_time = time.time() - start

    # Bulk should be at least 5x faster
    assert bulk_time * 5 < individual_time
```

---

## Best Practices

1. **Always use real databases** - Never mock Django ORM
2. **Use Docker** - Consistent environment across machines
3. **Use Factory-Boy** - Generate realistic test data
4. **Test query counts** - Catch N+1 problems early
5. **Freeze time** - Deterministic datetime testing
6. **Given/When/Then** - Clear test structure
7. **Mark slow tests** - Use `@pytest.mark.slow` for performance tests
8. **Cleanup fixtures** - Use `db` fixture for automatic cleanup
9. **Session-scoped containers** - Reuse containers across tests for speed
10. **Test transactions** - Ensure atomic behavior

---

## Common Pitfalls

### Pitfall 1: Mocking Django ORM

```python
# ❌ WRONG
@patch('myapp.models.User.objects.get')
def test_user(mock_get):
    pass  # Tests nothing!

# ✅ CORRECT
@pytest.mark.django_db
def test_user():
    user = UserFactory()
    # Test real database
```

### Pitfall 2: Not Testing Query Counts

```python
# ❌ MISSING - No N+1 detection
@pytest.mark.django_db
def test_posts():
    posts = Post.objects.all()
    for post in posts:
        print(post.author.name)  # Hidden N+1!

# ✅ CORRECT - Catch N+1 problems
@pytest.mark.django_db
def test_posts():
    with CaptureQueriesContext(connection) as context:
        posts = Post.objects.select_related('author').all()
        for post in posts:
            print(post.author.name)
    assert len(context.captured_queries) == 1
```

### Pitfall 3: Inconsistent Test Data

```python
# ❌ WRONG - Hard to maintain
@pytest.mark.django_db
def test_user():
    user = User.objects.create(
        name="Alice",
        email="alice@example.com",
        # ... many fields
    )

# ✅ CORRECT - Factory-Boy
@pytest.mark.django_db
def test_user():
    user = UserFactory()  # All fields set correctly
```

### Pitfall 4: Missing @pytest.mark.django_db

```python
# ❌ WRONG - Test will fail
def test_user():
    user = UserFactory()  # Error: no database!

# ✅ CORRECT
@pytest.mark.django_db
def test_user():
    user = UserFactory()  # Works!
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: poetry run pytest
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5433/test_db
```

---

*Related: See `skill.md` for complete Django models guide*
