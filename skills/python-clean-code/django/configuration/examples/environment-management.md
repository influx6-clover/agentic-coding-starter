# Environment Variable Management

This guide covers patterns for managing environment variables in Django projects.

---

## Environment Variable Categories

**CRITICAL:** Always categorize environment variables by requirement level.

### Three Categories

```python
# myproject/settings/common.py
from configurations import Configuration
from typing import Set
import os

class Common(Configuration):
    """Base configuration with environment variable management."""

    # 1. REQUIRED - Application fails to start if missing
    ENVIRON_REQUIRED_KEYS: Set[str] = {
        'SECRET_KEY',
        'DATABASE_URL',
    }

    # 2. OPTIONAL - No default allowed, but not mandatory
    #    Used for optional integrations
    ENVIRON_ONLY_KEYS: Set[str] = {
        'SENDGRID_API_KEY',
        'SLACK_WEBHOOK_URL',
        'STRIPE_API_KEY',
        'SENTRY_DSN',
    }

    # 3. DEFAULT_ALLOWED - Has default value, can be overridden
    #    Used for feature flags and configuration
    DEFAULT_ALLOWED_KEYS: Set[str] = {
        'LOG_LEVEL',
        'ENABLE_NEW_UI',
        'MAX_UPLOAD_SIZE_MB',
        'API_RATE_LIMIT',
    }
```

---

## Validation Pattern

### Validate in pre_setup

```python
class Common(Configuration):
    """Configuration with validation."""

    @classmethod
    def pre_setup(cls):
        """Validate environment variables before setup."""
        super().pre_setup()

        # 1. Check required keys
        missing_required = []
        for key in cls.ENVIRON_REQUIRED_KEYS:
            if not os.getenv(key):
                missing_required.append(key)

        if missing_required:
            raise ValueError(
                f"Missing required environment variables: "
                f"{', '.join(sorted(missing_required))}\n"
                f"Set these in your .env file or environment."
            )

        # 2. Check environ-only keys don't have defaults in code
        for key in cls.ENVIRON_ONLY_KEYS:
            value = os.getenv(key)
            # Warning: This is a code review check, not runtime
            # Ensure these keys are only accessed via environment

        # 3. Validate default-allowed keys have sensible defaults
        for key in cls.DEFAULT_ALLOWED_KEYS:
            # These should have defaults in values.Value() declarations
            pass
```

### Environment-Specific Validation

```python
class Staging(Common):
    """Staging configuration with additional validation."""

    @classmethod
    def pre_setup(cls):
        """Staging requires additional environment variables."""
        super().pre_setup()

        staging_required = cls.ENVIRON_REQUIRED_KEYS | {
            'REDIS_URL',
            'SENTRY_DSN',
        }

        missing = [key for key in staging_required if not os.getenv(key)]
        if missing:
            raise ValueError(
                f"Staging requires: {', '.join(sorted(missing))}"
            )


class Production(Staging):
    """Production configuration with strict validation."""

    @classmethod
    def pre_setup(cls):
        """Production requires all optional service keys."""
        super().pre_setup()

        production_required = cls.ENVIRON_REQUIRED_KEYS | {
            'REDIS_URL',
            'SENTRY_DSN',
            'SENDGRID_API_KEY',
        }

        missing = [key for key in production_required if not os.getenv(key)]
        if missing:
            raise ValueError(
                f"Production requires: {', '.join(sorted(missing))}"
            )

    @classmethod
    def post_setup(cls):
        """Validate production configuration."""
        super().post_setup()

        # Ensure DEBUG is False
        if cls.DEBUG:
            raise ValueError("DEBUG must be False in production")

        # Ensure SECRET_KEY is not default
        if cls.SECRET_KEY == 'change-me':
            raise ValueError("SECRET_KEY must be changed in production")

        # Validate ALLOWED_HOSTS is set
        if not cls.ALLOWED_HOSTS:
            raise ValueError("ALLOWED_HOSTS must be set in production")
```

---

## .env File Management

### .env File (Local Development)

