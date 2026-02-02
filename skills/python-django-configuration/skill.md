---
name: "Python Django Configuration"
description: "Django configuration patterns with django-configurations, environment management, and multi-tenancy"
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
  - configuration
  - settings
  - environment
  - multi-tenancy
files:
  - examples/django-configurations-guide.md: "Complete guide to django-configurations"
  - examples/environment-management.md: "Environment variable patterns and validation"
  - examples/multi-tenancy-patterns.md: "Multi-tenant configuration strategies"
  - examples/caching-patterns.md: "Django caching configuration and patterns"
---

# Python Django Configuration

## When to Use This Skill

Read this when:
- Setting up Django project configuration
- Managing environment-specific settings
- Implementing feature flags
- Configuring multi-tenant applications
- Setting up caching strategies
- Managing secrets and sensitive configuration

---

## Critical Principles

### 1. Use django-configurations (MANDATORY)

**ALWAYS** use `django-configurations` for environment-based settings:

```python
# BAD ❌ - Manual environment switching
import os

if os.getenv('ENVIRONMENT') == 'production':
    DEBUG = False
    # ... production settings
elif os.getenv('ENVIRONMENT') == 'staging':
    DEBUG = False
    # ... staging settings
else:
    DEBUG = True
    # ... development settings

# GOOD ✅ - django-configurations
from configurations import Configuration, values

class Common(Configuration):
    """Shared settings across all environments."""
    DEBUG = values.BooleanValue(False)
    SECRET_KEY = values.SecretValue()

class Development(Common):
    """Local development settings."""
    DEBUG = True

class Production(Common):
    """Production environment settings."""
    pass
```

### 2. Environment Variable Categories (CRITICAL)

**ALWAYS** categorize environment variables by requirement level:

```python
# Required - application fails if missing
ENVIRON_REQUIRED_KEYS = {
    "DATABASE_URL",
    "SECRET_KEY",
    "REDIS_URL",
}

# Optional - no default, but not mandatory
ENVIRON_ONLY_KEYS = {
    "SENDGRID_API_KEY",
    "SLACK_WEBHOOK_URL",
}

# Optional - has default, can be overridden
DEFAULT_ALLOWED_KEYS = {
    "LOG_LEVEL",
    "FEATURE_FLAG_NEW_UI",
}
```

### 3. Never Hardcode Secrets (MANDATORY)

**NEVER** commit secrets to version control:

```python
# BAD ❌ - Hardcoded secrets
SECRET_KEY = "django-insecure-hardcoded-secret-key"
DATABASE_PASSWORD = "mypassword123"

# GOOD ✅ - Environment variables
SECRET_KEY = values.SecretValue()
DATABASE_URL = values.DatabaseURLValue()
```

---

## django-configurations Setup

### Installation

```bash
pip install django-configurations python-dotenv
# or
poetry add django-configurations python-dotenv
```

### Project Structure

```
myproject/
├── myproject/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── common.py      # Shared settings
│   │   ├── development.py # Dev settings
│   │   ├── staging.py     # Staging settings
│   │   ├── production.py  # Production settings
│   │   └── test.py        # Test settings
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── .env                    # Local environment variables (DON'T COMMIT)
├── .env.example           # Template (DO COMMIT)
└── pyproject.toml
```

### Common Settings (Base Configuration)

