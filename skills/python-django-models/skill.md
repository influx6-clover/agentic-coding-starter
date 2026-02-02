---
name: "Python Django Models"
description: "Django model patterns with base classes, query optimization, and real database testing"
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
  - models
  - orm
  - database
  - query-optimization
files:
  - examples/base-models-guide.md: "Complete guide to Django base model classes"
  - examples/query-optimization.md: "Query optimization patterns and N+1 prevention"
  - examples/testing-with-docker.md: "Testing Django models with real databases"
---

# Python Django Models

## When to Use This Skill

Read this when:
- Creating Django models with proper base classes
- Optimizing database queries
- Preventing N+1 query problems
- Working with UUIDs, timestamps, soft deletes
- Testing Django models against real databases

---

## Critical Principles

### 1. Base Model Classes (MANDATORY)

**ALWAYS** inherit from project base model classes, **NEVER** directly from `models.Model`:

```python
# BAD ❌ - Direct Django model inheritance
class User(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

# GOOD ✅ - Project base class inheritance
class User(UUIDPrimaryKeyModelBase, TimestampedModelBase):
    # UUID and timestamps handled by base classes
    name = models.CharField(max_length=255)
```

### 2. Query Optimization (CRITICAL)

**ALWAYS** use `select_related()` and `prefetch_related()` to prevent N+1 queries:

```python
# BAD ❌ - N+1 query problem
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # Queries database for EACH user!

# GOOD ✅ - Single query with select_related
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # No additional queries!
```

### 3. Real Database Testing (MANDATORY)

**ALWAYS** test Django models against real databases using Docker:

```python
# BAD ❌ - Mocking Django ORM
@patch('myapp.models.User.objects.get')
def test_user_fetch(mock_get):
    mock_get.return_value = Mock()  # Tests nothing!

# GOOD ✅ - Real PostgreSQL via Docker
def test_user_fetch(db):  # pytest-django fixture
    user = User.objects.create(name="Alice")
    fetched = User.objects.get(pk=user.pk)
    assert fetched.name == "Alice"
```

---

## Base Model Classes

### Available Base Classes

```python
# ca_lib/common/base_models.py (or project equivalent)

class UUIDPrimaryKeyModelBase(models.Model):
    """Provides UUID primary key instead of integer."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModelBase(models.Model):
    """Provides created_at and updated_at timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeletionTimestampModelBase(models.Model):
    """Provides soft delete with deleted_at timestamp."""
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark record as deleted without removing from database."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def is_deleted(self) -> bool:
        """Check if record is soft-deleted."""
        return self.deleted_at is not None


class EffectiveTimeRangeModelBase(models.Model):
    """Provides effective_from and effective_to for temporal data."""
    effective_from = models.DateTimeField(default=timezone.now)
    effective_to = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def is_effective(self, at_time: datetime | None = None) -> bool:
        """Check if record is effective at given time (default: now)."""
        check_time = at_time or timezone.now()
        if check_time < self.effective_from:
            return False
        if self.effective_to and check_time >= self.effective_to:
            return False
        return True
```

### Combining Base Classes

```python
from ca_lib.common.base_models import (
    UUIDPrimaryKeyModelBase,
    TimestampedModelBase,
    DeletionTimestampModelBase,
)

class User(UUIDPrimaryKeyModelBase, TimestampedModelBase, DeletionTimestampModelBase):
    """User model with UUID, timestamps, and soft delete support.

    Inherits:
        - id (UUID): Primary key
        - created_at (datetime): Auto-set on creation
        - updated_at (datetime): Auto-updated on save
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

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"
```

### Base Class Inheritance Order

**CRITICAL:** Django processes base classes from **left to right**. Put most specific first:

```python
# CORRECT ✅ - Specific to general
class User(UUIDPrimaryKeyModelBase, TimestampedModelBase, DeletionTimestampModelBase):
    pass

# ALSO CORRECT ✅ - Common pattern
class User(TimestampedModelBase, UUIDPrimaryKeyModelBase, DeletionTimestampModelBase):
    pass

# AVOID ❌ - Field conflicts may occur with wrong order
class User(DeletionTimestampModelBase, TimestampedModelBase, UUIDPrimaryKeyModelBase):
    pass  # May cause field ordering issues
```

