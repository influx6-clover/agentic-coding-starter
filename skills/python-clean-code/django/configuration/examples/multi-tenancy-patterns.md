# Multi-Tenancy Configuration Patterns

This guide covers implementing multi-tenant Django applications using the BRAND pattern.

---

## What is Multi-Tenancy?

**Multi-tenancy:** Single application serving multiple tenants (brands, organizations, customers) with tenant-specific configuration.

**Common use cases:**
- White-label SaaS applications
- Multi-brand companies
- Regional variants of same application
- Healthcare systems serving multiple provider networks

---

## BRAND Pattern

### Basic BRAND Configuration

```python
# myproject/settings/common.py
from configurations import Configuration, values
import os

class Common(Configuration):
    """Base configuration with multi-tenancy support."""

    # Brand selection from environment
    BRAND = values.Value(
        os.getenv('BRAND', 'default'),
        environ_prefix=None,
    )

    # Brand-specific configuration
    _BRAND_CONFIG = {
        'clover': {
            'name': 'Clover Health',
            'base_url': 'https://cloverassistant.com',
            'email_sender': 'support@cloverhealth.com',
            'primary_color': '#00A651',
            'logo_url': 'https://cdn.cloverhealth.com/logo.png',
            'timezone': 'America/New_York',
        },
        'counterpart': {
            'name': 'Counterpart Health',
            'base_url': 'https://counterparthealth.com',
            'email_sender': 'support@counterparthealth.com',
            'primary_color': '#0066CC',
            'logo_url': 'https://cdn.counterparthealth.com/logo.png',
            'timezone': 'America/Los_Angeles',
        },
        'default': {
            'name': 'My Application',
            'base_url': 'http://localhost:8000',
            'email_sender': 'noreply@example.com',
            'primary_color': '#333333',
            'logo_url': '',
            'timezone': 'UTC',
        },
    }

    @classmethod
    def setup(cls):
        """Apply brand-specific configuration."""
        super().setup()

        # Get brand configuration
        brand = cls.BRAND.value
        if brand not in cls._BRAND_CONFIG:
            raise ValueError(
                f"Unknown brand: {brand}. "
                f"Valid brands: {', '.join(cls._BRAND_CONFIG.keys())}"
            )

        brand_config = cls._BRAND_CONFIG[brand]

        # Apply brand settings as class attributes
        cls.BRAND_NAME = brand_config['name']
        cls.BASE_URL = brand_config['base_url']
        cls.EMAIL_SENDER = brand_config['email_sender']
        cls.PRIMARY_COLOR = brand_config['primary_color']
        cls.LOGO_URL = brand_config['logo_url']
        cls.TIME_ZONE = brand_config['timezone']

        # Log brand selection
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Configured for brand: {brand} ({cls.BRAND_NAME})")
```

### Usage

```bash
# Run with different brands
BRAND=clover python manage.py runserver
BRAND=counterpart python manage.py runserver

# Default brand if not specified
python manage.py runserver  # Uses 'default' brand
```

---

## Environment Variable Overrides

### Allow Environment Overrides

```python
class Common(Configuration):
    """Configuration with environment overrides per brand."""

    _BRAND_CONFIG = {
        'clover': {
            'base_url': 'https://cloverassistant.com',
            'email_sender': 'support@cloverhealth.com',
        },
        'counterpart': {
            'base_url': 'https://counterparthealth.com',
            'email_sender': 'support@counterparthealth.com',
        },
    }

    @classmethod
    def setup(cls):
        """Apply brand config with environment overrides."""
        super().setup()

        brand = cls.BRAND.value
        brand_config = cls._BRAND_CONFIG.get(brand, {})

        # Apply brand defaults with environment variable overrides
        cls.BASE_URL = values.Value(
            brand_config.get('base_url', 'http://localhost:8000'),
            environ_name='BASE_URL',
            environ_prefix=None,
        ).value

        cls.EMAIL_SENDER = values.Value(
            brand_config.get('email_sender', 'noreply@example.com'),
            environ_name='EMAIL_SENDER',
            environ_prefix=None,
        ).value
```

### Environment Variables

```bash
# .env
BRAND=clover
# Override brand defaults
BASE_URL=https://staging-clover.example.com
EMAIL_SENDER=staging-support@cloverhealth.com
```

