# Django Configurations - Complete Guide

This guide covers using `django-configurations` for managing Django settings across environments.

---

## Why django-configurations?

**Problems with traditional Django settings:**
- Hard to manage multiple environments (dev, staging, production)
- Environment-specific settings scattered across files
- No built-in validation for required settings
- Manual environment switching prone to errors

**Benefits of django-configurations:**
- Class-based configuration hierarchy
- Environment variable integration with type safety
- Validation hooks (`pre_setup`, `post_setup`)
- Clear inheritance chain (Development → Staging → Production)
- Built-in values classes for common types

---

## Installation

```bash
pip install django-configurations python-dotenv
# or
poetry add django-configurations python-dotenv
```

---

## Basic Setup

### 1. Convert settings.py to Configuration Classes

**Before (traditional settings.py):**

```python
# settings.py
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mydb'),
        'USER': os.getenv('DB_USER', 'user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**After (with django-configurations):**

```python
# settings.py
from configurations import Configuration, values

class Development(Configuration):
    """Local development settings."""
    DEBUG = True
    SECRET_KEY = values.SecretValue()
    DATABASES = values.DatabaseURLValue(
        'postgresql://user:password@localhost:5432/mydb'
    )

class Production(Configuration):
    """Production settings."""
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    DATABASES = values.DatabaseURLValue()
```

### 2. Update manage.py

```python
# manage.py
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Set the settings module and configuration class
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

### 3. Update wsgi.py

```python
# wsgi.py
import os
from configurations.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

application = get_wsgi_application()
```

### 4. Update asgi.py (for async)

```python
# asgi.py
import os
from configurations.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

application = get_asgi_application()
```

---

## Configuration Hierarchy

### Pattern: Common → Development/Staging/Production

```python
# myproject/settings/common.py
from configurations import Configuration, values
from pathlib import Path

class Common(Configuration):
    """Base configuration shared across all environments."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Core Django settings
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
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

    # Security
    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = values.ListValue([])

    # Database
    DATABASES = values.DatabaseURLValue()

    # Static files
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True


# myproject/settings/development.py
from .common import Common

class Development(Common):
    """Local development configuration."""

    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    # Use console email backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# myproject/settings/staging.py
from .common import Common

class Staging(Common):
    """Staging/QA configuration."""

    DEBUG = False
    ALLOWED_HOSTS = values.ListValue(['staging.example.com'])

    # Security headers
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# myproject/settings/production.py
from .staging import Staging

class Production(Staging):
    """Production configuration.

    Inherits from Staging to ensure staging environment
    tests production configuration.
    """

    ALLOWED_HOSTS = values.ListValue(['example.com', 'www.example.com'])

    # Additional production security
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## Values Classes

### Built-in Values

```python
from configurations import values

class MyConfig(Configuration):
    """Configuration using various value types."""

    # Boolean values
    DEBUG = values.BooleanValue(False)  # Default: False
    ENABLE_FEATURE = values.BooleanValue(True, environ_name='FEATURE_FLAG')

    # String values
    SECRET_KEY = values.SecretValue()  # Must be in environment
    API_KEY = values.Value('default-key')  # Has default

    # Integer values
    MAX_CONNECTIONS = values.IntegerValue(100)
    PORT = values.IntegerValue(8000, environ_name='APP_PORT')

    # Float values
    CACHE_TIMEOUT = values.FloatValue(30.5)

    # List values
    ALLOWED_HOSTS = values.ListValue(['localhost'])
    INTERNAL_IPS = values.ListValue(['127.0.0.1'], separator=',')

    # Tuple values
    ADMINS = values.TupleValue((('Admin', 'admin@example.com'),))

    # Dict values
    LOGGING_CONFIG = values.DictValue({'version': 1})

    # Database URL
    DATABASES = values.DatabaseURLValue(
        'postgresql://user:pass@localhost/db'
    )

    # Email URL
    EMAIL_CONFIG = values.EmailURLValue(
        'smtp://user:pass@smtp.gmail.com:587/?tls=True'
    )

    # Cache URL
    CACHES = values.CacheURLValue('redis://localhost:6379/0')

    # Path values
    MEDIA_ROOT = values.PathValue('/var/www/media')

    # JSON values
    FEATURE_FLAGS = values.JSONValue('{"new_ui": false}')