---

## Query Optimization Patterns

### 1. Select Related (ForeignKey and OneToOne)

Use `select_related()` for **single-valued relationships**:

```python
# BAD ❌ - N+1 query problem
def get_posts_with_authors():
    posts = Post.objects.all()
    for post in posts:
        print(post.author.name)  # Database hit for EACH post!
    # Executes: 1 query for posts + N queries for authors = N+1 queries

# GOOD ✅ - Single JOIN query
def get_posts_with_authors():
    posts = Post.objects.select_related('author').all()
    for post in posts:
        print(post.author.name)  # No additional queries!
    # Executes: 1 query with JOIN

# EXCELLENT ✅✅ - Multiple relations
def get_posts_with_related():
    posts = Post.objects.select_related(
        'author',           # ForeignKey to User
        'author__profile',  # Through author to profile
        'category',         # ForeignKey to Category
    ).all()
    # Single query with multiple JOINs
```

### 2. Prefetch Related (ManyToMany and Reverse ForeignKey)

Use `prefetch_related()` for **multi-valued relationships**:

```python
# BAD ❌ - N+1 query problem
def get_users_with_groups():
    users = User.objects.all()
    for user in users:
        print([g.name for g in user.groups.all()])  # Query for EACH user!
    # Executes: 1 query for users + N queries for groups = N+1 queries

# GOOD ✅ - Separate optimized query
def get_users_with_groups():
    users = User.objects.prefetch_related('groups').all()
    for user in users:
        print([g.name for g in user.groups.all()])  # No additional queries!
    # Executes: 2 queries total (users, then all groups in one query)

# EXCELLENT ✅✅ - Multiple prefetches
def get_users_with_data():
    users = User.objects.prefetch_related(
        'groups',                    # ManyToMany
        'posts',                     # Reverse ForeignKey
        'posts__comments',           # Through posts to comments
        'posts__comments__author',   # Deep prefetch
    ).all()
    # Executes: 4 optimized queries total (no N+1)
```

### 3. Combining Select and Prefetch

```python
def get_posts_optimized():
    """Fetch posts with all related data efficiently."""
    return Post.objects.select_related(
        'author',           # Single-valued: use select_related
        'category',
    ).prefetch_related(
        'tags',            # Multi-valued: use prefetch_related
        'comments',
        'comments__author',
    ).all()
    # Optimal query pattern:
    # - 1 query with JOINs for author/category
    # - 3 separate queries for tags/comments/comment_authors
    # Total: 4 queries regardless of result size
```

### 4. Custom Prefetch Objects

For complex scenarios, use `Prefetch` objects:

```python
from django.db.models import Prefetch

def get_users_with_recent_posts():
    """Get users with their recent posts only."""
    recent_posts = Post.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).select_related('category')

    return User.objects.prefetch_related(
        Prefetch(
            'posts',
            queryset=recent_posts,
            to_attr='recent_posts',  # Access via user.recent_posts
        )
    ).all()

# Usage
users = get_users_with_recent_posts()
for user in users:
    for post in user.recent_posts:  # Only recent posts, pre-filtered
        print(post.title)
```

### 5. Only and Defer (Field Selection)

Limit fields to reduce data transfer:

```python
# Only specific fields
users = User.objects.only('id', 'name', 'email')
# SELECT id, name, email FROM users

# Exclude specific fields
users = User.objects.defer('bio', 'profile_image')
# SELECT all fields EXCEPT bio and profile_image

# CAUTION ⚠️ - Accessing deferred fields causes additional query!
user = User.objects.defer('bio').first()
print(user.bio)  # Triggers additional query!
```

### 6. Bulk Operations

Use bulk methods for performance:

```python
# BAD ❌ - Multiple database hits
for user in users:
    user.is_active = True
    user.save()  # One query per user!

# GOOD ✅ - Single query
User.objects.filter(pk__in=user_ids).update(is_active=True)

# BULK CREATE ✅
users_to_create = [
    User(name=f"User {i}", email=f"user{i}@example.com")
    for i in range(1000)
]
User.objects.bulk_create(users_to_create, batch_size=500)

# BULK UPDATE ✅ (Django 4.2+)
users = User.objects.all()
for user in users:
    user.last_login = timezone.now()
User.objects.bulk_update(users, ['last_login'], batch_size=500)
```