```bash
# .env
# DON'T COMMIT THIS FILE - add to .gitignore

# Django configuration
DJANGO_SETTINGS_MODULE=myproject.settings.development
DJANGO_CONFIGURATION=Development

# Security (REQUIRED)
SECRET_KEY=django-insecure-dev-key-for-local-development-only

# Database (REQUIRED)
DATABASE_URL=postgresql://user:password@localhost:5432/myproject_dev

# Redis (OPTIONAL in dev, REQUIRED in staging/production)
REDIS_URL=redis://localhost:6379/0

# Feature flags (DEFAULT_ALLOWED)
ENABLE_NEW_UI=true
ENABLE_BETA_FEATURES=true
MAX_UPLOAD_SIZE_MB=100

# External services (ENVIRON_ONLY - optional in dev)
SENDGRID_API_KEY=SG.xxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
STRIPE_API_KEY=sk_test_xxx
SENTRY_DSN=https://xxx@sentry.io/xxx

# Logging
LOG_LEVEL=DEBUG
```

### .env.example File (Template - COMMIT THIS)

```bash
# .env.example
# Copy this file to .env and fill in values

# Django configuration
DJANGO_SETTINGS_MODULE=myproject.settings.development
DJANGO_CONFIGURATION=Development

# Security (REQUIRED in ALL environments)
SECRET_KEY=change-me-to-a-secure-secret-key

# Database (REQUIRED in ALL environments)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis (REQUIRED in staging/production, optional in dev)
REDIS_URL=redis://localhost:6379/0

# Feature flags (OPTIONAL - defaults applied if not set)
ENABLE_NEW_UI=false
ENABLE_BETA_FEATURES=false
MAX_UPLOAD_SIZE_MB=10

# External services (OPTIONAL in dev, REQUIRED in production)
SENDGRID_API_KEY=
SLACK_WEBHOOK_URL=
STRIPE_API_KEY=
SENTRY_DSN=

# Logging (OPTIONAL - defaults to INFO)
LOG_LEVEL=INFO
```

### Loading .env Files

```python
# myproject/settings/common.py
from configurations import Configuration
from pathlib import Path

class Common(Configuration):
    """Configuration with .env file loading."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    @classmethod
    def pre_setup(cls):
        """Load .env file before setup."""
        super().pre_setup()

        # Load .env file if it exists
        from dotenv import load_dotenv

        env_file = cls.BASE_DIR / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            print(f"Loaded environment from: {env_file}")
        else:
            print(f"No .env file found at: {env_file}")


class Development(Common):
    """Development loads .env.development if available."""

    @classmethod
    def pre_setup(cls):
        """Load development-specific .env file."""
        super().pre_setup()

        from dotenv import load_dotenv

        # Try .env.development first
        dev_env_file = cls.BASE_DIR / '.env.development'
        if dev_env_file.exists():
            load_dotenv(dev_env_file, override=True)
            print(f"Loaded development environment from: {dev_env_file}")
```

---

## Environment Variable Types

### String Values

```python
from configurations import values

class Common(Configuration):
    """Configuration with string values."""

    # Simple string with default
    APP_NAME = values.Value('MyApp', environ_prefix=None)

    # Required string (no default)
    SECRET_KEY = values.SecretValue()

    # Custom environment variable name
    API_KEY = values.Value(
        None,
        environ_name='EXTERNAL_API_KEY',
    )
```

### Boolean Values

```python
class Common(Configuration):
    """Configuration with boolean values."""

    # Boolean with default
    DEBUG = values.BooleanValue(False)

    # Feature flags
    ENABLE_NEW_UI = values.BooleanValue(False, environ_prefix=None)
    ENABLE_BETA_FEATURES = values.BooleanValue(False, environ_prefix=None)

    # Environment reads: 'true', 'True', '1', 'yes', 'on' as True
    # Everything else is False
```

### Numeric Values

```python
class Common(Configuration):
    """Configuration with numeric values."""

    # Integer values
    MAX_UPLOAD_SIZE_MB = values.IntegerValue(10, environ_prefix=None)
    API_RATE_LIMIT = values.IntegerValue(100, environ_prefix=None)
    CONNECTION_TIMEOUT_SECONDS = values.IntegerValue(30)

    # Float values
    CACHE_TIMEOUT_SECONDS = values.FloatValue(30.5)
    API_RETRY_BACKOFF = values.FloatValue(1.5)
```

### List and Tuple Values

```python
class Common(Configuration):
    """Configuration with list values."""

    # List of strings (comma-separated by default)
    ALLOWED_HOSTS = values.ListValue(['localhost'])
    # Environment: ALLOWED_HOSTS=example.com,www.example.com

    # Custom separator
    INTERNAL_IPS = values.ListValue(
        ['127.0.0.1'],
        separator=';',
    )
    # Environment: INTERNAL_IPS=127.0.0.1;10.0.0.1

    # Tuple of tuples
    ADMINS = values.TupleValue((
        ('Admin Name', 'admin@example.com'),
    ))
```

