---
name: "Python Django Testing"
description: "Django testing patterns with pytest, Factory-Boy, Given/When/Then, and 100% coverage requirement"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - django
  - testing
  - pytest
  - factory-boy
  - coverage
files:
  - examples/fixture-patterns.md: "Fixture organization and patterns"
  - examples/factory-boy-guide.md: "Factory-Boy for Django test data"
  - examples/given-when-then.md: "Given/When/Then test structure"
  - examples/django-test-patterns.md: "Django-specific testing patterns"
---

# Python Django Testing

## When to Use This Skill

Read this when:
- Writing tests for Django applications
- Setting up test fixtures and factories
- Testing Django models, views, and services
- Achieving 100% test coverage
- Organizing test structure

---

## Critical Principles

### 1. 100% Coverage Required (MANDATORY)

**ALWAYS** maintain 100% test coverage for all new code:

```bash
# BAD ❌ - Accepting less than 100% coverage
pytest --cov=. --cov-fail-under=80

# GOOD ✅ - Enforcing 100% coverage
pytest --cov=. --cov-fail-under=100 --cov-report=term-missing
```

### 2. Function-Based Tests Only (MANDATORY)

**NEVER** use test classes. **ALWAYS** use function-based tests:

```python
# BAD ❌ - Test class
class TestUserService:
    def test_create_user(self):
        user = create_user("Alice")
        assert user.name == "Alice"

# GOOD ✅ - Function-based test
def test_create_user__valid_name__succeeds():
    """Test user creation with valid name.

    Given: Valid user name
    When: Creating user
    Then: User is created with correct name
    """
    # given
    name = "Alice"

    # when
    user = create_user(name)

    # then
    assert user.name == name
```

### 3. Test Naming Convention (MANDATORY)

**ALWAYS** use the pattern: `test_<function>__<scenario>__<assertion>`

```python
# Examples
def test_divide__zero_denominator__raises_zero_division_error():
    """Test division by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_create_user__valid_email__saves_to_database():
    """Test user creation saves to database."""
    user = UserFactory(email="alice@example.com")
    assert User.objects.filter(pk=user.pk).exists()


def test_update_task_status__completed_status__sets_completed_at():
    """Test completing task sets completed_at timestamp."""
    task = TaskFactory(status='pending')
    task.complete()
    assert task.completed_at is not None
```

---

## Fixtures - Preferred Patterns

### 1. Fixtures in File (PREFERRED)

**IMPORTANT:** Moving TOWARD "fixtures in file" and AWAY FROM bloated conftest.py

```python
# test_visits.py
import pytest
from datetime import date
from myapp.factories import VisitFactory, UserFactory

@pytest.fixture
def test_visit():
    """Create test visit with standard data."""
    return {
        'visit_id': 'test-123',
        'service_date': date(2022, 1, 1),
        'mode_of_service': 'in_person',
    }


@pytest.fixture
def authenticated_user():
    """Create authenticated user context."""
    return UserFactory(email='test@example.com')


def test_create_visit__valid_data__succeeds(test_visit, authenticated_user):
    """Test visit creation with valid data.

    Given: Valid visit data and authenticated user
    When: Creating visit
    Then: Visit is created successfully
    """
    # given
    visit_data = test_visit

    # when
    result = create_visit(visit_data, authenticated_user)

    # then
    assert result.id == test_visit['visit_id']
    assert result.service_date == test_visit['service_date']
```

### 2. conftest.py - ONLY for Truly Shared Fixtures

**Use conftest.py ONLY for:**
1. pytest_configure and pytest hooks
2. Truly shared fixtures used across ALL tests
3. Global protections (network call blockers)

```python
# conftest.py - ONLY for truly shared patterns
import pytest

@pytest.fixture
def mock_network_calls(mocker):
    """Block all network calls in tests (global protection)."""
    mocker.patch('requests.get')
    mocker.patch('requests.post')
    mocker.patch('urllib3.PoolManager')


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up test database once per session."""
    with django_db_blocker.unblock():
        # Global database setup
        pass


# DO NOT put service-specific fixtures here
# Those belong in the test file itself
```

### 3. Using Fixtures That Aren't Referenced

Use `@pytest.mark.usefixtures` for fixtures with side effects not used directly:

```python
# BAD ❌ - Unused fixture parameters
def test_handle_message(
    test_visit,
    mock_retrieve_patient,
    mock_user_service,
    mock_practitioner_service,
):
    # Only test_visit is actually used!
    assert test_visit['visit_id'] == 'test-123'


# GOOD ✅ - Use @pytest.mark.usefixtures
@pytest.mark.usefixtures(
    'mock_retrieve_patient',
    'mock_user_service',
    'mock_practitioner_service',
)
def test_handle_message(test_visit):
    """Test message handling with mocked dependencies."""
    assert test_visit['visit_id'] == 'test-123'
```

