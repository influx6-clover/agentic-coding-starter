# Factory-Boy Guide for Django

This guide covers using Factory-Boy to generate Django model test data.

---

## Why Factory-Boy?

**Problems with manual test data:**
- Repetitive model creation code
- Hard to maintain when models change
- Difficult to create related objects
- No realistic fake data

**Benefits of Factory-Boy:**
- DRY principle - define once, use everywhere
- Automatic handling of required fields
- Easy creation of related objects
- Realistic fake data with Faker
- Flexible overrides for test-specific data

---

## Installation

```bash
pip install factory-boy faker
# or
poetry add --group dev factory-boy faker
```

---

## Basic Factory Pattern

### Simple Factory

```python
# myapp/factories.py
import factory
from factory.django import DjangoModelFactory
from myapp import models

class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = models.User

    # Simple fields
    name = 'Test User'
    email = 'test@example.com'
    is_active = True
```

### Usage

```python
# tests/test_users.py
import pytest
from myapp.factories import UserFactory

@pytest.mark.django_db
def test_user_creation():
    """Test user creation with factory."""
    # Create user with defaults
    user = UserFactory()

    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.is_active is True


@pytest.mark.django_db
def test_user_creation__custom_name__uses_custom():
    """Test user creation with custom name."""
    # Override defaults
    user = UserFactory(name='Alice', email='alice@example.com')

    assert user.name == 'Alice'
    assert user.email == 'alice@example.com'
```

---

## Using Faker for Realistic Data

### Basic Faker Usage

```python
from factory import Faker

class UserFactory(DjangoModelFactory):
    """Factory with Faker for realistic data."""

    class Meta:
        model = models.User

    name = Faker('name')  # Random name
    email = Faker('email')  # Random email
    username = Faker('user_name')  # Random username
    address = Faker('address')  # Random address
```

### Faker with Parameters

```python
class UserFactory(DjangoModelFactory):
    """Factory with parameterized Faker."""

    class Meta:
        model = models.User

    # Sentence with 6 words
    bio = Faker('sentence', nb_words=6)

    # Paragraph with 3 sentences
    description = Faker('paragraph', nb_sentences=3)

    # Company name
    company = Faker('company')

    # URL
    website = Faker('url')

    # Phone number
    phone = Faker('phone_number')
```

### Common Faker Providers

```python
class PostFactory(DjangoModelFactory):
    """Factory demonstrating common Faker providers."""

    class Meta:
        model = models.Post

    # Text
    title = Faker('sentence', nb_words=6)
    content = Faker('paragraph', nb_sentences=5)
    slug = Faker('slug')

    # Identifiers
    uuid = Faker('uuid4')

    # Dates and times
    published_at = Faker('date_time_this_year')
    created_date = Faker('date_this_year')

    # Numbers
    view_count = Faker('random_int', min=0, max=1000)
    rating = Faker('pyfloat', left_digits=1, right_digits=2, positive=True, max_value=5)

    # Boolean
    is_featured = Faker('boolean')

    # Choice from list
    category = Faker('random_element', elements=['tech', 'science', 'art'])
```

---

## Sequences for Unique Values

### Basic Sequence

```python
from factory import Sequence

class UserFactory(DjangoModelFactory):
    """Factory with sequences for unique values."""

    class Meta:
        model = models.User

    # Generates: test1@example.com, test2@example.com, test3@example.com
    email = Sequence(lambda n: f'test{n}@example.com')

    # Generates: user1, user2, user3
    username = Sequence(lambda n: f'user{n}')
```

### Sequence with Padding

```python
class OrderFactory(DjangoModelFactory):
    """Factory with padded sequences."""

    class Meta:
        model = models.Order

    # Generates: ORD-00001, ORD-00002, ORD-00003
    order_number = Sequence(lambda n: f'ORD-{n:05d}')

    # Generates: INV-000001, INV-000002, INV-000003
    invoice_number = Sequence(lambda n: f'INV-{n:06d}')
```