### Complex Values

```python
class Common(Configuration):
    """Configuration with complex values."""

    # JSON value
    FEATURE_FLAGS = values.JSONValue('{"new_ui": false, "beta": false}')
    # Environment: FEATURE_FLAGS='{"new_ui": true, "beta": false}'

    # Dict value
    CUSTOM_SETTINGS = values.DictValue({
        'option1': 'value1',
        'option2': 'value2',
    })

    # Path value
    MEDIA_ROOT = values.PathValue('/var/www/media')
    LOG_FILE_PATH = values.PathValue('/var/log/myapp/app.log')
```

### Database and Service URLs

```python
class Common(Configuration):
    """Configuration with URL values."""

    # Database URL
    DATABASES = values.DatabaseURLValue(
        'postgresql://user:pass@localhost/db'
    )
    # Environment: DATABASE_URL=postgresql://...

    # Email URL
    EMAIL_CONFIG = values.EmailURLValue(
        'smtp://user:pass@smtp.gmail.com:587/?tls=True'
    )
    # Environment: EMAIL_URL=smtp://...

    # Cache URL
    CACHES = values.CacheURLValue('redis://localhost:6379/0')
    # Environment: CACHE_URL=redis://...

    # Custom URL parsing
    REDIS_URL = values.Value('redis://localhost:6379/0')

    @classmethod
    def setup(cls):
        """Parse REDIS_URL manually if needed."""
        super().setup()

        # Parse Redis URL
        import urllib.parse
        parsed = urllib.parse.urlparse(cls.REDIS_URL)
        cls.REDIS_HOST = parsed.hostname
        cls.REDIS_PORT = parsed.port or 6379
        cls.REDIS_DB = int(parsed.path.lstrip('/') or 0)
```

---

## Secrets Management

### Never Commit Secrets

```python
# BAD ❌ - Hardcoded secrets
SECRET_KEY = "django-insecure-hardcoded-key"
DATABASE_PASSWORD = "mypassword123"
API_KEY = "sk-1234567890"

# GOOD ✅ - Environment variables
SECRET_KEY = values.SecretValue()
DATABASE_URL = values.DatabaseURLValue()
API_KEY = values.Value(None, environ_prefix=None)
```

### Validate Secrets in Production

```python
class Production(Staging):
    """Production with secret validation."""

    @classmethod
    def post_setup(cls):
        """Validate secrets are production-ready."""
        super().post_setup()

        # Ensure SECRET_KEY is not a default/example value
        insecure_keys = [
            'change-me',
            'django-insecure',
            'your-secret-key',
        ]
        for insecure in insecure_keys:
            if insecure in cls.SECRET_KEY.lower():
                raise ValueError(
                    f"SECRET_KEY contains insecure value: '{insecure}'"
                )

        # Ensure SECRET_KEY is long enough
        if len(cls.SECRET_KEY) < 50:
            raise ValueError("SECRET_KEY must be at least 50 characters")
```

### External Secret Management

```python
class Production(Staging):
    """Production with AWS Secrets Manager."""

    @classmethod
    def pre_setup(cls):
        """Load secrets from AWS Secrets Manager."""
        super().pre_setup()

        import os
        import json
        import boto3

        # Only in production
        if os.getenv('DJANGO_CONFIGURATION') == 'Production':
            # Get secret from AWS Secrets Manager
            secret_name = "myproject/production/django"
            region_name = "us-east-1"

            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name,
            )

            try:
                secret_value = client.get_secret_value(SecretId=secret_name)
                secrets = json.loads(secret_value['SecretString'])

                # Set environment variables from secrets
                for key, value in secrets.items():
                    os.environ[key] = value

            except Exception as e:
                raise ValueError(f"Failed to load secrets: {e}")
```

---

## Feature Flags

### Boolean Feature Flags