---

## Transaction Patterns

### 1. Atomic Transactions

```python
from django.db import transaction

@transaction.atomic
def create_user_with_profile(user_data: dict, profile_data: dict) -> User:
    """Create user and profile in single transaction.

    Args:
        user_data: User model fields
        profile_data: Profile model fields

    Returns:
        Created user instance with profile

    Raises:
        ValidationError: If data is invalid
        DatabaseError: If transaction fails (auto-rollback)
    """
    user = User.objects.create(**user_data)
    profile = Profile.objects.create(user=user, **profile_data)
    return user

# Manual transaction control
def update_user_balance(user_id: UUID, amount: Decimal) -> None:
    """Update user balance with explicit transaction control."""
    with transaction.atomic():
        # Create savepoint
        sid = transaction.savepoint()

        try:
            user = User.objects.select_for_update().get(pk=user_id)
            user.balance += amount
            user.save()
            transaction.savepoint_commit(sid)
        except Exception:
            transaction.savepoint_rollback(sid)
            raise
```

### 2. Performance Transaction Pattern

**CRITICAL:** Disable savepoints for better performance when appropriate:

```python
# Normal transactions (with savepoint overhead)
@transaction.atomic
def process_records(records):
    for record in records:
        process_one(record)  # Each call creates savepoint

# High-performance transactions (no savepoint overhead)
@transaction.atomic(savepoint=False)
def process_records_fast(records):
    """Process records without savepoint overhead.

    Use when:
    - Processing many records in loop
    - No need for partial rollback
    - Performance is critical

    WARNING: Cannot rollback to middle of transaction!
    """
    for record in records:
        process_one(record)  # No savepoint overhead
```

---

## Datetime Handling

### 1. Always Use Timezone-Aware Datetimes

```python
from django.utils import timezone
from datetime import datetime, timedelta

# BAD ❌ - Naive datetime
class Event(models.Model):
    start_time = models.DateTimeField(default=datetime.now)  # WRONG!

# GOOD ✅ - Timezone-aware datetime
class Event(models.Model):
    start_time = models.DateTimeField(default=timezone.now)  # CORRECT!

# Creating timezone-aware datetimes
now = timezone.now()  # Current time in project timezone
yesterday = timezone.now() - timedelta(days=1)

# Converting naive to aware (if necessary)
naive_dt = datetime(2024, 1, 1, 12, 0, 0)
aware_dt = timezone.make_aware(naive_dt)
```

### 2. Filtering by Date Ranges

```python
from django.utils import timezone
from datetime import timedelta

def get_recent_posts(days: int = 7):
    """Get posts from last N days."""
    cutoff = timezone.now() - timedelta(days=days)
    return Post.objects.filter(created_at__gte=cutoff)

def get_posts_in_range(start: datetime, end: datetime):
    """Get posts within date range."""
    return Post.objects.filter(
        created_at__gte=start,
        created_at__lt=end,  # Exclusive end
    )

# Date-only filtering (ignores time component)
def get_posts_on_date(date):
    """Get all posts on specific date."""
    return Post.objects.filter(created_at__date=date)
```

---

## Enum Integration

### 1. TextChoices and IntegerChoices

```python
from django.db import models

class UserRole(models.TextChoices):
    """User role enumeration.

    Use TextChoices for human-readable values.
    Use IntegerChoices for performance (smaller storage).
    """
    ADMIN = 'ADMIN', 'Administrator'
    MODERATOR = 'MODERATOR', 'Moderator'
    USER = 'USER', 'Regular User'
    GUEST = 'GUEST', 'Guest User'


class User(UUIDPrimaryKeyModelBase, TimestampedModelBase):
    """User with role enum."""
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

    def can_moderate(self) -> bool:
        """Check if user can moderate."""
        return self.role in [UserRole.ADMIN, UserRole.MODERATOR]


# Usage in queries
admins = User.objects.filter(role=UserRole.ADMIN)
staff = User.objects.filter(role__in=[UserRole.ADMIN, UserRole.MODERATOR])
```

### 2. IntegerChoices for Performance

