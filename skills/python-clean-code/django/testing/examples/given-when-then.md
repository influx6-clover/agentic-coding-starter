# Given/When/Then Test Structure

This guide covers using Given/When/Then pattern for clear, maintainable tests.

---

## Why Given/When/Then?

**Benefits:**
- **Clarity**: Easy to understand test intent
- **Structure**: Consistent test organization
- **Maintainability**: Clear sections for modifications
- **Documentation**: Tests serve as specification

---

## Basic Pattern

```python
def test_create_user__valid_email__saves_to_database():
    """Test user creation with valid email.

    Given: Valid user data
    When: Creating user
    Then: User is saved to database
    """
    # given: Valid user data
    name = 'Alice'
    email = 'alice@example.com'

    # when: Create user
    user = User.objects.create(name=name, email=email)

    # then: User saved to database
    assert User.objects.filter(pk=user.pk).exists()
    assert user.name == name
    assert user.email == email
```

---

## Given Section

**Purpose:** Set up test preconditions

```python
@pytest.mark.django_db
def test_complete_task__pending_task__sets_completed_at():
    """Test completing pending task sets timestamp."""
    # given: Pending task
    task = TaskFactory(
        title='Test Task',
        status='pending',
        completed_at=None,
    )

    # given: Frozen time
    from freezegun import freeze_time
    frozen_time = '2024-01-15 12:00:00+00:00'

    # when/then...
```

---

## When Section

**Purpose:** Execute the action being tested

```python
@pytest.mark.django_db
def test_update_user_email__new_email__updates_successfully():
    """Test updating user email."""
    # given
    user = UserFactory(email='old@example.com')
    new_email = 'new@example.com'

    # when: Update email
    user.email = new_email
    user.save()

    # then...
```

---

## Then Section

**Purpose:** Verify expected outcomes

```python
@pytest.mark.django_db
def test_delete_user__soft_delete__marks_deleted():
    """Test soft deleting user."""
    # given
    user = UserFactory()
    user_id = user.pk

    # when
    user.soft_delete()

    # then: User marked deleted
    user.refresh_from_db()
    assert user.is_deleted() is True
    assert user.deleted_at is not None

    # then: User still in database
    assert User.objects.filter(pk=user_id).exists()
```

---

## Complex Example

```python
@pytest.mark.django_db
def test_place_order__insufficient_stock__raises_error(mocker):
    """Test ordering with insufficient stock raises error.

    Given: Product with limited stock and order exceeding stock
    When: Attempting to place order
    Then: InsufficientStockError is raised and no order created
    """
    # given: Product with 5 items in stock
    product = ProductFactory(name='Widget', stock_quantity=5)

    # given: User attempting to order 10 items
    user = UserFactory()
    order_quantity = 10

    # given: Mock notification service
    mock_notify = mocker.patch('myapp.services.NotificationService.send')

    # when: Attempt to place order
    with pytest.raises(InsufficientStockError) as exc_info:
        place_order(user=user, product=product, quantity=order_quantity)

    # then: Error message contains details
    assert 'insufficient stock' in str(exc_info.value).lower()
    assert str(product.stock_quantity) in str(exc_info.value)

    # then: No order created
    assert Order.objects.filter(user=user, product=product).count() == 0

    # then: Stock unchanged
    product.refresh_from_db()
    assert product.stock_quantity == 5

    # then: Notification not sent
    mock_notify.assert_not_called()
```

---

## Best Practices

1. **Always use comments** - Mark sections with # given:, # when:, # then:
2. **Blank lines** - Separate sections with blank lines
3. **Multiple assertions in then** - Verify all expected outcomes
4. **Docstring** - Summarize in Given/When/Then format
5. **Complex setup** - Break given into multiple subsections
6. **One when** - Single action being tested
7. **Clear intent** - Test name and structure show what's tested

---

*Related: See `skill.md` for complete Django testing guide*