```python
class Common(Configuration):
    """Configuration with feature flags."""

    # Feature flags with sensible defaults
    ENABLE_NEW_UI = values.BooleanValue(False, environ_prefix=None)
    ENABLE_BETA_FEATURES = values.BooleanValue(False, environ_prefix=None)
    ENABLE_EXPERIMENTAL_API = values.BooleanValue(False, environ_prefix=None)
    ENABLE_ANALYTICS = values.BooleanValue(True, environ_prefix=None)


class Development(Common):
    """Development with features enabled."""

    # Enable all features in development
    ENABLE_NEW_UI = True
    ENABLE_BETA_FEATURES = True
    ENABLE_EXPERIMENTAL_API = True


class Production(Staging):
    """Production with conservative feature flags."""

    # All features disabled by default in production
    # Enable via environment variables after testing in staging
    pass
```

### Testing Feature Flags

```python
# tests/test_features.py
import pytest
from django.test import override_settings
from myapp.views import dashboard

@override_settings(ENABLE_NEW_UI=True)
def test_dashboard__new_ui_enabled__uses_new_template(client):
    """Test new UI template when feature is enabled.

    Given: New UI feature flag is enabled
    When: Accessing dashboard
    Then: New UI template is rendered
    """
    # when
    response = client.get('/dashboard/')

    # then
    assert response.status_code == 200
    assert 'dashboard_new.html' in [t.name for t in response.templates]


@override_settings(ENABLE_NEW_UI=False)
def test_dashboard__new_ui_disabled__uses_old_template(client):
    """Test old UI template when feature is disabled.

    Given: New UI feature flag is disabled
    When: Accessing dashboard
    Then: Old UI template is rendered
    """
    # when
    response = client.get('/dashboard/')

    # then
    assert response.status_code == 200
    assert 'dashboard_old.html' in [t.name for t in response.templates]
```

---

## Documentation Pattern

### Document Environment Variables

```python
# myproject/settings/common.py
"""
Django settings using django-configurations.

Environment Variables
--------------------

REQUIRED (all environments):
    SECRET_KEY: Django secret key (50+ characters)
    DATABASE_URL: PostgreSQL connection URL
        Example: postgresql://user:pass@localhost:5432/dbname

REQUIRED (staging/production):
    REDIS_URL: Redis connection URL
        Example: redis://localhost:6379/0
    SENTRY_DSN: Sentry error tracking DSN
        Example: https://xxx@sentry.io/xxx

OPTIONAL (external services):
    SENDGRID_API_KEY: SendGrid API key for emails
    SLACK_WEBHOOK_URL: Slack webhook for notifications
    STRIPE_API_KEY: Stripe payment processing API key

OPTIONAL (feature flags - defaults provided):
    ENABLE_NEW_UI: Enable new user interface (default: false)
    ENABLE_BETA_FEATURES: Enable beta features (default: false)
    MAX_UPLOAD_SIZE_MB: Maximum file upload size in MB (default: 10)
    API_RATE_LIMIT: API requests per hour (default: 100)

OPTIONAL (configuration - defaults provided):
    LOG_LEVEL: Logging level (default: INFO)
        Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
"""
```

### README Documentation

```markdown
# Environment Setup

## Required Environment Variables

All environments require:

- `SECRET_KEY` - Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DATABASE_URL` - PostgreSQL connection URL

Staging and Production require:

- `REDIS_URL` - Redis connection URL
- `SENTRY_DSN` - Sentry error tracking DSN

## Optional Environment Variables

### External Services

- `SENDGRID_API_KEY` - Email sending via SendGrid
- `SLACK_WEBHOOK_URL` - Slack notifications
- `STRIPE_API_KEY` - Payment processing

### Feature Flags

- `ENABLE_NEW_UI` (default: `false`) - Enable new user interface
- `ENABLE_BETA_FEATURES` (default: `false`) - Enable beta features

### Configuration

- `LOG_LEVEL` (default: `INFO`) - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `MAX_UPLOAD_SIZE_MB` (default: `10`) - Maximum file upload size in megabytes

## Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set required values:
   ```bash
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:pass@localhost/db
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```
```

---

## Best Practices

1. **Categorize variables** - Required, optional, default-allowed
2. **Validate early** - Check in `pre_setup` before app loads
3. **Never commit secrets** - Use `.env` locally, secret managers in production
4. **Document all variables** - In docstrings and README
5. **Use .env.example** - Committed template for setup
6. **Type-safe values** - Use BooleanValue, IntegerValue, etc.
7. **Test feature flags** - Test both enabled and disabled
8. **Environment-specific validation** - Stricter in production
9. **Fail fast** - Raise ValueError for missing required vars
10. **Log configuration** - Log active config and flag states

---

*Related: See `skill.md` for complete Django configuration guide*