```python
class OrderStatus(models.IntegerChoices):
    """Order status with integer values for better performance."""
    PENDING = 1, 'Pending'
    PROCESSING = 2, 'Processing'
    SHIPPED = 3, 'Shipped'
    DELIVERED = 4, 'Delivered'
    CANCELLED = 5, 'Cancelled'


class Order(UUIDPrimaryKeyModelBase, TimestampedModelBase):
    """Order with integer-based status enum."""
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,  # Index for frequent filtering
    )

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
```

---

## Testing Django Models

### 1. Real Database Testing (MANDATORY)

**CRITICAL:** Always test against real databases using Docker. Never mock Django ORM.

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "myproject.settings.test"
addopts = [
    "--reuse-db",           # Reuse test database between runs
    "--create-db",          # Create test database if needed
    "--nomigrations",       # Skip migrations for speed (optional)
]

# conftest.py - Docker PostgreSQL setup
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
```

### 2. Model Testing with Factory-Boy

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from myapp.models import User, Post, UserRole

class UserFactory(DjangoModelFactory):
    """Factory for User model with realistic data."""

    class Meta:
        model = User
        django_get_or_create = ('email',)  # Avoid duplicates

    name = factory.Faker('name')
    email = factory.Faker('email')
    role = UserRole.USER

    @factory.post_generation
    def with_profile(self, create, extracted, **kwargs):
        """Optionally create profile with user."""
        if extracted:
            ProfileFactory(user=self, **kwargs)


class PostFactory(DjangoModelFactory):
    """Factory for Post model."""

    class Meta:
        model = Post

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags if provided."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)


# tests/test_models.py - Using factories with real database
import pytest
from tests.factories import UserFactory, PostFactory

@pytest.mark.django_db
def test_user_creation__with_real_db__persists():
    """Test user creation against real PostgreSQL.

    Given: A user factory with valid data
    When: User is created in real database
    Then: User is persisted with correct attributes
    """
    # given: Factory creates user in real DB
    user = UserFactory(name="Alice", email="alice@example.com")

    # when: Fetch from database
    fetched = User.objects.get(pk=user.pk)

    # then: Attributes match
    assert fetched.name == "Alice"
    assert fetched.email == "alice@example.com"
    assert fetched.role == UserRole.USER
    assert fetched.created_at is not None
    assert not fetched.is_deleted()


@pytest.mark.django_db
def test_post_with_author__query_optimization__no_n_plus_1():
    """Test query optimization with select_related.

    Given: Multiple posts with authors in real database
    When: Fetching posts with select_related
    Then: No N+1 query problem occurs
    """
    # given: Create posts with authors
    users = UserFactory.create_batch(10)
    posts = [PostFactory(author=user) for user in users]

    # when: Fetch with select_related
    from django.test.utils import CaptureQueriesContext
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        fetched_posts = list(
            Post.objects.select_related('author').all()
        )
        for post in fetched_posts:
            _ = post.author.name  # Access author (should not query)

    # then: Only 1 query executed (no N+1)
    assert len(context.captured_queries) == 1


@pytest.mark.django_db
def test_soft_delete__user__marks_deleted():
    """Test soft delete functionality.

    Given: An active user in real database
    When: Soft delete is called
    Then: User is marked as deleted but not removed
    """
    # given: Active user
    user = UserFactory()
    assert not user.is_deleted()

    # when: Soft delete
    user.soft_delete()

    # then: User marked deleted but exists in DB
    user.refresh_from_db()
    assert user.is_deleted()
    assert user.deleted_at is not None
    assert User.objects.filter(pk=user.pk).exists()
```

### 3. Deterministic Testing with freezegun

```python
import pytest
from freezegun import freeze_time
from django.utils import timezone
from tests.factories import PostFactory

@pytest.mark.django_db
@freeze_time("2024-01-15 12:00:00")
def test_recent_posts__with_frozen_time__filters_correctly():
    """Test recent posts filtering with deterministic time.

    Given: Posts created at known times (using frozen time)
    When: Filtering for recent posts
    Then: Only posts within timeframe are returned
    """
    # given: Posts at different times
    with freeze_time("2024-01-10"):
        old_post = PostFactory(title="Old Post")

    with freeze_time("2024-01-14"):
        recent_post = PostFactory(title="Recent Post")

    # when: Get posts from last 3 days
    cutoff = timezone.now() - timedelta(days=3)
    recent = Post.objects.filter(created_at__gte=cutoff)

    # then: Only recent post returned
    assert list(recent) == [recent_post]
    assert old_post not in recent
```