### 4. Avoid autouse=True

**DO NOT** set `autouse=True` on fixtures - makes dependencies unclear.

**Exception:** Global protections like blocking network calls.

```python
# BAD ❌ - Implicit autouse fixture
@pytest.fixture(autouse=True)
def authenticated():
    """All tests run as authenticated (problematic!)."""
    return setup_auth()


# GOOD ✅ - Explicit fixture usage
@pytest.fixture
def authenticated():
    """Authentication fixture (opt-in)."""
    return setup_auth()


@pytest.mark.usefixtures('authenticated')
def test_protected_endpoint__authenticated_user__succeeds():
    """Test protected endpoint with authentication."""
    response = client.get('/protected/')
    assert response.status_code == 200
```

---

## Factory-Boy for Test Data

### Basic Factory Pattern

```python
# myapp/factories.py
import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, SelfAttribute
from myapp import models
from datetime import date

class OrganizationFactory(DjangoModelFactory):
    """Factory for Organization model."""

    class Meta:
        model = models.Organization
        django_get_or_create = ('name',)  # Avoid duplicates

    name = Faker('company')


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = models.User

    name = Faker('name')
    email = Faker('email')
    organization = SubFactory(OrganizationFactory)
    is_active = True
    registration_date = date(2022, 1, 1)  # Deterministic!


class PostFactory(DjangoModelFactory):
    """Factory for Post model."""

    class Meta:
        model = models.Post

    title = Faker('sentence', nb_words=6)
    content = Faker('paragraph', nb_sentences=5)
    author = SubFactory(UserFactory)
    status = 'published'
```

### Using Factories in Tests

```python
# tests/test_user_service.py
import pytest
from myapp.factories import UserFactory, OrganizationFactory

@pytest.mark.django_db
def test_create_user__with_organization__succeeds():
    """Test user creation with organization.

    Given: Organization and user data
    When: Creating user with organization
    Then: User is created and linked to organization
    """
    # given
    org = OrganizationFactory(name='Test Org')

    # when
    user = UserFactory(organization=org, email='test@example.com')

    # then
    assert user.organization == org
    assert user.email == 'test@example.com'


@pytest.mark.django_db
def test_create_users__batch__creates_multiple():
    """Test batch user creation."""
    # given/when
    users = UserFactory.create_batch(10)

    # then
    assert len(users) == 10
    assert all(user.pk for user in users)
```

---

## Given/When/Then Pattern

**Use for all complex tests** to ensure clarity:

```python
@pytest.mark.django_db
def test_complete_task__pending_task__sets_completed_at(mocker):
    """Test completing task sets completed_at timestamp.

    Given: Pending task and mocked time
    When: Completing task
    Then: Task status is completed and completed_at is set
    """
    # given: Pending task
    task = TaskFactory(status='pending', completed_at=None)

    # given: Frozen time
    from freezegun import freeze_time
    frozen_time = '2024-01-15 10:00:00+00:00'

    # when: Complete task
    with freeze_time(frozen_time):
        task.complete()

    # then: Status updated and timestamp set
    task.refresh_from_db()
    assert task.status == 'completed'
    assert task.completed_at is not None
    assert str(task.completed_at) == '2024-01-15 10:00:00+00:00'
```

---

## Test Organization

### Directory Structure

```
myproject/
├── myapp/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Only global fixtures
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_services.py
│   │   │   └── test_utils.py
│   │   └── integration/
│   │       ├── __init__.py
│   │       ├── test_database_operations.py
│   │       └── test_api_endpoints.py
│   ├── factories.py             # Factory-Boy factories
│   ├── models.py
│   ├── services.py
│   └── utils.py
└── pytest.ini
```

### File Organization

- One class/service per file
- Test files mirror source file structure
- Separate `unit/` and `integration/` directories
- Keep `conftest.py` minimal

---

## Parametrize Usage (DISCOURAGED)

**Use parametrize sparingly.** Follow these rules:

### When to Use

✅ **Good use cases:**
- Testing same function with 2-4 simple variations
- Simple data types only
- No control flow in test

❌ **Bad use cases:**
- Complex logic requiring if/else
- Nested dicts or complex structures
- More than 4 test cases

### Rules

1. NO control flow statements (if/else, loops) in test
2. Cases must be extremely similar
3. Simple datatypes only
4. **Always use pytest.param with id**

