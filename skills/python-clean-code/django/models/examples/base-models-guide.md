# Django Base Model Classes - Complete Guide

This guide covers the project's base model classes and when to use them.

---

## Overview

**NEVER** inherit directly from `django.db.models.Model`. **ALWAYS** use project base classes.

```python
# ❌ WRONG - Direct Django inheritance
class MyModel(models.Model):
    pass

# ✅ CORRECT - Project base class
class MyModel(UUIDPrimaryKeyModelBase):
    pass
```

---

## Available Base Classes

### 1. UUIDPrimaryKeyModelBase

**Use when:** You want UUID primary keys instead of integer IDs.

**Benefits:**
- No sequential IDs (better security)
- Globally unique across databases
- Safe for distributed systems
- No ID conflicts when merging databases

```python
from ca_lib.common.base_models import UUIDPrimaryKeyModelBase

class User(UUIDPrimaryKeyModelBase):
    """User model with UUID primary key."""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

# Usage
user = User.objects.create(name="Alice", email="alice@example.com")
print(user.id)  # UUID('550e8400-e29b-41d4-a716-446655440000')
```

**Field provided:**
- `id`: UUID field, auto-generated, primary key

---

### 2. TimestampedModelBase

**Use when:** You need automatic timestamp tracking.

**Benefits:**
- Automatic `created_at` on creation
- Automatic `updated_at` on every save
- No manual timestamp management
- Audit trail for all records

```python
from ca_lib.common.base_models import TimestampedModelBase

class Post(TimestampedModelBase):
    """Blog post with automatic timestamps."""
    title = models.CharField(max_length=255)
    content = models.TextField()

# Usage
post = Post.objects.create(title="Hello", content="World")
print(post.created_at)  # 2024-01-15 10:30:00+00:00
print(post.updated_at)  # 2024-01-15 10:30:00+00:00

post.content = "Updated content"
post.save()
print(post.updated_at)  # 2024-01-15 10:45:00+00:00 (auto-updated!)
```

**Fields provided:**
- `created_at`: DateTimeField, auto-set on creation
- `updated_at`: DateTimeField, auto-updated on save

---

### 3. DeletionTimestampModelBase

**Use when:** You need soft delete (mark as deleted without removing from database).

**Benefits:**
- Data preservation for audit/recovery
- Can restore deleted records
- Historical data analysis
- Compliance requirements (GDPR, SOX, etc.)

```python
from ca_lib.common.base_models import DeletionTimestampModelBase

class User(DeletionTimestampModelBase):
    """User with soft delete support."""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

# Usage
user = User.objects.create(name="Alice", email="alice@example.com")
print(user.is_deleted())  # False

# Soft delete
user.soft_delete()
print(user.is_deleted())  # True
print(user.deleted_at)    # 2024-01-15 11:00:00+00:00

# User still exists in database!
assert User.objects.filter(pk=user.pk).exists()

# Filter active users
active_users = User.objects.filter(deleted_at__isnull=True)
```

**Fields provided:**
- `deleted_at`: DateTimeField, null=True, blank=True

**Methods provided:**
- `soft_delete()`: Mark record as deleted
- `is_deleted()`: Check if record is deleted

---

### 4. EffectiveTimeRangeModelBase

**Use when:** You need temporal data with effective date ranges.

**Benefits:**
- Track when data is valid/active
- Historical data with effective periods
- Future-dated records
- Regulatory compliance (insurance, finance)

```python
from ca_lib.common.base_models import EffectiveTimeRangeModelBase

class PricingRule(EffectiveTimeRangeModelBase):
    """Pricing rule with effective date range."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Usage
from django.utils import timezone
from datetime import timedelta

# Current pricing
current_rule = PricingRule.objects.create(
    product=product,
    price=99.99,
    effective_from=timezone.now(),
    effective_to=None,  # Indefinite
)

# Future pricing (price increase next month)
future_rule = PricingRule.objects.create(
    product=product,
    price=109.99,
    effective_from=timezone.now() + timedelta(days=30),
    effective_to=None,
)

# Check if rule is currently effective
print(current_rule.is_effective())  # True
print(future_rule.is_effective())   # False

# Check if rule will be effective in 35 days
check_date = timezone.now() + timedelta(days=35)
print(future_rule.is_effective(at_time=check_date))  # True
```

**Fields provided:**
- `effective_from`: DateTimeField, default=timezone.now
- `effective_to`: DateTimeField, null=True, blank=True