---

## Related Objects with SubFactory

### One-to-Many Relationship

```python
class OrganizationFactory(DjangoModelFactory):
    """Factory for Organization."""

    class Meta:
        model = models.Organization

    name = Faker('company')


class UserFactory(DjangoModelFactory):
    """Factory for User with organization relationship."""

    class Meta:
        model = models.User

    name = Faker('name')
    email = Faker('email')
    organization = SubFactory(OrganizationFactory)  # Auto-creates organization
```

### Usage

```python
@pytest.mark.django_db
def test_user_with_organization():
    """Test user creation with related organization."""
    # Creates both user AND organization
    user = UserFactory()

    assert user.organization is not None
    assert isinstance(user.organization, Organization)


@pytest.mark.django_db
def test_user_with_existing_organization():
    """Test user with specific organization."""
    # Create organization first
    org = OrganizationFactory(name='Test Org')

    # Create users with same organization
    user1 = UserFactory(organization=org)
    user2 = UserFactory(organization=org)

    assert user1.organization == org
    assert user2.organization == org
```

### Nested SubFactories

```python
class ProfileFactory(DjangoModelFactory):
    """Factory for Profile."""

    class Meta:
        model = models.Profile

    bio = Faker('paragraph')
    website = Faker('url')


class UserFactory(DjangoModelFactory):
    """Factory for User with profile."""

    class Meta:
        model = models.User

    name = Faker('name')
    email = Faker('email')
    organization = SubFactory(OrganizationFactory)
    profile = SubFactory(ProfileFactory)  # Nested relationship


class PostFactory(DjangoModelFactory):
    """Factory for Post."""

    class Meta:
        model = models.Post

    title = Faker('sentence')
    content = Faker('paragraph')
    author = SubFactory(UserFactory)  # Creates user with org and profile!
```

---

## Post-Generation Hooks

### post_generation Decorator

```python
class UserFactory(DjangoModelFactory):
    """Factory with post-generation hook."""

    class Meta:
        model = models.User

    name = Faker('name')
    email = Faker('email')

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Add groups to user after creation.

        Usage:
            user = UserFactory()  # No groups
            user = UserFactory(groups=['admin', 'staff'])  # With groups
        """
        if not create:
            return  # Build strategy, not create

        if extracted:
            # Add specified groups
            for group in extracted:
                self.groups.add(group)


class PostFactory(DjangoModelFactory):
    """Factory with tags post-generation."""

    class Meta:
        model = models.Post

    title = Faker('sentence')
    content = Faker('paragraph')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags to post after creation.

        Usage:
            post = PostFactory()  # No tags
            post = PostFactory(tags=['python', 'django'])  # With tags
        """
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
```

### Usage

```python
@pytest.mark.django_db
def test_user_with_groups():
    """Test user with multiple groups."""
    # given: Create groups
    admin_group = Group.objects.create(name='admin')
    staff_group = Group.objects.create(name='staff')

    # when: Create user with groups
    user = UserFactory(groups=[admin_group, staff_group])

    # then: User has both groups
    assert user.groups.count() == 2
    assert admin_group in user.groups.all()
    assert staff_group in user.groups.all()


@pytest.mark.django_db
def test_post_with_tags():
    """Test post with tags."""
    # given: Create tags
    tag1 = Tag.objects.create(name='python')
    tag2 = Tag.objects.create(name='django')

    # when: Create post with tags
    post = PostFactory(tags=[tag1, tag2])

    # then: Post has tags
    assert post.tags.count() == 2
```

---

## LazyAttribute and LazyFunction

### LazyAttribute