```python
@pytest.mark.parametrize(
    'input_value, expected_output',
    [
        pytest.param(
            'foo',
            True,
            id='Input matches',
        ),
        pytest.param(
            'bar',
            False,
            id='Input does not match',
        ),
    ],
)
def test_match_input__all_scenarios(input_value, expected_output):
    """Test input matching for all scenarios."""
    # when
    result = match_input_to_foo(input_value)

    # then
    assert result == expected_output
```

---

## Django-Specific Patterns

### Settings Override

```python
from django.test import override_settings

@override_settings(FEATURE_FLAG_ENABLED=True)
def test_feature__when_enabled__works():
    """Test feature behavior when enabled."""
    from django.conf import settings
    assert settings.FEATURE_FLAG_ENABLED is True


@override_settings(
    DEBUG=True,
    ALLOWED_HOSTS=['testserver'],
)
def test_debug_view__debug_enabled__shows_details():
    """Test debug view with DEBUG enabled."""
    response = client.get('/debug/')
    assert 'Debug Info' in response.content.decode()
```

### Testing N+1 Queries

```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

@pytest.mark.django_db
def test_get_visits__batch_query__no_n_plus_one():
    """Test visit fetching has no N+1 queries.

    Given: 10 visits with patients
    When: Fetching visits with select_related
    Then: Only 1-2 queries executed (no N+1)
    """
    # given
    visits = [VisitFactory() for _ in range(10)]

    # when
    with CaptureQueriesContext(connection) as queries:
        result = get_visits_with_patients()
        for visit in result:
            _ = visit.patient.name  # Access patient (should not query)

    # then
    assert len(queries.captured_queries) <= 2
```

---

## Deterministic Test Data (CRITICAL)

**NEVER** use `datetime.now()` or `timezone.now()` in test setup.

### Bad Pattern

```python
# BAD ❌ - Non-deterministic test
RESOURCE = {'date': timezone.now().date()}

def test_process_resource():
    """Test fails at different times of day!"""
    assert process_resource(RESOURCE)
```

### Good Pattern

```python
# GOOD ✅ - Deterministic test
from freezegun import freeze_time
from datetime import date

RESOURCE = {'date': date(2022, 1, 1)}

@freeze_time('2022-01-03 02:30:00+00:00')
def test_process_resource():
    """Test with frozen time."""
    from django.utils import timezone
    now = timezone.now()
    assert now.year == 2022
    assert now.month == 1
    assert now.day == 3

    result = process_resource(RESOURCE)
    assert result is True
```

### Using freezegun

```python
from freezegun import freeze_time
from datetime import datetime
from django.utils import timezone

@freeze_time('2024-01-15 12:00:00+00:00')
@pytest.mark.django_db
def test_visit_creation__frozen_time__uses_fixed_date():
    """Test visit creation with frozen time.

    Given: Time frozen at 2024-01-15 12:00:00 UTC
    When: Creating visit
    Then: Visit created_at uses frozen time
    """
    # given: Frozen time
    expected_time = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

    # when
    visit = VisitFactory()

    # then
    assert visit.created_at == expected_time
```

---

## Test Markers

### Built-in Markers

```python
# Slow tests
@pytest.mark.slow
def test_expensive_operation():
    """Test expensive operation (marked slow)."""
    result = perform_expensive_operation()
    assert result is True


# Django database access
@pytest.mark.django_db
def test_database_operation():
    """Test requiring database access."""
    user = UserFactory()
    assert User.objects.filter(pk=user.pk).exists()


# Django transactions
@pytest.mark.django_db(transaction=True)
def test_transaction_behavior():
    """Test requiring transaction support."""
    with transaction.atomic():
        user = UserFactory()
        # Test transaction behavior
```

### Custom Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

# Usage
@pytest.mark.integration
@pytest.mark.django_db
def test_api_endpoint__full_flow__succeeds():
    """Integration test for API endpoint."""
    response = client.post('/api/users/', {'name': 'Alice'})
    assert response.status_code == 201


# Run only unit tests
# pytest -m unit

# Run only integration tests
# pytest -m integration

# Skip slow tests
# pytest -m "not slow"
```

---

## Coverage Requirements

### Running with Coverage

```bash
# Run tests with coverage
pytest --cov=myapp --cov-report=term-missing

# Fail if coverage below 100%
pytest --cov=myapp --cov-fail-under=100

# HTML coverage report
pytest --cov=myapp --cov-report=html

