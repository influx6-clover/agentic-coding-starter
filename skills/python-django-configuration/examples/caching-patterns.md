# Django Caching Patterns

This guide covers Django caching configuration and usage patterns.

---

## Cache Backends

### Redis Cache (Production/Staging - Recommended)

```python
# myproject/settings/production.py
from configurations import values

class Production(Staging):
    """Production configuration with Redis caching."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': values.Value(
                'redis://localhost:6379/0',
                environ_name='REDIS_URL',
                environ_prefix=None,
            ).value,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            },
            'KEY_PREFIX': 'myproject',
            'TIMEOUT': 300,  # 5 minutes default
        },
    }
```

### Database Cache (Alternative for Multi-Server)

```python
# myproject/settings/common.py
class Common(Configuration):
    """Configuration with database caching."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache',  # Table name
            'OPTIONS': {
                'MAX_ENTRIES': 10000,
                'CULL_FREQUENCY': 4,  # 1/4 of entries removed when MAX_ENTRIES reached
            },
            'TIMEOUT': 300,
        },
    }

# Create cache table
# python manage.py createcachetable
```

### Memcached Cache

```python
class Production(Staging):
    """Production with Memcached."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': values.Value(
                '127.0.0.1:11211',
                environ_name='MEMCACHED_LOCATION',
                environ_prefix=None,
            ).value,
            'TIMEOUT': 300,
        },
    }
```

### Local Memory Cache (Development)

```python
# myproject/settings/development.py
class Development(Common):
    """Development with in-memory cache."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,
        }
    }
```

### Dummy Cache (Testing)

```python
# myproject/settings/test.py
class Test(Common):
    """Test configuration with dummy cache."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    # Or use in-memory for testing cache behavior
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     }
    # }
```

---

## Multiple Cache Configurations

### Named Caches

```python
class Common(Configuration):
    """Configuration with multiple named caches."""

    CACHES = {
        # Default cache for general use
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://localhost:6379/0',
            'KEY_PREFIX': 'default',
            'TIMEOUT': 300,
        },
        # Session cache with longer timeout
        'sessions': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://localhost:6379/1',
            'KEY_PREFIX': 'session',
            'TIMEOUT': 3600,  # 1 hour
        },
        # User permissions cache
        'permissions': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache_permissions',
            'KEY_PREFIX': 'perm',
            'TIMEOUT': 1800,  # 30 minutes
        },
        # API response cache with short timeout
        'api': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://localhost:6379/2',
            'KEY_PREFIX': 'api',
            'TIMEOUT': 60,  # 1 minute
        },
    }
```

---

## Cache Usage Patterns

### Basic Cache Operations

```python
from django.core.cache import cache

def get_user_profile(user_id: int) -> dict:
    """Get user profile with caching.

    Args:
        user_id: User ID

    Returns:
        User profile dict

    Raises:
        User.DoesNotExist: If user not found
    """
    # Generate cache key
    cache_key = f"user:{user_id}:profile"

    # Try cache first
    cached_profile = cache.get(cache_key)
    if cached_profile is not None:
        return cached_profile

    # Cache miss - fetch from database
    from myapp.models import User
    user = User.objects.select_related('profile').get(pk=user_id)
    profile = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'bio': user.profile.bio,
    }

    # Cache for 5 minutes
    cache.set(cache_key, profile, timeout=300)

    return profile


def update_user_profile(user_id: int, data: dict) -> None:
    """Update user profile and invalidate cache.

    Args:
        user_id: User ID
        data: Profile data to update
    """
    from myapp.models import User

    # Update database
    user = User.objects.get(pk=user_id)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()

    # Invalidate cache
    cache_key = f"user:{user_id}:profile"
    cache.delete(cache_key)
```

### Using Named Caches

```python
from django.core.cache import caches

def get_user_permissions(user_id: int) -> list[str]:
    """Get user permissions from permissions cache.

    Args:
        user_id: User ID

    Returns:
        List of permission strings
    """
    # Use named cache
    perm_cache = caches['permissions']

    cache_key = f"user:{user_id}:permissions"
    cached = perm_cache.get(cache_key)
    if cached is not None:
        return cached

    # Fetch permissions
    from myapp.models import User
    user = User.objects.get(pk=user_id)
    permissions = list(user.get_all_permissions())

    # Cache for 30 minutes
    perm_cache.set(cache_key, permissions, timeout=1800)

    return permissions
```