```python
from factory import LazyAttribute

class UserFactory(DjangoModelFactory):
    """Factory with lazy attributes."""

    class Meta:
        model = models.User

    first_name = Faker('first_name')
    last_name = Faker('last_name')

    # Generated from first_name and last_name
    email = LazyAttribute(lambda obj: f'{obj.first_name}.{obj.last_name}@example.com'.lower())

    # Username from email
    username = LazyAttribute(lambda obj: obj.email.split('@')[0])
```

### LazyFunction

```python
from factory import LazyFunction
from datetime import date, timedelta

class SubscriptionFactory(DjangoModelFactory):
    """Factory with lazy functions."""

    class Meta:
        model = models.Subscription

    # Always today's date
    start_date = LazyFunction(date.today)

    # Always 30 days from today
    end_date = LazyFunction(lambda: date.today() + timedelta(days=30))
```

---

## Deterministic Test Data

### Problem: Non-Deterministic Tests

```python
# BAD ❌ - Non-deterministic
class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    registration_date = Faker('date_this_year')  # Random date!


def test_recent_registrations():
    """This test may pass or fail depending on random date!"""
    user = UserFactory()
    # Test logic depends on registration_date being recent
    assert is_recent_registration(user)  # May fail!
```

### Solution: Fixed Dates

```python
# GOOD ✅ - Deterministic
from datetime import date

class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    registration_date = date(2022, 1, 1)  # Fixed date


@freeze_time('2022-01-15 12:00:00+00:00')
def test_recent_registrations():
    """Test with frozen time and fixed dates."""
    user = UserFactory()
    assert user.registration_date == date(2022, 1, 1)
```

---

## Traits for Variations

### Using Traits

```python
class UserFactory(DjangoModelFactory):
    """Factory with traits for common variations."""

    class Meta:
        model = models.User

    name = Faker('name')
    email = Faker('email')
    is_active = True
    role = 'user'

    class Params:
        # Traits
        admin = factory.Trait(
            role='admin',
            is_staff=True,
        )

        inactive = factory.Trait(
            is_active=False,
        )

        with_profile = factory.Trait(
            profile=SubFactory(ProfileFactory),
        )
```

### Usage

```python
@pytest.mark.django_db
def test_admin_user():
    """Test admin user creation."""
    admin = UserFactory(admin=True)
    assert admin.role == 'admin'
    assert admin.is_staff is True


@pytest.mark.django_db
def test_inactive_user():
    """Test inactive user creation."""
    user = UserFactory(inactive=True)
    assert user.is_active is False


@pytest.mark.django_db
def test_user_with_profile():
    """Test user with profile."""
    user = UserFactory(with_profile=True)
    assert user.profile is not None
```

---

## Batch Creation

### Create Multiple Instances

```python
@pytest.mark.django_db
def test_bulk_user_creation():
    """Test creating multiple users."""
    # Create 10 users
    users = UserFactory.create_batch(10)

    assert len(users) == 10
    assert all(isinstance(u, User) for u in users)
    assert User.objects.count() == 10


@pytest.mark.django_db
def test_batch_with_overrides():
    """Test batch creation with overrides."""
    # Create 5 admin users
    admins = UserFactory.create_batch(5, role='admin')

    assert len(admins) == 5
    assert all(u.role == 'admin' for u in admins)
```

### Build vs Create

```python
@pytest.mark.django_db
def test_build_vs_create():
    """Test difference between build and create."""
    # build() - Create instance but DON'T save to database
    user1 = UserFactory.build()
    assert user1.pk is None  # Not saved

    # create() - Create and save to database
    user2 = UserFactory.create()
    assert user2.pk is not None  # Saved

    # Default behavior is create()
    user3 = UserFactory()
    assert user3.pk is not None  # Saved
```

---

## Custom Faker Providers

### Creating Custom Provider