```

### Custom environ_name and environ_prefix

```python
class MyConfig(Configuration):
    """Configuration with custom environment variable names."""

    # Use custom environment variable name
    API_KEY = values.Value(
        'default',
        environ_name='CUSTOM_API_KEY',  # Reads from CUSTOM_API_KEY
    )

    # Disable automatic prefix
    FEATURE_FLAG = values.BooleanValue(
        False,
        environ_prefix=None,  # Reads from FEATURE_FLAG (not DJANGO_FEATURE_FLAG)
    )

    # Custom prefix
    APP_VERSION = values.Value(
        '1.0.0',
        environ_prefix='MYAPP',  # Reads from MYAPP_APP_VERSION
    )
```

---

## Configuration Hooks

### pre_setup Hook

**Called BEFORE settings are loaded.**

Use for:
- Loading .env files
- Environment variable validation
- Setting up logging

```python
class Common(Configuration):
    """Configuration with pre_setup hook."""

    @classmethod
    def pre_setup(cls):
        """Hook called before configuration setup.

        Use for:
        - Loading .env files
        - Validating required environment variables
        - Early initialization
        """
        super().pre_setup()

        # Load .env file
        from dotenv import load_dotenv
        env_file = cls.BASE_DIR / '.env'
        if env_file.exists():
            load_dotenv(env_file)

        # Validate required environment variables
        import os
        required = ['SECRET_KEY', 'DATABASE_URL']
        missing = [key for key in required if not os.getenv(key)]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        # Set up early logging
        import logging
        logging.basicConfig(level=logging.INFO)
```

### post_setup Hook

**Called AFTER settings are loaded.**

Use for:
- Configuration validation
- Initializing SDK clients
- Cross-setting validation

```python
class Common(Configuration):
    """Configuration with post_setup hook."""

    @classmethod
    def post_setup(cls):
        """Hook called after configuration setup.

        Use for:
        - Validating configuration consistency
        - Initializing SDK clients
        - Post-configuration initialization
        """
        super().post_setup()

        # Validate configuration consistency
        if cls.DEBUG and 'production' in cls.ALLOWED_HOSTS[0]:
            raise ValueError("DEBUG should not be True in production")

        # Initialize SDK clients
        if cls.SENDGRID_API_KEY:
            from sendgrid import SendGridAPIClient
            cls.sendgrid_client = SendGridAPIClient(cls.SENDGRID_API_KEY)

        # Log configuration status
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Configuration loaded: {cls.__name__}")
        logger.info(f"DEBUG: {cls.DEBUG}")
        logger.info(f"ALLOWED_HOSTS: {cls.ALLOWED_HOSTS}")
```

### setup Hook

**Override complete setup process.**

```python
class Common(Configuration):
    """Configuration with custom setup."""

    @classmethod
    def setup(cls):
        """Override complete setup process.

        Only use when you need full control over setup.
        Most cases should use pre_setup/post_setup instead.
        """
        super().setup()

        # Custom setup logic
        cls.CUSTOM_SETTING = cls.calculate_custom_value()

    @classmethod
    def calculate_custom_value(cls):
        """Calculate custom configuration value."""
        return "custom-value"
```

---

## Advanced Patterns

### Dynamic Configuration

```python
class Common(Configuration):
    """Configuration with dynamic values."""

    @classmethod
    def setup(cls):
        """Set up dynamic configuration."""
        super().setup()

        # Dynamic INSTALLED_APPS
        if cls.ENABLE_DEBUG_TOOLBAR:
            cls.INSTALLED_APPS = cls.INSTALLED_APPS + ['debug_toolbar']
            cls.MIDDLEWARE = cls.MIDDLEWARE + [
                'debug_toolbar.middleware.DebugToolbarMiddleware'
            ]

        # Dynamic DATABASES based on environment
        if cls.USE_REPLICA:
            cls.DATABASES['replica'] = {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': cls.REPLICA_HOST,
                'NAME': cls.REPLICA_DB_NAME,
            }
```

### Conditional Configuration

```python
class Staging(Common):
    """Staging configuration with conditional settings."""

    ENABLE_SENTRY = values.BooleanValue(False)
    SENTRY_DSN = values.Value(None)

    @classmethod
    def post_setup(cls):
        """Set up conditional Sentry integration."""
        super().post_setup()

        if cls.ENABLE_SENTRY and cls.SENTRY_DSN:
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration

            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                integrations=[DjangoIntegration()],
                environment='staging',
            )