```python
# myproject/settings/common.py
"""Common settings shared across all environments."""
from configurations import Configuration, values
from pathlib import Path
import os

class Common(Configuration):
    """Base configuration class."""

    # Build paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Security settings
    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = values.ListValue([])

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Third-party apps
        'rest_framework',
        # Local apps
        'myapp',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'myproject.urls'
    WSGI_APPLICATION = 'myproject.wsgi.application'

    # Database
    DATABASES = values.DatabaseURLValue(
        'postgresql://user:pass@localhost/dbname'
    )

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    # Static files
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Feature flags (with defaults)
    ENABLE_NEW_UI = values.BooleanValue(False, environ_prefix=None)
    ENABLE_BETA_FEATURES = values.BooleanValue(False, environ_prefix=None)

    # External services
    SENDGRID_API_KEY = values.Value(None, environ_prefix=None)
    SLACK_WEBHOOK_URL = values.Value(None, environ_prefix=None)

    @classmethod
    def pre_setup(cls):
        """Hook called before configuration is set up.

        Use for:
        - Environment variable validation
        - Loading .env files
        - Setting up logging before Django loads
        """
        super().pre_setup()

        # Load .env file in development
        from dotenv import load_dotenv
        env_file = cls.BASE_DIR / '.env'
        if env_file.exists():
            load_dotenv(env_file)

    @classmethod
    def post_setup(cls):
        """Hook called after configuration is set up.

        Use for:
        - Validating configuration consistency
        - Setting up SDK clients
        - Initializing third-party services
        """
        super().post_setup()

        # Validate required environment variables
        cls.validate_required_env_vars()

    @classmethod
    def validate_required_env_vars(cls):
        """Validate required environment variables are set."""
        REQUIRED_KEYS = {
            'SECRET_KEY',
            'DATABASE_URL',
        }

        missing = []
        for key in REQUIRED_KEYS:
            if not os.getenv(key):
                missing.append(key)

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
```

### Development Settings

```python
# myproject/settings/development.py
"""Development environment settings."""
from .common import Common

class Development(Common):
    """Configuration for local development."""

    DEBUG = True

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

    # Enable Django Debug Toolbar
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = ['127.0.0.1']

    # Feature flags (enabled in dev)
    ENABLE_NEW_UI = True
    ENABLE_BETA_FEATURES = True

    # Development-specific cache (in-memory)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

    # Email backend (console for development)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
```

### Staging Settings

```python
# myproject/settings/staging.py
"""Staging environment settings."""
from .common import Common
from configurations import values

class Staging(Common):
    """Configuration for staging/QA environment."""

    DEBUG = False

    ALLOWED_HOSTS = values.ListValue(['staging.example.com'])

    # Security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Cache (Redis)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': values.Value(
                'redis://localhost:6379/0',
                environ_prefix=None,
                environ_name='REDIS_URL',
            ),
        }
    }

    # JSON logging for structured logs
    LOG_JSON = True

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }

    @classmethod
    def pre_setup(cls):
        """Enforce required environment variables for staging."""
        super().pre_setup()

        import os
        required = ['DATABASE_URL', 'REDIS_URL', 'SECRET_KEY']
        missing = [key for key in required if not os.getenv(key)]

        if missing:
            raise ValueError(
                f"Staging requires: {', '.join(missing)}"
            )
```

### Production Settings

```python
# myproject/settings/production.py
"""Production environment settings."""
from .staging import Staging
from configurations import values

class Production(Staging):
    """Configuration for production environment.

    Inherits from Staging to ensure staging tests production config.
    """

    ALLOWED_HOSTS = values.ListValue(['example.com', 'www.example.com'])

    # Additional security headers
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Database connection pooling
    DATABASES = values.DatabaseURLValue(
        conn_max_age=600,  # Connection pooling
    )

    # Feature flags (conservative in production)
    ENABLE_NEW_UI = values.BooleanValue(False, environ_prefix=None)
    ENABLE_BETA_FEATURES = False  # Never enabled in production

    @classmethod
    def post_setup(cls):
        """Production-specific post-setup validation."""
        super().post_setup()

        # Ensure critical settings are production-ready
        if cls.DEBUG:
            raise ValueError("DEBUG must be False in production")

        if not cls.SECRET_KEY or cls.SECRET_KEY == 'change-me':
            raise ValueError("SECRET_KEY must be set in production")
```

### Test Settings

```python
# myproject/settings/test.py
"""Test environment settings."""
from .common import Common

class Test(Common):
    """Configuration for running tests."""

    DEBUG = False

    # In-memory database for speed
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    # Or use test PostgreSQL container
    # DATABASES = values.DatabaseURLValue(
    #     'postgresql://test_user:test_password@localhost:5433/test_db'
    # )

    # Fast password hashing for tests
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    # Disable migrations for speed
    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    # MIGRATION_MODULES = DisableMigrations()  # Uncomment for speed

    # In-memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    # Email backend
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    # Feature flags (all enabled for testing)
    ENABLE_NEW_UI = True
    ENABLE_BETA_FEATURES = True
```

