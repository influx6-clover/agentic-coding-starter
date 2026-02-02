# Fixture Patterns - Organization and Usage

This guide covers fixture organization, conftest.py usage, and fixture best practices.

---

## The Fixture Philosophy

**KEY PRINCIPLE:** Moving TOWARD "fixtures in file" and AWAY FROM bloated conftest.py

### Why Fixtures in File?

**Benefits:**
- **Co-location**: Test setup next to tests that use it
- **Clarity**: Easy to see what fixtures a test file uses
- **Maintainability**: Changes don't affect unrelated tests
- **Discoverability**: No hunting through conftest.py files

**Problems with bloated conftest.py:**
- Unclear dependencies
- Difficult to understand what fixtures exist
- Changes can break unrelated tests
- Hard to maintain as project grows

---

## Pattern 1: Fixtures in Test File (PREFERRED)

### Basic Fixture in File

```python
# tests/test_visits.py
import pytest
from datetime import date
from myapp.factories import VisitFactory, PatientFactory

@pytest.fixture
def test_visit_data():
    """Standard test visit data."""
    return {
        'visit_id': 'test-123',
        'service_date': date(2022, 1, 1),
        'mode_of_service': 'in_person',
        'diagnosis_codes': ['Z00.00'],
    }


@pytest.fixture
def test_patient():
    """Create test patient."""
    return PatientFactory(
        name='Test Patient',
        date_of_birth=date(1980, 1, 1),
    )


def test_create_visit__valid_data__succeeds(test_visit_data, test_patient):
    """Test visit creation with valid data.

    Given: Valid visit data and patient
    When: Creating visit
    Then: Visit is created successfully
    """
    # given
    visit_data = test_visit_data
    patient = test_patient

    # when
    visit = create_visit(visit_data, patient)

    # then
    assert visit.visit_id == test_visit_data['visit_id']
    assert visit.patient == patient
```

### Fixture with Parameters

```python
# tests/test_users.py
import pytest
from myapp.factories import UserFactory

@pytest.fixture
def admin_user():
    """Create admin user."""
    return UserFactory(role='admin', is_active=True)


@pytest.fixture
def regular_user():
    """Create regular user."""
    return UserFactory(role='user', is_active=True)


@pytest.fixture
def inactive_user():
    """Create inactive user."""
    return UserFactory(role='user', is_active=False)


def test_admin_access__admin_user__allowed(admin_user):
    """Test admin can access admin panel."""
    assert can_access_admin_panel(admin_user) is True


def test_admin_access__regular_user__denied(regular_user):
    """Test regular user cannot access admin panel."""
    assert can_access_admin_panel(regular_user) is False
```

### Fixture Composition

```python
# tests/test_orders.py
import pytest
from myapp.factories import UserFactory, ProductFactory, OrderFactory

@pytest.fixture
def user_with_address():
    """Create user with address."""
    user = UserFactory()
    user.addresses.create(
        street='123 Main St',
        city='New York',
        zip_code='10001',
    )
    return user


@pytest.fixture
def product_in_stock():
    """Create product with stock."""
    return ProductFactory(stock_quantity=100)


@pytest.fixture
def complete_order(user_with_address, product_in_stock):
    """Create complete order with user and product."""
    return OrderFactory(
        user=user_with_address,
        product=product_in_stock,
        quantity=1,
    )


def test_place_order__complete_data__succeeds(complete_order):
    """Test order placement with all required data."""
    order = complete_order
    assert order.user is not None
    assert order.product is not None
    assert order.product.stock_quantity >= order.quantity
```

---

## Pattern 2: conftest.py - ONLY for Shared Fixtures

### When to Use conftest.py

✅ **Use conftest.py ONLY for:**

1. **pytest_configure** and pytest hooks
2. **Truly shared fixtures** used across ALL test files
3. **Global protections** (network blockers, etc.)

```python
# conftest.py
import pytest
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Configure test database for entire session."""
    with django_db_blocker.unblock():
        # Run migrations
        # Load initial data if needed
        pass


@pytest.fixture
def mock_external_api(mocker):
    """Mock all external API calls (global protection)."""
    mocker.patch('requests.get')
    mocker.patch('requests.post')
    mocker.patch('requests.put')
    mocker.patch('requests.delete')


@pytest.fixture
def authenticated_client(client, django_user_model):
    """Create authenticated client (used across many tests)."""
    user = django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
    )
    client.force_login(user)
    return client


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
```

### What NOT to Put in conftest.py

❌ **Do NOT put in conftest.py:**