---

## Brand-Specific Templates

### Template Directory Structure

```
templates/
├── base.html                  # Common base template
├── clover/
│   ├── base_brand.html       # Clover-specific base
│   ├── home.html             # Clover home page
│   └── emails/
│       └── welcome.html      # Clover welcome email
├── counterpart/
│   ├── base_brand.html       # Counterpart-specific base
│   ├── home.html             # Counterpart home page
│   └── emails/
│       └── welcome.html      # Counterpart welcome email
└── default/
    ├── base_brand.html       # Default base
    └── home.html             # Default home page
```

### Template Configuration

```python
class Common(Configuration):
    """Configuration with brand-specific templates."""

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],  # Will be set in setup()
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'myproject.context_processors.brand_context',
                ],
            },
        },
    ]

    @classmethod
    def setup(cls):
        """Set brand-specific template directories."""
        super().setup()

        brand = cls.BRAND.value

        # Brand-specific templates first, then common templates
        template_dirs = [
            cls.BASE_DIR / 'templates' / brand,
            cls.BASE_DIR / 'templates',
        ]

        cls.TEMPLATES[0]['DIRS'] = template_dirs
```

### Context Processor

```python
# myproject/context_processors.py
"""Brand context processor."""
from django.conf import settings

def brand_context(request):
    """Add brand information to all template contexts.

    Returns:
        Dict with brand configuration
    """
    return {
        'BRAND': settings.BRAND,
        'BRAND_NAME': settings.BRAND_NAME,
        'PRIMARY_COLOR': settings.PRIMARY_COLOR,
        'LOGO_URL': settings.LOGO_URL,
        'BASE_URL': settings.BASE_URL,
    }
```

### Template Usage

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{{ BRAND_NAME }}{% endblock %}</title>
    <style>
        :root {
            --primary-color: {{ PRIMARY_COLOR }};
        }
    </style>
</head>
<body>
    <header>
        {% if LOGO_URL %}
            <img src="{{ LOGO_URL }}" alt="{{ BRAND_NAME }}">
        {% else %}
            <h1>{{ BRAND_NAME }}</h1>
        {% endif %}
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        &copy; 2024 {{ BRAND_NAME }}
    </footer>
</body>
</html>
```

---

## Brand-Specific Static Files

### Static Files Structure

```
static/
├── common/
│   ├── css/
│   │   └── base.css
│   └── js/
│       └── app.js
├── clover/
│   ├── css/
│   │   └── theme.css
│   ├── images/
│   │   └── logo.png
│   └── favicon.ico
├── counterpart/
│   ├── css/
│   │   └── theme.css
│   ├── images/
│   │   └── logo.png
│   └── favicon.ico
└── default/
    └── css/
        └── theme.css
```

### Static Files Configuration

```python
class Common(Configuration):
    """Configuration with brand-specific static files."""

    STATIC_URL = '/static/'
    STATIC_ROOT = None  # Set in setup()
    STATICFILES_DIRS = []  # Set in setup()

    @classmethod
    def setup(cls):
        """Configure brand-specific static files."""
        super().setup()

        brand = cls.BRAND.value

        # Brand-specific static files first, then common
        cls.STATICFILES_DIRS = [
            cls.BASE_DIR / 'static' / brand,
            cls.BASE_DIR / 'static' / 'common',
        ]

        cls.STATIC_ROOT = cls.BASE_DIR / 'staticfiles' / brand
```

---

## Brand-Specific Database Configuration

### Separate Databases Per Brand

```python
class Common(Configuration):
    """Configuration with brand-specific databases."""

    _BRAND_DATABASES = {
        'clover': 'postgresql://user:pass@localhost/clover_db',
        'counterpart': 'postgresql://user:pass@localhost/counterpart_db',
        'default': 'postgresql://user:pass@localhost/default_db',
    }

    @classmethod
    def setup(cls):
        """Configure brand-specific database."""
        super().setup()

        brand = cls.BRAND.value
        database_url = cls._BRAND_DATABASES.get(
            brand,
            cls._BRAND_DATABASES['default']
        )

        # Override with environment variable if provided
        import os
        database_url = os.getenv('DATABASE_URL', database_url)

        cls.DATABASES = values.DatabaseURLValue(database_url).value