```python
# myapp/faker_providers.py
from faker.providers import BaseProvider

class HealthcareProvider(BaseProvider):
    """Custom Faker provider for healthcare data."""

    def npi(self):
        """Generate valid NPI number."""
        from myapp.utils import validators

        # Generate 9-digit base
        npi_base = self.bothify(text='1########')

        # Calculate and append checksum
        checksum = validators.get_npi_checksum(npi_base)
        return f'{npi_base}{checksum}'

    def icd10_code(self):
        """Generate sample ICD-10 code."""
        letter = self.random_element(elements=['A', 'B', 'C', 'Z'])
        numbers = self.numerify(text='##')
        return f'{letter}{numbers}'
```

### Register and Use Custom Provider

```python
# myapp/factories.py
from faker import Faker
from myapp.faker_providers import HealthcareProvider

# Register custom provider
Faker.add_provider(HealthcareProvider)


class PractitionerFactory(DjangoModelFactory):
    """Factory using custom provider."""

    class Meta:
        model = models.Practitioner

    name = Faker('name')
    npi = Faker('npi')  # Uses custom provider
    specialty = Faker('random_element', elements=['cardiology', 'pediatrics'])


class DiagnosisFactory(DjangoModelFactory):
    """Factory with custom ICD-10 codes."""

    class Meta:
        model = models.Diagnosis

    code = Faker('icd10_code')  # Uses custom provider
    description = Faker('sentence')
```

---

## Advanced Patterns

### Conditional SubFactory

```python
from factory import Maybe

class PostFactory(DjangoModelFactory):
    """Factory with conditional author."""

    class Meta:
        model = models.Post

    title = Faker('sentence')
    content = Faker('paragraph')

    # Create author only if published
    author = Maybe(
        'is_published',
        yes_declaration=SubFactory(UserFactory),
        no_declaration=None,
    )

    class Params:
        is_published = True


# Usage
@pytest.mark.django_db
def test_draft_post_no_author():
    """Test draft post has no author."""
    draft = PostFactory(is_published=False)
    assert draft.author is None


@pytest.mark.django_db
def test_published_post_has_author():
    """Test published post has author."""
    published = PostFactory(is_published=True)
    assert published.author is not None
```

### SelfAttribute for Related Fields

```python
from factory import SelfAttribute

class UserFactory(DjangoModelFactory):
    """Factory with related email domain."""

    class Meta:
        model = models.User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = LazyAttribute(lambda obj: f'{obj.first_name}.{obj.last_name}@example.com'.lower())


class OrganizationFactory(DjangoModelFactory):
    """Factory with domain from primary user email."""

    class Meta:
        model = models.Organization

    name = Faker('company')
    primary_user = SubFactory(UserFactory)

    # Extract domain from primary user's email
    domain = LazyAttribute(lambda obj: obj.primary_user.email.split('@')[1])
```

---

## django_get_or_create

### Avoid Duplicate Objects

```python
class OrganizationFactory(DjangoModelFactory):
    """Factory that avoids duplicate organizations."""

    class Meta:
        model = models.Organization
        django_get_or_create = ('name',)  # Get existing or create new

    name = 'Default Organization'


@pytest.mark.django_db
def test_organization_get_or_create():
    """Test organization reuse."""
    # First call creates
    org1 = OrganizationFactory(name='Acme Corp')
    assert Organization.objects.count() == 1

    # Second call gets existing
    org2 = OrganizationFactory(name='Acme Corp')
    assert Organization.objects.count() == 1  # Still 1!
    assert org1.pk == org2.pk  # Same object
```

---

## Best Practices

1. **One factory per model** - Keep factories focused
2. **Realistic but deterministic** - Use Faker but fixed dates
3. **Minimal required fields** - Only define what's needed
4. **SubFactory for relationships** - Let factory handle related objects
5. **post_generation for ManyToMany** - Add after creation
6. **Traits for variations** - Common configurations as traits
7. **Create vs Build** - Use create() for database tests
8. **Batch creation** - Use create_batch() for multiple instances
9. **Custom providers** - Domain-specific fake data
10. **Document usage** - Add docstrings showing examples

---

*Related: See `skill.md` for complete Django testing guide*