**Methods provided:**
- `is_effective(at_time=None)`: Check if effective at given time (default: now)

---

## Combining Base Classes

**Most common pattern:** Combine multiple base classes for rich functionality.

### Pattern 1: UUID + Timestamps (Most Common)

```python
from ca_lib.common.base_models import (
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
)

class User(UUIDPrimaryKeyModelBase, TimestampedModelBase):
    """User with UUID and timestamps.

    Inherits:
        - id (UUID): Primary key
        - created_at (datetime): Creation timestamp
        - updated_at (datetime): Last update timestamp
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'users'
```

### Pattern 2: UUID + Timestamps + Soft Delete

```python
from ca_lib.common.base_models import (
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
)

class User(UUIDPrimaryKeyModelBase, TimestampedModelBase, DeletionTimestampModelBase):
    """User with UUID, timestamps, and soft delete.

    Inherits:
        - id (UUID): Primary key
        - created_at (datetime): Creation timestamp
        - updated_at (datetime): Last update timestamp
        - deleted_at (datetime): Soft delete timestamp
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['deleted_at']),  # For filtering active users
        ]

# Custom manager for active users only
class ActiveUserManager(models.Manager):
    """Manager that returns only non-deleted users."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(UUIDPrimaryKeyModelBase, TimestampedModelBase, DeletionTimestampModelBase):
    # ... fields ...

    objects = models.Manager()  # Default manager (all users)
    active = ActiveUserManager()  # Active users only

# Usage
all_users = User.objects.all()      # Including deleted
active_users = User.active.all()    # Only non-deleted
```

### Pattern 3: Timestamps + Temporal Data

```python
from ca_lib.common.base_models import (
    TimestampedModelBase,
    EffectiveTimeRangeModelBase,
)

class Contract(TimestampedModelBase, EffectiveTimeRangeModelBase):
    """Contract with creation tracking and effective period.

    Inherits:
        - created_at (datetime): When contract was created
        - updated_at (datetime): When contract was last modified
        - effective_from (datetime): When contract starts
        - effective_to (datetime): When contract ends
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    terms = models.TextField()
    value = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'contracts'
        indexes = [
            models.Index(fields=['effective_from', 'effective_to']),
        ]

    @classmethod
    def get_active_contracts(cls, at_time=None):
        """Get contracts effective at given time."""
        check_time = at_time or timezone.now()
        return cls.objects.filter(
            effective_from__lte=check_time,
            Q(effective_to__isnull=True) | Q(effective_to__gt=check_time)
        )
```

### Pattern 4: All Base Classes Combined

```python
from ca_lib.common.base_models import (
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
    EffectiveTimeRangeModelBase,
)

class PolicyVersion(
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
    EffectiveTimeRangeModelBase,
):
    """Insurance policy version with full tracking.

    Inherits:
        - id (UUID): Unique version identifier
        - created_at (datetime): When version was created
        - updated_at (datetime): When version was last modified
        - deleted_at (datetime): When version was soft-deleted
        - effective_from (datetime): When policy version becomes active
        - effective_to (datetime): When policy version expires

    Use case: Insurance policy with multiple versions, each with
    effective periods, audit trail, and soft delete capability.
    """
    policy_number = models.CharField(max_length=50)
    terms = models.TextField()
    premium = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'policy_versions'
        indexes = [
            models.Index(fields=['policy_number', 'effective_from']),
            models.Index(fields=['deleted_at']),
        ]

    @classmethod
    def get_current_version(cls, policy_number: str):
        """Get currently effective, non-deleted version."""
        return cls.objects.filter(
            policy_number=policy_number,
            deleted_at__isnull=True,
        ).filter(
            effective_from__lte=timezone.now(),
        ).filter(
            Q(effective_to__isnull=True) | Q(effective_to__gt=timezone.now())
        ).first()
```

---

## Base Class Inheritance Order

**Rule:** Django processes base classes **left to right**.

**Recommendation:** Order from most specific to most general.