```

### Nested Configuration

```python
class Common(Configuration):
    """Configuration with nested settings."""

    # REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': values.IntegerValue(100, environ_prefix=None),
    }

    @classmethod
    def post_setup(cls):
        """Update nested settings from environment."""
        super().post_setup()

        # Update PAGE_SIZE from environment
        import os
        page_size = os.getenv('PAGE_SIZE')
        if page_size:
            cls.REST_FRAMEWORK['PAGE_SIZE'] = int(page_size)
```

---

## Testing Configuration

### Test-Specific Configuration

```python
# myproject/settings/test.py
from .common import Common

class Test(Common):
    """Configuration for running tests."""

    DEBUG = False

    # Fast password hashing
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    # In-memory database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    # In-memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    # Console email
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    # Disable migrations for speed
    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
```

### pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "myproject.settings"
DJANGO_CONFIGURATION = "Test"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Using @override_settings

```python
# tests/test_features.py
import pytest
from django.test import override_settings

@override_settings(ENABLE_NEW_FEATURE=True)
def test_feature_enabled():
    """Test behavior with feature enabled."""
    from django.conf import settings
    assert settings.ENABLE_NEW_FEATURE is True
    # Test feature behavior


@override_settings(
    DEBUG=True,
    ALLOWED_HOSTS=['testserver'],
)
def test_multiple_settings():
    """Test with multiple setting overrides."""
    from django.conf import settings
    assert settings.DEBUG is True
    assert 'testserver' in settings.ALLOWED_HOSTS
```

---

## Common Patterns

### Pattern 1: Environment-Specific Apps

```python
class Common(Configuration):
    """Base configuration."""
    INSTALLED_APPS = [
        'django.contrib.admin',
        # ... common apps
    ]


class Development(Common):
    """Development with debug toolbar."""
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
        'django_extensions',
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


class Production(Common):
    """Production without debug tools."""
    INSTALLED_APPS = Common.INSTALLED_APPS
    # No debug toolbar in production
```

### Pattern 2: Secrets Management

```python
class Common(Configuration):
    """Configuration with secrets management."""

    # Required secrets
    SECRET_KEY = values.SecretValue()
    DATABASE_URL = values.DatabaseURLValue()

    # Optional secrets (with fallback)
    SENDGRID_API_KEY = values.Value(None, environ_prefix=None)
    STRIPE_API_KEY = values.Value(None, environ_prefix=None)

    @classmethod
    def post_setup(cls):
        """Validate secrets based on environment."""
        super().post_setup()

        # In production, require optional secrets
        if not cls.DEBUG:
            if not cls.SENDGRID_API_KEY:
                raise ValueError("SENDGRID_API_KEY required in production")
```

### Pattern 3: Multi-Database Configuration

```python
class Common(Configuration):
    """Configuration with multiple databases."""

    DATABASES = {
        'default': values.DatabaseURLValue(),
    }

    # Optional read replica
    USE_REPLICA = values.BooleanValue(False, environ_prefix=None)
    REPLICA_URL = values.DatabaseURLValue(
        None,
        environ_name='REPLICA_DATABASE_URL',
    )

    @classmethod
    def setup(cls):
        """Set up database routing."""
        super().setup()

        if cls.USE_REPLICA and cls.REPLICA_URL:
            cls.DATABASES['replica'] = cls.REPLICA_URL

            # Set up database router
            cls.DATABASE_ROUTERS = [
                'myproject.routers.ReplicaRouter',
            ]
```

---

## Best Practices

1. **Use class inheritance** - Common → Staging → Production
2. **Validate early** - Use `pre_setup` for validation
3. **Keep secrets in env** - Never commit secrets
4. **Test configuration** - Use `@override_settings` in tests
5. **Production inherits Staging** - Ensures staging tests prod config
6. **Document env vars** - Maintain `.env.example`
7. **Use type-safe values** - BooleanValue, IntegerValue, etc.
8. **Fail fast** - Validate required settings in hooks
9. **Log configuration** - Log which config is active
10. **Keep it DRY** - Extract common settings to base class

---

*Related: See `skill.md` for complete Django configuration guide*