# Open HTML report
open htmlcov/index.html
```

### Coverage Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--cov=myapp",
    "--cov-report=term-missing",
    "--cov-fail-under=100",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["myapp"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

---

## Integration with Other Skills

### From python-testing-excellence

- Docker/docker-compose for real databases (FIRST priority)
- Real code over mocks philosophy
- pytest patterns and fixtures
- Property-based testing with Hypothesis

### From python-django-models

- Test base model classes (UUID, timestamps, soft delete)
- Test query optimization (select_related, prefetch_related)
- Test N+1 query prevention
- Factory-Boy for model instances

### From python-django-configuration

- Test feature flags with @override_settings
- Test multi-tenancy with BRAND settings
- Test configuration validation
- Test environment-specific behavior

---

## Common Pitfalls

### Pitfall 1: Test Classes

```python
# BAD ❌ - Test class
class TestUserService:
    def test_create_user(self):
        pass

# GOOD ✅ - Function-based test
def test_create_user__valid_name__succeeds():
    pass
```

### Pitfall 2: Poor Test Names

```python
# BAD ❌ - Unclear test name
def test_user():
    pass

def test_create():
    pass

# GOOD ✅ - Clear test name
def test_create_user__valid_email__saves_to_database():
    pass
```

### Pitfall 3: Non-Deterministic Tests

```python
# BAD ❌ - Non-deterministic
def test_recent_posts():
    cutoff = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=cutoff)
    assert len(posts) == 5  # Fails at different times!

# GOOD ✅ - Deterministic with freezegun
@freeze_time('2024-01-15 12:00:00+00:00')
def test_recent_posts__last_7_days__returns_5_posts():
    # Create posts at known times
    old_post = PostFactory(created_at=datetime(2024, 1, 1))
    recent_posts = PostFactory.create_batch(
        5,
        created_at=datetime(2024, 1, 10)
    )

    cutoff = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=cutoff)
    assert len(posts) == 5
```

### Pitfall 4: Bloated conftest.py

```python
# BAD ❌ - Service-specific fixtures in conftest
@pytest.fixture
def test_visit():
    return {'visit_id': 'test-123'}

@pytest.fixture
def test_user():
    return UserFactory()

# GOOD ✅ - Move to test file
# test_visits.py
@pytest.fixture
def test_visit():
    return {'visit_id': 'test-123'}
```

### Pitfall 5: Not Testing N+1 Queries

```python
# BAD ❌ - No query count test
@pytest.mark.django_db
def test_get_posts_with_authors():
    posts = get_posts_with_authors()
    assert len(posts) == 10  # Hidden N+1 problem!

# GOOD ✅ - Test query count
@pytest.mark.django_db
def test_get_posts_with_authors__no_n_plus_one():
    PostFactory.create_batch(10)

    with CaptureQueriesContext(connection) as queries:
        posts = get_posts_with_authors()
        for post in posts:
            _ = post.author.name

    assert len(queries.captured_queries) <= 2
```

---

## Best Practices

1. **100% coverage** - No exceptions
2. **Function-based tests** - Never use test classes
3. **Clear test names** - Use test_<function>__<scenario>__<assertion>
4. **Fixtures in file** - Keep conftest.py minimal
5. **Given/When/Then** - Use for all complex tests
6. **Factory-Boy** - Generate Django model instances
7. **Deterministic data** - Use freezegun, avoid timezone.now()
8. **Test N+1 queries** - Use CaptureQueriesContext
9. **Parametrize sparingly** - Only for simple, similar cases
10. **@override_settings** - Test configuration variations

---

## Learning Log

### 2026-02-02: Python Django Testing Skill Created

**Issue:** Need comprehensive Django testing patterns.

**Learning:** Created Django testing skill covering:
- 100% coverage requirement (mandatory)
- Function-based tests only (never classes)
- Test naming convention (test_<function>__<scenario>__<assertion>)
- Fixtures in file pattern (away from bloated conftest.py)
- Factory-Boy for Django model test data
- Given/When/Then pattern for complex tests
- Deterministic test data with freezegun
- Django-specific patterns (settings override, N+1 queries)
- Parametrize rules (discouraged, use sparingly)
- Test organization (unit/ and integration/ directories)

**Adaptation:** Integrated with existing Python skills:
- Docker testing from python-testing-excellence
- Model testing from python-django-models
- Configuration testing from python-django-configuration
- Real code over mocks philosophy throughout

**New Standard:** All Django tests must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `fixture-patterns.md` - Fixture organization and conftest.py usage
- `factory-boy-guide.md` - Factory-Boy patterns for Django models
- `given-when-then.md` - Given/When/Then test structure
- `django-test-patterns.md` - Django-specific testing patterns

## Related Skills

- [Python Testing Excellence](../../testing/skill.md) - For pytest fundamentals
- [Python Django Models](../python-django-models/skill.md) - For model testing patterns
- [Python Django Configuration](../python-django-configuration/skill.md) - For configuration testing

---

*Created: 2026-02-02*
*Version: 1.0*