### Cache with Default Value

```python
from django.core.cache import cache

def get_site_config(key: str, default=None):
    """Get site configuration with caching.

    Args:
        key: Configuration key
        default: Default value if not found

    Returns:
        Configuration value
    """
    cache_key = f"config:{key}"

    # get() returns None if not found
    value = cache.get(cache_key)
    if value is not None:
        return value

    # Fetch from database
    from myapp.models import SiteConfig
    try:
        config = SiteConfig.objects.get(key=key)
        value = config.value
    except SiteConfig.DoesNotExist:
        value = default

    # Cache for 1 hour
    if value is not None:
        cache.set(cache_key, value, timeout=3600)

    return value
```

---

## Database Cache Deadlock Handling

### Problem: Cache Cleanup Deadlocks

**Issue:** Django's database cache cleans up expired entries during `get()` operations, which can cause deadlocks under high concurrency.

```python
# BAD ❌ - Can deadlock on DatabaseCache
from django.core.cache import cache

def get_cached_data(key: str):
    """Get cached data - may deadlock!"""
    return cache.get(key)  # Can deadlock during cleanup!
```

### Solution: Handle OperationalError

```python
# GOOD ✅ - Handle deadlock gracefully
from django.core.cache import cache
from django.db import OperationalError

def get_cached_data(key: str, default=None):
    """Get cached data with deadlock handling.

    Args:
        key: Cache key
        default: Default value if cache fails

    Returns:
        Cached value or default
    """
    try:
        value = cache.get(key)
        return value if value is not None else default
    except OperationalError:
        # Deadlock during cache cleanup - treat as cache miss
        return default


def safe_cache_get(cache_key: str, fetch_func, timeout: int = 300):
    """Safely get from cache with fallback function.

    Args:
        cache_key: Cache key
        fetch_func: Function to call on cache miss
        timeout: Cache timeout in seconds

    Returns:
        Cached or fetched value
    """
    try:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    except OperationalError:
        # Deadlock - continue to fetch fresh data
        pass

    # Cache miss or error - fetch fresh data
    value = fetch_func()

    # Try to cache (may also fail on deadlock)
    try:
        cache.set(cache_key, value, timeout=timeout)
    except OperationalError:
        # Failed to cache - not critical
        pass

    return value
```

---

## Cache Decorators

### cache_page Decorator (View Caching)

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# Cache for 5 minutes
@cache_page(60 * 5)
def my_view(request):
    """View cached for 5 minutes."""
    return render(request, 'template.html', {'data': expensive_operation()})


# Cache per user (vary on cookie)
@cache_page(60 * 5)
@vary_on_cookie
def user_specific_view(request):
    """Cache per user based on session cookie."""
    return render(request, 'profile.html', {'user': request.user})


# Cache with custom key function
from django.utils.cache import get_cache_key

def custom_cache_key(request):
    """Generate custom cache key."""
    return f"view:{request.user.id}:{request.path}"

@cache_page(60 * 5, key_prefix=custom_cache_key)
def custom_cached_view(request):
    """View with custom cache key."""
    return render(request, 'template.html')
```

### cache_control Decorator (HTTP Headers)

```python
from django.views.decorators.cache import cache_control

@cache_control(max_age=3600, public=True)
def public_view(request):
    """Cached by browser and CDN for 1 hour."""
    return render(request, 'public.html')


@cache_control(private=True, max_age=600)
def private_view(request):
    """Cached by browser only for 10 minutes."""
    return render(request, 'private.html')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def never_cache_view(request):
    """Never cached."""
    return render(request, 'sensitive.html')
```

### cached_property Decorator (Model Properties)

```python
from django.utils.functional import cached_property