```

### Shared Database with Brand Field

```python
# models.py
from django.db import models
from django.conf import settings

class BrandedModel(models.Model):
    """Abstract base model with brand field."""

    brand = models.CharField(
        max_length=50,
        default=lambda: settings.BRAND,
        db_index=True,
    )

    class Meta:
        abstract = True


class Patient(BrandedModel):
    """Patient model with brand isolation."""
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        indexes = [
            models.Index(fields=['brand', 'email']),
        ]


# Custom manager for brand filtering
class BrandedManager(models.Manager):
    """Manager that filters by current brand."""

    def get_queryset(self):
        """Filter queryset by current brand."""
        qs = super().get_queryset()
        from django.conf import settings
        return qs.filter(brand=settings.BRAND)


class Patient(BrandedModel):
    # ... fields ...

    objects = models.Manager()  # All brands
    current = BrandedManager()  # Current brand only


# Usage
all_patients = Patient.objects.all()  # All brands
clover_patients = Patient.current.all()  # Current brand only
```

---

## Brand-Specific External Services

### Service Configuration Per Brand

```python
class Common(Configuration):
    """Configuration with brand-specific services."""

    _BRAND_SERVICES = {
        'clover': {
            'SENDGRID_API_KEY': values.Value(
                None,
                environ_name='CLOVER_SENDGRID_API_KEY',
                environ_prefix=None,
            ),
            'STRIPE_API_KEY': values.Value(
                None,
                environ_name='CLOVER_STRIPE_API_KEY',
                environ_prefix=None,
            ),
        },
        'counterpart': {
            'SENDGRID_API_KEY': values.Value(
                None,
                environ_name='COUNTERPART_SENDGRID_API_KEY',
                environ_prefix=None,
            ),
            'STRIPE_API_KEY': values.Value(
                None,
                environ_name='COUNTERPART_STRIPE_API_KEY',
                environ_prefix=None,
            ),
        },
    }

    @classmethod
    def setup(cls):
        """Configure brand-specific services."""
        super().setup()

        brand = cls.BRAND.value
        if brand in cls._BRAND_SERVICES:
            services = cls._BRAND_SERVICES[brand]
            cls.SENDGRID_API_KEY = services['SENDGRID_API_KEY'].value
            cls.STRIPE_API_KEY = services['STRIPE_API_KEY'].value
        else:
            cls.SENDGRID_API_KEY = None
            cls.STRIPE_API_KEY = None
```

### Environment Variables

```bash
# .env
BRAND=clover

# Clover-specific services
CLOVER_SENDGRID_API_KEY=SG.clover-key
CLOVER_STRIPE_API_KEY=sk_live_clover

# Counterpart-specific services
COUNTERPART_SENDGRID_API_KEY=SG.counterpart-key
COUNTERPART_STRIPE_API_KEY=sk_live_counterpart
```

---

## Testing Multi-Tenancy

### Test with Different Brands

```python
# tests/test_multi_tenancy.py
import pytest
from django.test import override_settings

@override_settings(BRAND='clover')
def test_clover_brand__home_page__shows_clover_branding(client):
    """Test Clover brand home page.

    Given: Application configured for Clover brand
    When: Accessing home page
    Then: Clover branding is displayed
    """
    # when
    response = client.get('/')

    # then
    assert response.status_code == 200
    assert 'Clover Health' in response.content.decode()
    assert '#00A651' in response.content.decode()  # Primary color


@override_settings(BRAND='counterpart')
def test_counterpart_brand__home_page__shows_counterpart_branding(client):
    """Test Counterpart brand home page.

    Given: Application configured for Counterpart brand
    When: Accessing home page
    Then: Counterpart branding is displayed
    """
    # when
    response = client.get('/')

    # then
    assert response.status_code == 200
    assert 'Counterpart Health' in response.content.decode()
    assert '#0066CC' in response.content.decode()  # Primary color


