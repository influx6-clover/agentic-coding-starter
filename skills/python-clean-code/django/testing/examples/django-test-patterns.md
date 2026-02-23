# Django-Specific Test Patterns

This guide covers Django-specific testing patterns and utilities.

---

## Settings Override

### Basic Override

```python
from django.test import override_settings

@override_settings(DEBUG=True)
def test_debug_view__debug_enabled__shows_info():
    """Test debug view when DEBUG is True."""
    from django.conf import settings
    assert settings.DEBUG is True
```

### Multiple Settings

```python
@override_settings(
    FEATURE_FLAG_NEW_UI=True,
    MAX_UPLOAD_SIZE_MB=100,
    ALLOWED_HOSTS=['testserver', 'localhost'],
)
def test_feature_with_settings():
    """Test with multiple setting overrides."""
    pass
```

---

## Testing N+1 Queries

### Query Count Testing

```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

@pytest.mark.django_db
def test_get_posts__optimized__no_n_plus_one():
    """Test posts query has no N+1 problem."""
    # given: 10 posts with authors
    PostFactory.create_batch(10)

    # when: Fetch posts with select_related
    with CaptureQueriesContext(connection) as queries:
        posts = Post.objects.select_related('author').all()
        for post in posts:
            _ = post.author.name

    # then: Only 1 query (with JOIN)
    assert len(queries.captured_queries) == 1
```

---

## Testing Transactions

```python
from django.db import transaction

@pytest.mark.django_db(transaction=True)
def test_atomic_operation__error__rolls_back():
    """Test transaction rollback on error."""
    # given
    initial_count = User.objects.count()

    # when: Transaction with error
    with pytest.raises(ValueError):
        with transaction.atomic():
            UserFactory()
            raise ValueError('Rollback')

    # then: No user created (rolled back)
    assert User.objects.count() == initial_count
```

---

## Testing Middleware

```python
@pytest.mark.django_db
def test_auth_middleware__no_token__returns_401(client):
    """Test auth middleware rejects unauthenticated requests."""
    response = client.get('/api/protected/')
    assert response.status_code == 401
```

---

## Testing Management Commands

```python
from django.core.management import call_command
from io import StringIO

@pytest.mark.django_db
def test_cleanup_command__removes_old_records():
    """Test cleanup management command."""
    # given: Old and new records
    old = RecordFactory(created_at=date(2020, 1, 1))
    new = RecordFactory(created_at=date(2024, 1, 1))

    # when: Run cleanup command
    out = StringIO()
    call_command('cleanup', '--days=365', stdout=out)

    # then: Old record deleted, new preserved
    assert not Record.objects.filter(pk=old.pk).exists()
    assert Record.objects.filter(pk=new.pk).exists()
```

---

## Testing Signals

```python
from django.db.models.signals import post_save

@pytest.mark.django_db
def test_post_save_signal__user_creation__sends_email(mocker):
    """Test post_save signal sends welcome email."""
    # given: Mock email
    mock_send = mocker.patch('django.core.mail.send_mail')

    # when: Create user (triggers signal)
    user = UserFactory(email='test@example.com')

    # then: Email sent
    mock_send.assert_called_once()
    args, kwargs = mock_send.call_args
    assert 'Welcome' in args[0]  # Subject
    assert user.email in args[3]  # Recipient
```

---

## Testing with freezegun

```python
from freezegun import freeze_time
from datetime import datetime
from django.utils import timezone

@freeze_time('2024-01-15 12:00:00+00:00')
@pytest.mark.django_db
def test_create_subscription__frozen_time__uses_fixed_date():
    """Test subscription uses frozen time."""
    # given: Frozen time
    expected = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

    # when
    sub = SubscriptionFactory()

    # then
    assert sub.start_date == expected.date()
```

---

## Testing Caching

```python
from django.core.cache import cache

@pytest.mark.django_db
def test_get_user_profile__cache_hit__no_query():
    """Test cached profile doesn't query database."""
    # given: User and cached profile
    user = UserFactory()
    cache_key = f'user:{user.pk}:profile'
    cache.set(cache_key, {'name': user.name})

    # when
    with CaptureQueriesContext(connection) as queries:
        profile = get_user_profile(user.pk)

    # then: No database query
    assert len(queries.captured_queries) == 0
    assert profile['name'] == user.name


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test."""
    cache.clear()
    yield
    cache.clear()
```

---

## Testing File Uploads

```python
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_upload_avatar__valid_image__saves(client):
    """Test avatar upload."""
    # given: User and image file
    user = UserFactory()
    client.force_login(user)

    image_content = b'fake-image-content'
    image = SimpleUploadedFile(
        'avatar.jpg',
        image_content,
        content_type='image/jpeg'
    )

    # when: Upload
    response = client.post('/api/upload-avatar/', {'avatar': image})

    # then
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.avatar is not None
```

---

## Best Practices

1. **@override_settings** - Test configuration variations
2. **CaptureQueriesContext** - Catch N+1 queries
3. **transaction=True** - Test transaction behavior
4. **freezegun** - Deterministic time testing
5. **Mock signals** - Test signal handlers
6. **Clear cache** - Isolate cache tests
7. **Client fixture** - Test views and middleware

---

*Related: See `skill.md` for complete Django testing guide*