---

## Environment Variable Management

### .env File (Development)

```bash
# .env (DON'T COMMIT - add to .gitignore)

# Django settings
DJANGO_SETTINGS_MODULE=myproject.settings.development
DJANGO_CONFIGURATION=Development

# Security
SECRET_KEY=django-insecure-dev-key-change-me

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myproject_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Feature flags
ENABLE_NEW_UI=true
ENABLE_BETA_FEATURES=true

# External services (optional in dev)
SENDGRID_API_KEY=SG.xxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
```

### .env.example (Template - DO COMMIT)

```bash
# .env.example

# Django settings
DJANGO_SETTINGS_MODULE=myproject.settings.development
DJANGO_CONFIGURATION=Development

# Security (REQUIRED)
SECRET_KEY=change-me

# Database (REQUIRED)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis (OPTIONAL)
REDIS_URL=redis://localhost:6379/0

# Feature flags (OPTIONAL - defaults to false)
ENABLE_NEW_UI=false
ENABLE_BETA_FEATURES=false

# External services (OPTIONAL)
SENDGRID_API_KEY=
SLACK_WEBHOOK_URL=
```

### Environment Variable Validation

```python
# myproject/settings/common.py
from typing import Set
import os

class Common(Configuration):
    """Base configuration with environment validation."""

    # Define environment variable categories
    ENVIRON_REQUIRED_KEYS: Set[str] = {
        'SECRET_KEY',
        'DATABASE_URL',
    }

    ENVIRON_ONLY_KEYS: Set[str] = {
        'SENDGRID_API_KEY',
        'SLACK_WEBHOOK_URL',
        'STRIPE_API_KEY',
    }

    DEFAULT_ALLOWED_KEYS: Set[str] = {
        'LOG_LEVEL',
        'ENABLE_NEW_UI',
        'ENABLE_BETA_FEATURES',
    }

    @classmethod
    def pre_setup(cls):
        """Validate environment variables before setup."""
        super().pre_setup()

        # Check required keys
        missing_required = []
        for key in cls.ENVIRON_REQUIRED_KEYS:
            if not os.getenv(key):
                missing_required.append(key)

        if missing_required:
            raise ValueError(
                f"Missing required environment variables: "
                f"{', '.join(missing_required)}"
            )

        # Check environ-only keys don't have defaults
        for key in cls.ENVIRON_ONLY_KEYS:
            value = os.getenv(key)
            if value and value.startswith('default-'):
                raise ValueError(
                    f"{key} should not have default value in code. "
                    f"Either make it required or allow defaults."
                )
```

---

## Multi-Tenancy Configuration

### Brand-Based Multi-Tenancy

```python
# myproject/settings/common.py
from configurations import Configuration, values
import os

class Common(Configuration):
    """Base configuration with multi-tenancy support."""

    # Brand configuration
    BRAND = values.Value(
        os.getenv('BRAND', 'default'),
        environ_prefix=None,
    )

    # Brand-specific default values
    _BRAND_CONFIG = {
        'clover': {
            'BASE_URL': 'https://cloverassistant.com',
            'EMAIL_SENDER': 'support@cloverhealth.com',
            'PRIMARY_COLOR': '#00A651',
            'LOGO_URL': 'https://cdn.cloverhealth.com/logo.png',
        },
        'counterpart': {
            'BASE_URL': 'https://counterparthealth.com',
            'EMAIL_SENDER': 'support@counterparthealth.com',
            'PRIMARY_COLOR': '#0066CC',
            'LOGO_URL': 'https://cdn.counterparthealth.com/logo.png',
        },
        'default': {
            'BASE_URL': 'http://localhost:8000',
            'EMAIL_SENDER': 'noreply@example.com',
            'PRIMARY_COLOR': '#333333',
            'LOGO_URL': '',
        },
    }

    @classmethod
    def setup(cls):
        """Set up brand-specific configuration."""
        super().setup()

        # Get brand configuration
        brand = cls.BRAND.value
        if brand not in cls._BRAND_CONFIG:
            raise ValueError(
                f"Unknown brand: {brand}. "
                f"Valid brands: {', '.join(cls._BRAND_CONFIG.keys())}"
            )

        brand_config = cls._BRAND_CONFIG[brand]

        # Apply brand-specific settings
        cls.BASE_URL = values.Value(
            brand_config['BASE_URL'],
            environ_prefix=None,
        ).value

        cls.EMAIL_SENDER = values.Value(
            brand_config['EMAIL_SENDER'],
            environ_prefix=None,
        ).value

        cls.PRIMARY_COLOR = brand_config['PRIMARY_COLOR']
        cls.LOGO_URL = brand_config['LOGO_URL']
```