@pytest.mark.django_db
@override_settings(BRAND='clover')
def test_patient_manager__current_brand__filters_by_brand():
    """Test branded manager filters by brand.

    Given: Patients for multiple brands
    When: Querying with current brand manager
    Then: Only current brand patients returned
    """
    # given
    from myapp.models import Patient

    clover_patient = Patient.objects.create(
        brand='clover',
        name='Alice',
        email='alice@clover.example.com',
    )
    counterpart_patient = Patient.objects.create(
        brand='counterpart',
        name='Bob',
        email='bob@counterpart.example.com',
    )

    # when: Query with current brand manager
    current_patients = Patient.current.all()

    # then: Only Clover patients returned
    assert list(current_patients) == [clover_patient]
    assert counterpart_patient not in current_patients
```

---

## Advanced Patterns

### Dynamic Brand Selection from Domain

```python
# myproject/middleware.py
"""Brand selection middleware."""
from django.conf import settings

class BrandMiddleware:
    """Middleware to set brand based on request domain."""

    DOMAIN_BRAND_MAP = {
        'cloverassistant.com': 'clover',
        'www.cloverassistant.com': 'clover',
        'counterparthealth.com': 'counterpart',
        'www.counterparthealth.com': 'counterpart',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Set brand based on request domain."""
        domain = request.get_host().split(':')[0]  # Remove port
        brand = self.DOMAIN_BRAND_MAP.get(domain, settings.BRAND)

        # Store brand in request
        request.brand = brand

        response = self.get_response(request)
        return response


# Update context processor to use request brand
def brand_context(request):
    """Add brand information from request."""
    brand = getattr(request, 'brand', settings.BRAND)
    brand_config = settings._BRAND_CONFIG.get(brand, {})

    return {
        'BRAND': brand,
        'BRAND_NAME': brand_config.get('name', 'Unknown'),
        'PRIMARY_COLOR': brand_config.get('primary_color', '#000'),
        'LOGO_URL': brand_config.get('logo_url', ''),
    }
```

### Brand-Specific Feature Flags

```python
class Common(Configuration):
    """Configuration with brand-specific feature flags."""

    _BRAND_FEATURES = {
        'clover': {
            'ENABLE_NEW_UI': True,
            'ENABLE_BETA_FEATURES': False,
            'MAX_UPLOAD_SIZE_MB': 100,
        },
        'counterpart': {
            'ENABLE_NEW_UI': False,
            'ENABLE_BETA_FEATURES': True,
            'MAX_UPLOAD_SIZE_MB': 50,
        },
        'default': {
            'ENABLE_NEW_UI': False,
            'ENABLE_BETA_FEATURES': False,
            'MAX_UPLOAD_SIZE_MB': 10,
        },
    }

    @classmethod
    def setup(cls):
        """Apply brand-specific feature flags."""
        super().setup()

        brand = cls.BRAND.value
        features = cls._BRAND_FEATURES.get(brand, cls._BRAND_FEATURES['default'])

        # Apply feature flags with environment overrides
        import os
        cls.ENABLE_NEW_UI = os.getenv(
            'ENABLE_NEW_UI',
            str(features['ENABLE_NEW_UI'])
        ).lower() in ('true', '1', 'yes')

        cls.ENABLE_BETA_FEATURES = os.getenv(
            'ENABLE_BETA_FEATURES',
            str(features['ENABLE_BETA_FEATURES'])
        ).lower() in ('true', '1', 'yes')

        cls.MAX_UPLOAD_SIZE_MB = int(os.getenv(
            'MAX_UPLOAD_SIZE_MB',
            str(features['MAX_UPLOAD_SIZE_MB'])
        ))
```

---

## Best Practices

1. **Environment-based brand selection** - Use `BRAND` environment variable
2. **Default brand** - Always provide a 'default' brand configuration
3. **Validate brand** - Fail fast if unknown brand is specified
4. **Brand-specific templates** - Use brand subdirectories for templates
5. **Brand context processor** - Make brand info available in all templates
6. **Test all brands** - Use `@override_settings(BRAND=...)` in tests
7. **Document brands** - List all supported brands in README
8. **Brand isolation** - Use separate databases or brand field for data isolation
9. **Feature flags per brand** - Allow different features for different brands
10. **Environment overrides** - Allow overriding brand defaults via env vars

---

*Related: See `skill.md` for complete Django configuration guide*