---

## Common Pitfalls

### Pitfall 1: Direct Model Inheritance

```python
# BAD ❌ - Missing base class benefits
class User(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Duplicating common fields!

# GOOD ✅ - Use base classes
class User(UUIDPrimaryKeyModelBase, TimestampedModelBase):
    # UUID and timestamps inherited!
    name = models.CharField(max_length=255)
```

### Pitfall 2: N+1 Query Problem

```python
# BAD ❌ - N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # Query for each post!

# GOOD ✅ - Optimized queries
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # No additional queries
```

### Pitfall 3: Naive Datetimes

```python
# BAD ❌ - Naive datetime
from datetime import datetime
event_time = datetime.now()  # Naive datetime!

# GOOD ✅ - Timezone-aware datetime
from django.utils import timezone
event_time = timezone.now()  # Aware datetime
```

### Pitfall 4: Mocking Django ORM

```python
# BAD ❌ - Mocking ORM (tests nothing!)
@patch('myapp.models.User.objects.get')
def test_user_fetch(mock_get):
    mock_get.return_value = Mock(name="Alice")
    # This doesn't test actual database behavior!

# GOOD ✅ - Real database testing
@pytest.mark.django_db
def test_user_fetch():
    user = UserFactory(name="Alice")
    fetched = User.objects.get(pk=user.pk)
    assert fetched.name == "Alice"
```

### Pitfall 5: Transaction Performance

```python
# SLOW 🐢 - Savepoint overhead in loop
@transaction.atomic
def process_many_records(records):
    for record in records:
        # Each iteration creates savepoint overhead!
        process_record(record)

# FAST ⚡ - Disabled savepoints
@transaction.atomic(savepoint=False)
def process_many_records(records):
    for record in records:
        # No savepoint overhead!
        process_record(record)
```

---

## Integration with Other Skills

### From python-testing-excellence

- **Docker/docker-compose** (FIRST): Real PostgreSQL/MySQL for tests
- **Factory-Boy**: Generate realistic test data
- **pytest-django**: Django-specific test fixtures
- **Given/When/Then**: Clear test structure

### From python-clean-implementation

- **Type hints**: All model methods must have type hints
- **Docstrings**: Document model purpose and fields
- **Custom exceptions**: Raise specific exceptions, not generic ones

### From python-with-async-code

- When using Django with async views:
  - Use `sync_to_async` for ORM calls
  - Never block event loop with synchronous queries
  - Use `QuerySet.aiterator()` for async iteration (Django 4.1+)

---

## Learning Log

### 2026-02-02: Python Django Models Skill Created

**Issue:** Need comprehensive Django model patterns for Python projects.

**Learning:** Created Django models skill covering:
- Base model classes from counterpart prompts (UUID, timestamps, soft delete, temporal)
- Query optimization patterns (select_related, prefetch_related, bulk operations)
- Transaction performance patterns (savepoint=False)
- Real database testing with Docker and Factory-Boy
- Enum integration with TextChoices/IntegerChoices
- Datetime handling with timezone awareness

**Adaptation:** Integrated with existing Python skills:
- Docker testing principle from python-testing-excellence (FIRST priority)
- Type hints and docstrings from python-clean-implementation
- No mocking of Django ORM (Real code over mocks philosophy)

**New Standard:** All Django models must follow these patterns.

---

## Examples

See `examples/` directory for detailed guides:

- `base-models-guide.md` - Complete guide to base model classes
- `query-optimization.md` - Query optimization patterns and N+1 prevention
- `testing-with-docker.md` - Testing Django models with real databases

## Related Skills

- [Python Testing Excellence](../python-testing-excellence/skill.md) - For testing patterns
- [Python Clean Implementation](../python-clean-implementation/skill.md) - For code quality
- [Python Directory and Configuration](../python-directory-and-configuration/skill.md) - For project setup

---

*Created: 2026-02-02*
*Version: 1.0*