### Usage

```bash
# Run with different brands
BRAND=clover python manage.py runserver
BRAND=counterpart python manage.py runserver
```

---

## Feature Flags

### Boolean Feature Flags

```python
# myproject/settings/common.py
class Common(Configuration):
    """Configuration with feature flags."""

    # Feature flags with defaults
    ENABLE_NEW_UI = values.BooleanValue(False, environ_prefix=None)
    ENABLE_BETA_FEATURES = values.BooleanValue(False, environ_prefix=None)
    ENABLE_EXPERIMENTAL_API = values.BooleanValue(False, environ_prefix=None)

    # Numeric feature flags
    MAX_UPLOAD_SIZE_MB = values.IntegerValue(10, environ_prefix=None)
    API_RATE_LIMIT = values.IntegerValue(100, environ_prefix=None)

# Usage in code
from django.conf import settings

def my_view(request):
    if settings.ENABLE_NEW_UI:
        return render(request, 'new_ui.html')
    else:
        return render(request, 'old_ui.html')
```

### Testing Feature Flags

```python
# tests/test_features.py
import pytest
from django.test import override_settings

@override_settings(ENABLE_NEW_UI=True)
def test_new_ui__when_enabled__renders_new_template():
    """Test new UI is used when feature flag is enabled."""
    # given/when: Make request with feature enabled
    response = client.get('/dashboard/')

    # then: New UI template is used
    assert 'new_ui.html' in [t.name for t in response.templates]


@override_settings(ENABLE_NEW_UI=False)
def test_new_ui__when_disabled__renders_old_template():
    """Test old UI is used when feature flag is disabled."""
    # given/when: Make request with feature disabled
    response = client.get('/dashboard/')

    # then: Old UI template is used
    assert 'old_ui.html' in [t.name for t in response.templates]
```

---

## Caching Configuration

### Redis Cache (Production/Staging)

```python
# myproject/settings/production.py
class Production(Staging):
    """Production configuration with Redis caching."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': values.Value(
                environ_name='REDIS_URL',
                environ_prefix=None,
            ),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                },
            },
            'KEY_PREFIX': 'myproject',
            'TIMEOUT': 300,  # 5 minutes default
        },
        'user_sessions': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': values.Value(
                environ_name='REDIS_URL',
                environ_prefix=None,
            ),
            'KEY_PREFIX': 'sessions',
            'TIMEOUT': 3600,  # 1 hour
        },
    }
```

### Database Cache (Alternative)

```python
# myproject/settings/common.py
class Common(Configuration):
    """Configuration with database caching."""

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache',
        },
        'user_permissions': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache_permissions',
        },
    }
```

### Cache Usage

```python
from django.core.cache import cache, caches
from django.db import OperationalError

def get_user_permissions(user_id: int) -> list[str]:
    """Get user permissions with caching.

    Args:
        user_id: User ID

    Returns:
        List of permission strings

    Raises:
        User.DoesNotExist: If user not found
    """
    cache_key = f"user:{user_id}:permissions"

    # Try cache first
    try:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    except OperationalError:
        # Database cache deadlock - treat as miss
        pass

    # Cache miss - fetch from database
    from myapp.models import User
    user = User.objects.get(pk=user_id)
    permissions = list(user.get_all_permissions())

    # Cache for 1 hour
    cache.set(cache_key, permissions, timeout=3600)

    return permissions


def use_named_cache():
    """Use specific named cache."""
    user_cache = caches['user_sessions']
    user_cache.set('user:123:session', session_data, timeout=3600)
    session = user_cache.get('user:123:session')
```