```python
# RECOMMENDED ORDER ✅
class MyModel(
    UUIDPrimaryKeyModelBase,      # Most specific (primary key)
    TimestampedModelBase,          # Medium specific (timestamps)
    DeletionTimestampModelBase,    # Medium specific (soft delete)
    EffectiveTimeRangeModelBase,   # General (temporal)
):
    pass

# ALSO VALID ✅
class MyModel(
    TimestampedModelBase,
    UUIDPrimaryKeyModelBase,
    DeletionTimestampModelBase,
):
    pass

# AVOID ❌ - May cause field ordering issues
class MyModel(
    EffectiveTimeRangeModelBase,
    DeletionTimestampModelBase,
    TimestampedModelBase,
    UUIDPrimaryKeyModelBase,
):
    pass
```

---

## Custom Base Classes

**When to create:** Project-specific patterns used across many models.

```python
# myapp/models/base.py
from ca_lib.common.base_models import (
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
)

class ProjectBaseModel(
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
):
    """Standard base model for all project models.

    Provides:
        - UUID primary key
        - Automatic timestamps
        - Soft delete capability
    """

    class Meta:
        abstract = True  # CRITICAL: Must be abstract!

    def __repr__(self) -> str:
        """Standard repr for all models."""
        return f"<{self.__class__.__name__}(id={self.id})>"


# myapp/models/user.py
from myapp.models.base import ProjectBaseModel

class User(ProjectBaseModel):
    """User model with all standard base fields."""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'users'
```

---

## Migration Considerations

### Adding Base Classes to Existing Models

**Scenario:** Existing model needs timestamps added.

```python
# BEFORE
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

# AFTER
class User(TimestampedModelBase):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

# Migration will add created_at and updated_at fields
# IMPORTANT: Set default for existing records!
```

**Migration file:**

```python
# Generated migration
from django.utils import timezone

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=timezone.now,  # For existing records
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(
                auto_now=True,
                default=timezone.now,  # For existing records
            ),
            preserve_default=False,
        ),
    ]
```

---

## Testing Base Models

```python
# tests/test_base_models.py
import pytest
from freezegun import freeze_time
from django.utils import timezone
from tests.factories import UserFactory

@pytest.mark.django_db
def test_uuid_primary_key__creates_uuid():
    """Test UUID primary key generation."""
    # given/when: Create user
    user = UserFactory()

    # then: ID is UUID
    from uuid import UUID
    assert isinstance(user.id, UUID)
    assert str(user.id)  # Can convert to string


@pytest.mark.django_db
@freeze_time("2024-01-15 10:00:00")
def test_timestamped__auto_sets_timestamps():
    """Test automatic timestamp behavior."""
    # given/when: Create user
    user = UserFactory()

    # then: Timestamps are set
    assert user.created_at == timezone.now()
    assert user.updated_at == timezone.now()


@pytest.mark.django_db
@freeze_time("2024-01-15 10:00:00")
def test_timestamped__updates_updated_at():
    """Test updated_at auto-update on save."""
    # given: User created at specific time
    user = UserFactory()
    original_updated = user.updated_at

    # when: Update after time passes
    with freeze_time("2024-01-15 11:00:00"):
        user.name = "Updated Name"
        user.save()

    # then: updated_at changed, created_at did not
    assert user.updated_at > original_updated
    assert user.created_at == timezone.datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)


@pytest.mark.django_db
def test_soft_delete__marks_deleted():
    """Test soft delete functionality."""
    # given: Active user
    user = UserFactory()
    assert not user.is_deleted()

    # when: Soft delete
    user.soft_delete()

    # then: Marked deleted, still in database
    assert user.is_deleted()
    assert user.deleted_at is not None
    assert User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_effective_time_range__is_effective():
    """Test effective time range checking."""
    # given: Rule effective from now to tomorrow
    rule = PricingRuleFactory(
        effective_from=timezone.now(),
        effective_to=timezone.now() + timedelta(days=1),
    )

    # then: Currently effective
    assert rule.is_effective()

    # when/then: Not effective yesterday
    yesterday = timezone.now() - timedelta(days=1)
    assert not rule.is_effective(at_time=yesterday)

    # when/then: Not effective in 2 days
    future = timezone.now() + timedelta(days=2)
    assert not rule.is_effective(at_time=future)
```

---

## Best Practices

1. **Always use base classes** - Never inherit directly from `models.Model`
2. **Combine as needed** - Use multiple base classes for rich functionality
3. **Index soft delete** - Add index on `deleted_at` for filtering performance
4. **Custom managers** - Create managers for common filters (e.g., active users)
5. **Document inheritance** - Use docstrings to list inherited fields
6. **Test with real DB** - Never mock base model behavior

---

*Related: See `skill.md` for complete Django models guide*