- Service-specific fixtures
- Test-file-specific fixtures
- Fixtures used by only a few tests
- Complex domain-specific fixtures

```python
# BAD ❌ - Don't put in conftest.py
@pytest.fixture
def test_visit():
    """Specific to visit tests - belongs in test_visits.py"""
    return VisitFactory()


@pytest.fixture
def mock_patient_service():
    """Specific to patient service - belongs in test_patient_service.py"""
    return Mock()


# GOOD ✅ - These belong in conftest.py
@pytest.fixture
def db(django_db_setup, django_db_blocker):
    """Database fixture used by ALL tests."""
    with django_db_blocker.unblock():
        yield


@pytest.fixture
def settings(settings):
    """Settings fixture used by ALL tests."""
    return settings
```

---

## Pattern 3: Using Fixtures Without Referencing

### Problem: Unused Fixture Parameters

```python
# BAD ❌ - Fixtures listed but not used
def test_handle_message(
    test_visit,
    mock_retrieve_patient,
    mock_user_service,
    mock_practitioner_service,
    mock_billing_service,
):
    # Only test_visit is actually used in test body!
    assert test_visit['visit_id'] == 'test-123'
    result = handle_message(test_visit)
    assert result is True
```

### Solution: @pytest.mark.usefixtures

```python
# GOOD ✅ - Use @pytest.mark.usefixtures
@pytest.mark.usefixtures(
    'mock_retrieve_patient',
    'mock_user_service',
    'mock_practitioner_service',
    'mock_billing_service',
)
def test_handle_message(test_visit):
    """Test message handling with mocked dependencies.

    Given: Mocked external dependencies (via fixtures)
    When: Handling message
    Then: Message is processed successfully
    """
    # given
    visit_data = test_visit

    # when
    result = handle_message(visit_data)

    # then
    assert result is True
```

### When to Use @pytest.mark.usefixtures

Use when fixture:
- Has side effects (mocking, setup)
- Is not directly accessed in test
- Must run before test executes

```python
# tests/test_api.py
import pytest

@pytest.fixture
def mock_cache(mocker):
    """Mock cache for all tests."""
    return mocker.patch('django.core.cache.cache')


@pytest.fixture
def mock_celery(mocker):
    """Mock Celery tasks."""
    return mocker.patch('myapp.tasks.send_email.delay')


@pytest.mark.usefixtures('mock_cache', 'mock_celery')
@pytest.mark.django_db
def test_create_user__caching_disabled__creates_successfully():
    """Test user creation with cache and tasks mocked."""
    # Cache and Celery are mocked but not directly accessed
    user = UserFactory(email='test@example.com')
    assert User.objects.filter(pk=user.pk).exists()
```

---

## Pattern 4: Avoid autouse=True

### Problem with autouse

```python
# BAD ❌ - autouse makes dependencies unclear
@pytest.fixture(autouse=True)
def authenticated():
    """Automatically authenticate all tests."""
    setup_authentication()
    yield
    teardown_authentication()


def test_public_endpoint():
    """This test shouldn't need authentication!"""
    response = client.get('/public/')
    assert response.status_code == 200


def test_unauthenticated_access():
    """Can't test unauthenticated access - fixture runs automatically!"""
    response = client.get('/protected/')
    # Want 401, but fixture authenticated us!
    assert response.status_code == 401  # FAILS
```

### Solution: Explicit Fixture Usage

```python
# GOOD ✅ - Explicit fixture usage
@pytest.fixture
def authenticated():
    """Authentication fixture (opt-in)."""
    setup_authentication()
    yield
    teardown_authentication()


def test_public_endpoint():
    """Test public endpoint (no auth needed)."""
    response = client.get('/public/')
    assert response.status_code == 200


@pytest.mark.usefixtures('authenticated')
def test_protected_endpoint__authenticated__succeeds():
    """Test protected endpoint with authentication."""
    response = client.get('/protected/')
    assert response.status_code == 200


def test_protected_endpoint__unauthenticated__forbidden():
    """Test protected endpoint without authentication."""
    response = client.get('/protected/')
    assert response.status_code == 401
```

### Exception: Global Protections

```python
# ACCEPTABLE ✅ - autouse for global protection
@pytest.fixture(autouse=True)
def block_network_calls(mocker):
    """Block all network calls in tests (safety measure)."""
    mocker.patch('requests.get', side_effect=RuntimeError('Network calls blocked'))
    mocker.patch('requests.post', side_effect=RuntimeError('Network calls blocked'))
    # This protects ALL tests from accidental network calls
```

---

## Pattern 5: Fixture Scopes

### Function Scope (Default)