---

## Integration with Other Skills

### From python-testing-excellence

- Use `@override_settings` to test different configurations
- Test feature flags with both enabled/disabled states
- Use Docker for testing with real Redis/PostgreSQL

### From python-clean-implementation

- Type hints for all configuration methods
- Docstrings explaining configuration purpose
- Validate configuration in `pre_setup`/`post_setup`

### From python-django-models

- Database configuration with connection pooling
- Cache configuration for query optimization
- Multi-database setup for read replicas

---

## Common Pitfalls

### Pitfall 1: Hardcoding Configuration

```python
# BAD ❌ - Hardcoded config
DEBUG = True
SECRET_KEY = "insecure-key"

# GOOD ✅ - Environment-based config
DEBUG = values.BooleanValue(False)
SECRET_KEY = values.SecretValue()
```

### Pitfall 2: Missing Environment Variables

```python
# BAD ❌ - No validation
DATABASE_URL = os.getenv('DATABASE_URL')

# GOOD ✅ - Validated in pre_setup
@classmethod
def pre_setup(cls):
    super().pre_setup()
    if not os.getenv('DATABASE_URL'):
        raise ValueError("DATABASE_URL is required")
```

### Pitfall 3: Inconsistent Staging/Production

```python
# BAD ❌ - Staging and Production diverge
class Staging(Common):
    MIDDLEWARE = [...]  # Different from production

class Production(Common):
    MIDDLEWARE = [...]  # Different from staging

# GOOD ✅ - Production inherits from Staging
class Staging(Common):
    MIDDLEWARE = [...]

class Production(Staging):
    # Inherits Staging config, overrides as needed
    pass
```

### Pitfall 4: Feature Flags Without Tests

```python
# BAD ❌ - Feature flag without tests
if settings.ENABLE_NEW_FEATURE:
    do_new_thing()

# GOOD ✅ - Test both states
@override_settings(ENABLE_NEW_FEATURE=True)
def test_feature_enabled():
    assert new_behavior_works()

@override_settings(ENABLE_NEW_FEATURE=False)
def test_feature_disabled():
    assert old_behavior_works()
```

---

## Best Practices

1. **Use django-configurations** - Don't reinvent configuration management
2. **Categorize env vars** - Required, optional, default-allowed
3. **Validate early** - Fail fast in `pre_setup` if config is invalid
4. **Production inherits Staging** - Ensures staging tests production config
5. **Test feature flags** - Test both enabled and disabled states
6. **Never commit secrets** - Use environment variables
7. **Document env vars** - Maintain `.env.example` template
8. **Use type hints** - Annotate configuration methods
9. **Multi-tenancy** - Use BRAND pattern for tenant configuration
10. **Cache wisely** - Handle cache failures gracefully

---

## Learning Log

### 2026-02-02: Python Django Configuration Skill Created

**Issue:** Need comprehensive Django configuration patterns.

**Learning:** Created Django configuration skill covering:
- django-configurations for environment-based settings
- Environment variable categorization (required, optional, default-allowed)
- Multi-tenancy with BRAND pattern
- Feature flag patterns
- Caching configuration (Redis, Database)
- Configuration validation with pre_setup/post_setup hooks
- Production inheriting from Staging pattern

**Adaptation:** Integrated with existing Python skills:
- Type hints and docstrings from python-clean-implementation
- Testing patterns from python-testing-excellence
- Integration with python-django-models for database config

**New Standard:** All Django projects must use django-configurations.

---

## Examples

See `examples/` directory for detailed guides:

- `django-configurations-guide.md` - Complete guide to django-configurations
- `environment-management.md` - Environment variable patterns
- `multi-tenancy-patterns.md` - Multi-tenant configuration
- `caching-patterns.md` - Django caching strategies

## Related Skills

- [Python Django Models](../python-django-models/skill.md) - For model configuration
- [Python Testing Excellence](../python-testing-excellence/skill.md) - For testing config
- [Python Directory and Configuration](../python-directory-and-configuration/skill.md) - For project setup

---

*Created: 2026-02-02*
*Version: 1.0*
