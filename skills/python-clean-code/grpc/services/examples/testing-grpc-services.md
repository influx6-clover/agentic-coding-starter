# Testing gRPC Services

Testing patterns for gRPC service methods.

---

## Basic Test Pattern

```python
def test_create_user__valid_request__succeeds():
    # given
    service = UserManagementService()
    request = usr_pb2.CreateUserRequest(
        email='test@example.com',
        name='Test User',
    )
    context = Mock(spec=ServicerContext)
    context.auth_user_id = 'test-user-id'

    # when
    response = service.CreateUser(request, context)

    # then
    assert response.user.email == 'test@example.com'
```

---

*Related: See skill.md for complete patterns*