```python
@pytest.fixture  # scope='function' is default
def user():
    """Create new user for each test."""
    return UserFactory()


def test_user_creation(user):
    """Each test gets a fresh user."""
    assert user.pk is not None


def test_user_update(user):
    """This user is different from previous test."""
    user.name = 'Updated'
    user.save()
    assert user.name == 'Updated'
```

### Module Scope

```python
@pytest.fixture(scope='module')
def organization():
    """Create organization once per module."""
    return OrganizationFactory(name='Test Org')


def test_org_users(organization):
    """Uses same organization as other tests in module."""
    user = UserFactory(organization=organization)
    assert user.organization == organization


def test_org_name(organization):
    """Same organization instance."""
    assert organization.name == 'Test Org'
```

### Session Scope

```python
@pytest.fixture(scope='session')
def test_database_setup(django_db_setup):
    """Set up test database once for entire session."""
    # Create test data used by all tests
    # Only runs once
    pass
```

### Scope Best Practices

- **Function scope**: Most fixtures (default, safest)
- **Module scope**: Expensive setup shared within file
- **Session scope**: Database setup, global configuration
- **Be careful**: Higher scopes can cause test interdependence

---

## Pattern 6: Fixture Factories

### Fixture That Returns Factory Function

```python
@pytest.fixture
def make_user():
    """Factory function to create users with custom attributes."""
    def _make_user(**kwargs):
        defaults = {
            'email': 'test@example.com',
            'is_active': True,
        }
        defaults.update(kwargs)
        return UserFactory(**defaults)
    return _make_user


def test_multiple_users(make_user):
    """Create multiple users with different attributes."""
    # given
    admin = make_user(role='admin')
    user1 = make_user(email='user1@example.com')
    user2 = make_user(email='user2@example.com')

    # when/then
    assert admin.role == 'admin'
    assert user1.email == 'user1@example.com'
    assert user2.email == 'user2@example.com'
```

---

## Pattern 7: Cleanup and Teardown

### Using yield for Cleanup

```python
@pytest.fixture
def temporary_file():
    """Create temporary file and clean up after test."""
    import tempfile
    import os

    # Setup
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write('test data')

    # Provide to test
    yield path

    # Teardown (always runs)
    if os.path.exists(path):
        os.remove(path)


def test_file_processing(temporary_file):
    """Test file processing with automatic cleanup."""
    result = process_file(temporary_file)
    assert result is True
    # File is automatically cleaned up after test
```

### Multiple Teardown Steps

```python
@pytest.fixture
def test_environment(mocker):
    """Set up and tear down test environment."""
    # Setup
    mock_api = mocker.patch('external_api.client')
    test_data = create_test_data()
    cache.clear()

    yield {
        'mock_api': mock_api,
        'test_data': test_data,
    }

    # Teardown
    cache.clear()
    delete_test_data(test_data)
    # Mocks are automatically cleaned up by pytest-mock
```

---

## Pattern 8: Parameterized Fixtures

### Fixture with Parameters

```python
@pytest.fixture(params=['admin', 'moderator', 'user'])
def user_role(request):
    """Create user with different roles."""
    return UserFactory(role=request.param)


def test_user_permissions__all_roles__have_basic_access(user_role):
    """Test all user roles have basic access.

    This test runs 3 times with different user roles.
    """
    user = user_role
    assert user.can_read() is True
```

### Fixture with Named Parameters

```python
@pytest.fixture(
    params=[
        pytest.param('active', id='active_user'),
        pytest.param('inactive', id='inactive_user'),
        pytest.param('suspended', id='suspended_user'),
    ]
)
def user_status(request):
    """Create user with different statuses."""
    return UserFactory(status=request.param)


def test_user_login__various_statuses(user_status):
    """Test login with various user statuses."""
    user = user_status
    if user.status == 'active':
        assert can_login(user) is True
    else:
        assert can_login(user) is False
```

---

## Best Practices

1. **Fixtures in file** - Default to defining fixtures in test file
2. **conftest.py minimal** - Only truly shared fixtures
3. **No autouse** - Make dependencies explicit (except global protections)
4. **@pytest.mark.usefixtures** - For fixtures with side effects
5. **Function scope default** - Safest, most predictable
6. **yield for cleanup** - Ensure teardown always runs
7. **Clear names** - Fixture name should describe what it provides
8. **Docstrings** - Document what fixture provides and why
9. **Avoid nesting** - Keep fixture dependencies shallow
10. **Test isolation** - Each test should be independent

---

*Related: See `skill.md` for complete Django testing guide*
