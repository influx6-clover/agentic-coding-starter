# Monorepo Development Workflows

Development workflows for working in Python monorepo.

---

## Working Across Services

```bash
# 1. Update ca-lib
cd ca-lib
# Make changes
make protoc
make test

# 2. Update dependent service
cd ../ca-user-service
uv sync  # Gets updated ca-lib
make test

# 3. Commit both
git add ca-lib ca-user-service
git commit -m "feat: update ca-lib and services"
```

## Installing Dependencies

```bash
# From workspace root
uv sync                    # All services
uv sync --package ca-user-service  # Specific service

# From service directory
cd ca-user-service
uv add django             # Add dependency
uv add --dev pytest       # Add dev dependency
```

---

*Related: See skill.md for complete workflows*