class User(models.Model):
    """User model with cached properties."""

    name = models.CharField(max_length=255)
    email = models.EmailField()

    @cached_property
    def full_permissions(self) -> list[str]:
        """Get all user permissions (cached per instance).

        Computed once per instance, then cached for the lifetime
        of the instance in memory.

        Returns:
            List of permission strings
        """
        # Expensive operation - only computed once
        return list(self.get_all_permissions())

    @cached_property
    def post_count(self) -> int:
        """Get user's post count (cached per instance)."""
        return self.posts.count()


# Usage
user = User.objects.get(pk=1)
perms1 = user.full_permissions  # Computed
perms2 = user.full_permissions  # Cached (same result, no query)

# Refresh by deleting cached property
del user.full_permissions
perms3 = user.full_permissions  # Re-computed
```

---

## Template Fragment Caching

### Basic Fragment Caching

```html
{% load cache %}

<!-- Cache fragment for 5 minutes -->
{% cache 300 sidebar %}
    <div class="sidebar">
        <!-- Expensive template code -->
        {% for item in expensive_queryset %}
            <div>{{ item.name }}</div>
        {% endfor %}
    </div>
{% endcache %}
```

### Fragment Caching with Variables

```html
{% load cache %}

<!-- Cache per user -->
{% cache 300 sidebar request.user.id %}
    <div class="sidebar">
        Welcome, {{ request.user.name }}!
        <!-- User-specific content -->
    </div>
{% endcache %}

<!-- Cache per user and language -->
{% cache 300 navbar request.user.id request.LANGUAGE_CODE %}
    <nav>
        <!-- Localized navigation -->
    </nav>
{% endcache %}
```

### Using Named Caches in Templates

```html
{% load cache %}

<!-- Use named cache -->
{% cache 300 widget using='api' %}
    <div class="widget">
        <!-- API data cached separately -->
    </div>
{% endcache %}
```

---

## Cache Invalidation Patterns

### Time-Based Expiration (Simple)

```python
def cache_with_timeout(key: str, value, timeout: int = 300):
    """Cache with automatic expiration.

    Args:
        key: Cache key
        value: Value to cache
        timeout: Timeout in seconds
    """
    cache.set(key, value, timeout=timeout)
```

### Manual Invalidation (On Update)

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    """Invalidate user cache on save."""
    cache_key = f"user:{instance.id}:profile"
    cache.delete(cache_key)

    # Invalidate related caches
    cache.delete(f"user:{instance.id}:permissions")
    cache.delete(f"user:{instance.id}:posts")


@receiver(post_delete, sender=User)
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    """Invalidate user cache on delete."""
    cache_key = f"user:{instance.id}:profile"
    cache.delete(cache_key)
```

### Pattern-Based Invalidation

```python
def invalidate_user_caches(user_id: int):
    """Invalidate all caches for a user.

    Args:
        user_id: User ID
    """
    # Delete multiple related keys
    keys = [
        f"user:{user_id}:profile",
        f"user:{user_id}:permissions",
        f"user:{user_id}:posts",
        f"user:{user_id}:settings",
    ]
    cache.delete_many(keys)


def invalidate_pattern(pattern: str):
    """Invalidate all keys matching pattern.

    Note: Requires Redis backend with django-redis for pattern support.

    Args:
        pattern: Pattern to match (e.g., 'user:*:profile')
    """
    from django_redis import get_redis_connection

    conn = get_redis_connection("default")
    keys = conn.keys(pattern)
    if keys:
        conn.delete(*keys)
```

### Version-Based Invalidation

```python
def get_cache_version(namespace: str) -> int:
    """Get current cache version for namespace.

    Args:
        namespace: Cache namespace

    Returns:
        Current version number
    """
    version_key = f"cache_version:{namespace}"
    version = cache.get(version_key)
    if version is None:
        version = 1
        cache.set(version_key, version, timeout=None)
    return version


def increment_cache_version(namespace: str):
    """Increment cache version to invalidate all keys in namespace.

    Args:
        namespace: Cache namespace
    """
    version_key = f"cache_version:{namespace}"
    try:
        cache.incr(version_key)
    except ValueError:
        # Key doesn't exist or not an integer
        cache.set(version_key, 1, timeout=None)


def versioned_cache_get(namespace: str, key: str):
    """Get from cache with version.

    Args:
        namespace: Cache namespace
        key: Cache key

    Returns:
        Cached value or None
    """
    version = get_cache_version(namespace)
    versioned_key = f"{namespace}:v{version}:{key}"
    return cache.get(versioned_key)


def versioned_cache_set(namespace: str, key: str, value, timeout: int = 300):
    """Set cache with version.

    Args:
        namespace: Cache namespace
        key: Cache key
        value: Value to cache
        timeout: Timeout in seconds
    """
    version = get_cache_version(namespace)
    versioned_key = f"{namespace}:v{version}:{key}"
    cache.set(versioned_key, value, timeout=timeout)


# Usage
def get_user_profile(user_id: int):
    """Get user profile with versioned cache."""
    profile = versioned_cache_get('user_profiles', str(user_id))
    if profile is None:
        profile = fetch_user_profile(user_id)
        versioned_cache_set('user_profiles', str(user_id), profile)
    return profile


def invalidate_all_user_profiles():
    """Invalidate all user profile caches."""
    increment_cache_version('user_profiles')
```

---

## Testing Cache Behavior

### Test Cache Hit/Miss

```python
import pytest
from django.core.cache import cache

@pytest.mark.django_db
def test_get_user_profile__cache_hit__no_database_query():
    """Test cache hit avoids database query.

    Given: User profile in cache
    When: Getting user profile
    Then: No database query is made
    """
    # given: User in database
    user = UserFactory()

    # given: Profile in cache
    cache_key = f"user:{user.id}:profile"
    profile_data = {'id': user.id, 'name': user.name}
    cache.set(cache_key, profile_data, timeout=300)

    # when: Get profile
    from django.test.utils import CaptureQueriesContext
    from django.db import connection

    with CaptureQueriesContext(connection) as queries:
        result = get_user_profile(user.id)

    # then: No database queries (cache hit)
    assert len(queries) == 0
    assert result == profile_data


@pytest.mark.django_db
def test_get_user_profile__cache_miss__queries_database():
    """Test cache miss queries database.

    Given: User profile NOT in cache
    When: Getting user profile
    Then: Database is queried and result is cached
    """
    # given: User in database
    user = UserFactory()

    # given: NOT in cache
    cache_key = f"user:{user.id}:profile"
    cache.delete(cache_key)

    # when: Get profile
    from django.test.utils import CaptureQueriesContext
    from django.db import connection

    with CaptureQueriesContext(connection) as queries:
        result = get_user_profile(user.id)

    # then: Database queried
    assert len(queries) > 0
    assert result['id'] == user.id

    # then: Result cached
    cached = cache.get(cache_key)
    assert cached == result
```

### Test Cache Invalidation

```python
@pytest.mark.django_db
def test_update_user_profile__invalidates_cache():
    """Test updating user invalidates cache.

    Given: User profile in cache
    When: Updating user profile
    Then: Cache is invalidated
    """
    # given: User with cached profile
    user = UserFactory()
    cache_key = f"user:{user.id}:profile"
    old_profile = {'id': user.id, 'name': user.name}
    cache.set(cache_key, old_profile, timeout=300)

    # when: Update profile
    update_user_profile(user.id, {'name': 'Updated Name'})

    # then: Cache invalidated
    cached = cache.get(cache_key)
    assert cached is None
```

---

## Best Practices

1. **Use Redis in production** - Best performance and features
2. **Handle deadlocks** - Catch OperationalError with DatabaseCache
3. **Named caches** - Separate caches by use case
4. **Versioned invalidation** - Use version-based invalidation for bulk updates
5. **Cache keys** - Use clear, predictable key patterns
6. **Timeouts** - Set appropriate timeouts based on data volatility
7. **Invalidation** - Invalidate on updates, not just time-based
8. **Test caching** - Test both cache hits and misses
9. **Monitor cache** - Track hit rate, memory usage
10. **Don't over-cache** - Cache expensive operations, not everything

---

*Related: See `skill.md` for complete Django configuration guide*
