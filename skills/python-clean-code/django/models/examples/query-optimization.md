# Django Query Optimization - N+1 Prevention Guide

This guide covers query optimization patterns to prevent N+1 query problems and optimize database access.

---

## What is the N+1 Problem?

**The Problem:** Making 1 query for main data, then N additional queries for related data.

```python
# BAD ❌ - N+1 queries
posts = Post.objects.all()  # 1 query for posts
for post in posts:
    print(post.author.name)  # N queries (one per post!)

# Total: 1 + N queries
# If 100 posts, executes 101 queries! 🔥
```

**The Solution:** Use `select_related()` or `prefetch_related()` to fetch related data efficiently.

```python
# GOOD ✅ - Single optimized query
posts = Post.objects.select_related('author').all()  # 1 query with JOIN
for post in posts:
    print(post.author.name)  # No additional queries!

# Total: 1 query
# Always 1 query regardless of post count! ✨
```

---

## Select Related (ForeignKey and OneToOne)

Use `select_related()` for **single-valued relationships** (ForeignKey, OneToOne).

### Basic Usage

```python
# Model structure
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Single-valued
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Single-valued

# BAD ❌ - N+1 queries
posts = Post.objects.all()
for post in posts:
    print(f"{post.title} by {post.author.name}")
# Queries: 1 (posts) + N (authors) = N+1

# GOOD ✅ - Single JOIN query
posts = Post.objects.select_related('author').all()
for post in posts:
    print(f"{post.title} by {post.author.name}")
# Queries: 1 (with JOIN)

# SQL generated:
# SELECT post.*, user.*
# FROM posts
# INNER JOIN users ON posts.author_id = users.id
```

### Multiple Relations

```python
# Fetch multiple related objects
posts = Post.objects.select_related(
    'author',
    'category',
).all()

for post in posts:
    print(f"{post.title} by {post.author.name} in {post.category.name}")
# Still just 1 query with multiple JOINs!
```

### Deep Relations (Following ForeignKeys)

```python
# Model structure
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class User(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

# Fetch post → author → profile in one query
posts = Post.objects.select_related('author__profile').all()

for post in posts:
    print(f"{post.title} by {post.author.profile.bio}")
# Single query with chained JOINs!

# SQL generated:
# SELECT post.*, user.*, profile.*
# FROM posts
# INNER JOIN users ON posts.author_id = users.id
# INNER JOIN profiles ON users.profile_id = profiles.id
```

### When to Use

✅ Use `select_related()` when:
- Following **ForeignKey** relationships
- Following **OneToOneField** relationships
- Relationship points to **one** object
- You will access the related object

❌ Don't use `select_related()` when:
- Following **ManyToManyField** (use `prefetch_related()`)
- Following reverse **ForeignKey** (use `prefetch_related()`)
- Related object is rarely accessed

---

## Prefetch Related (ManyToMany and Reverse ForeignKey)

Use `prefetch_related()` for **multi-valued relationships** (ManyToMany, reverse ForeignKey).

### Basic Usage

```python
# Model structure
class User(models.Model):
    name = models.CharField(max_length=255)

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='groups')  # Multi-valued

# BAD ❌ - N+1 queries
users = User.objects.all()
for user in users:
    print(f"{user.name}: {[g.name for g in user.groups.all()]}")
# Queries: 1 (users) + N (groups per user) = N+1

# GOOD ✅ - Separate optimized query
users = User.objects.prefetch_related('groups').all()
for user in users:
    print(f"{user.name}: {[g.name for g in user.groups.all()]}")
# Queries: 2 total (users, then all groups in one query)

# SQL generated:
# Query 1: SELECT * FROM users
# Query 2: SELECT * FROM groups
#          INNER JOIN user_groups ON groups.id = user_groups.group_id
#          WHERE user_groups.user_id IN (1, 2, 3, ...)
```

### Reverse ForeignKey

```python
# Model structure
class User(models.Model):
    name = models.CharField(max_length=255)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

# BAD ❌ - N+1 queries
users = User.objects.all()
for user in users:
    print(f"{user.name} has {user.posts.count()} posts")
# Queries: 1 (users) + N (posts per user) = N+1

# GOOD ✅ - Prefetch posts
users = User.objects.prefetch_related('posts').all()
for user in users:
    print(f"{user.name} has {len(user.posts.all())} posts")
# Queries: 2 total (users, then all posts)
```

### Deep Prefetching

```python
# Model structure
class User(models.Model):
    name = models.CharField(max_length=255)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Fetch users → posts → comments in optimized queries
users = User.objects.prefetch_related(
    'posts',                    # User's posts
    'posts__comments',          # Comments on those posts
    'posts__comments__author',  # Authors of those comments
).all()

for user in users:
    for post in user.posts.all():
        for comment in post.comments.all():
            print(f"{comment.author.name}: {comment.text}")
# Queries: 4 total (users, posts, comments, comment authors)
# NO N+1 problem!
```

### When to Use

✅ Use `prefetch_related()` when:
- Following **ManyToManyField** relationships
- Following **reverse ForeignKey** relationships
- Relationship points to **many** objects
- You will iterate over related objects

❌ Don't use `prefetch_related()` when:
- Following regular **ForeignKey** (use `select_related()`)
- Following **OneToOneField** (use `select_related()`)

---

## Combining Select and Prefetch

**Most powerful pattern:** Combine both for complex data structures.

```python
# Model structure
class User(models.Model):
    name = models.CharField(max_length=255)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')

# Optimal query pattern
posts = Post.objects.select_related(
    'author',           # ForeignKey: use select_related
    'author__profile',  # OneToOne through author: use select_related
    'category',         # ForeignKey: use select_related
).prefetch_related(
    'tags',            # ManyToMany: use prefetch_related
    'comments',        # Reverse ForeignKey: use prefetch_related
    'comments__author',
).all()

# Usage - all data available with no additional queries
for post in posts:
    print(f"Title: {post.title}")
    print(f"Author: {post.author.name}")
    print(f"Bio: {post.author.profile.bio}")
    print(f"Category: {post.category.name}")
    print(f"Tags: {[tag.name for tag in post.tags.all()]}")
    for comment in post.comments.all():
        print(f"  {comment.author.name}: {comment.text}")

# Total queries: 4
# - 1 query with JOINs (post, author, profile, category)
# - 1 query for tags
# - 1 query for comments
# - 1 query for comment authors
```

---

## Custom Prefetch Objects

For complex scenarios, use `Prefetch` objects to customize prefetching.

### Filtering Prefetched Data

```python
from django.db.models import Prefetch
from datetime import timedelta
from django.utils import timezone

# Only prefetch recent posts
recent_posts = Post.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=7)
).select_related('category')

users = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=recent_posts,
        to_attr='recent_posts',  # Access via user.recent_posts
    )
).all()

for user in users:
    print(f"{user.name} recent posts:")
    for post in user.recent_posts:  # Pre-filtered!
        print(f"  - {post.title} ({post.category.name})")
```

### Ordering Prefetched Data

```python
# Prefetch posts ordered by popularity
popular_posts = Post.objects.order_by('-view_count')

users = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=popular_posts,
        to_attr='popular_posts',
    )
).all()
```

### Multiple Prefetch Paths

```python
# Prefetch both published and draft posts separately
published_posts = Post.objects.filter(status='published')
draft_posts = Post.objects.filter(status='draft')

users = User.objects.prefetch_related(
    Prefetch('posts', queryset=published_posts, to_attr='published_posts'),
    Prefetch('posts', queryset=draft_posts, to_attr='draft_posts'),
).all()

for user in users:
    print(f"{user.name}:")
    print(f"  Published: {len(user.published_posts)}")
    print(f"  Drafts: {len(user.draft_posts)}")
```

---

## Only and Defer (Field Selection)

Reduce data transfer by selecting only needed fields.

### Only (Select Specific Fields)

```python
# Only fetch specific fields
users = User.objects.only('id', 'name', 'email')
# SELECT id, name, email FROM users

for user in users:
    print(user.name)   # ✅ No query
    print(user.email)  # ✅ No query
    print(user.bio)    # ❌ Additional query! Field was deferred
```

### Defer (Exclude Specific Fields)

```python
# Exclude large fields
users = User.objects.defer('bio', 'profile_image')
# SELECT id, name, email, ... FROM users (all except bio, profile_image)

for user in users:
    print(user.name)   # ✅ No query
    print(user.bio)    # ❌ Additional query! Field was deferred
```

### When to Use

✅ Use `only()` / `defer()` when:
- Large fields (text, binary) you don't need
- Reducing data transfer is critical
- Processing many records

❌ Avoid when:
- You'll access deferred fields anyway (causes more queries!)
- Fields are small (overhead not worth it)

---

## Bulk Operations

Use bulk methods for better performance when modifying multiple records.

### Bulk Create

```python
# BAD ❌ - Multiple INSERTs
for i in range(1000):
    User.objects.create(name=f"User {i}", email=f"user{i}@example.com")
# Executes: 1000 queries

# GOOD ✅ - Single bulk INSERT
users = [
    User(name=f"User {i}", email=f"user{i}@example.com")
    for i in range(1000)
]
User.objects.bulk_create(users, batch_size=500)
# Executes: 2 queries (batched by 500)
```

### Bulk Update

```python
# BAD ❌ - Multiple UPDATEs
users = User.objects.all()
for user in users:
    user.last_login = timezone.now()
    user.save()
# Executes: N queries

# GOOD ✅ - Single UPDATE (if all same value)
User.objects.all().update(last_login=timezone.now())
# Executes: 1 query

# GOOD ✅ - Bulk update (Django 4.2+, different values per record)
users = User.objects.all()
for user in users:
    user.last_login = timezone.now()
    user.login_count += 1
User.objects.bulk_update(users, ['last_login', 'login_count'], batch_size=500)
# Executes: Batched queries (much faster than individual saves)
```

### Bulk Update or Create

```python
# Update if exists, create if not
User.objects.update_or_create(
    email='alice@example.com',  # Lookup fields
    defaults={'name': 'Alice Updated', 'is_active': True}  # Update/create fields
)
# Executes: 1-2 queries (SELECT then UPDATE/INSERT)

# Bulk version (Django 4.2+)
User.objects.bulk_create(
    users,
    update_conflicts=True,
    unique_fields=['email'],
    update_fields=['name', 'is_active'],
)
```

---

## Query Debugging

### Checking Query Count

```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

with CaptureQueriesContext(connection) as context:
    # Your code here
    posts = Post.objects.select_related('author').all()
    for post in posts:
        print(post.author.name)

print(f"Queries executed: {len(context.captured_queries)}")
for query in context.captured_queries:
    print(query['sql'])
```

### Django Debug Toolbar (Development)

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = ['127.0.0.1']

# Shows:
# - Number of queries
# - Query execution time
# - Duplicate queries
# - Query location in code
```

### Django Silk (Production-Safe Profiling)

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'silk',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    # ...
]

# Features:
# - Production-safe profiling
# - Query analysis
# - Request profiling
# - No debug mode required
```

---

## Common Patterns

### Pattern 1: List View with Optimized Queries

```python
def get_posts_for_list():
    """Get posts optimized for list view."""
    return Post.objects.select_related(
        'author',
        'category',
    ).prefetch_related(
        'tags',
    ).only(
        'id', 'title', 'created_at',
        'author__name',
        'category__name',
    ).order_by('-created_at')
```

### Pattern 2: Detail View with All Related Data

```python
def get_post_for_detail(post_id):
    """Get single post with all related data."""
    return Post.objects.select_related(
        'author',
        'author__profile',
        'category',
    ).prefetch_related(
        'tags',
        'comments',
        'comments__author',
    ).get(pk=post_id)
```

### Pattern 3: Aggregation with Related Data

```python
from django.db.models import Count, Prefetch

# Get users with post count (no prefetch needed)
users = User.objects.annotate(
    post_count=Count('posts')
).order_by('-post_count')

# Get users with post count AND posts
users = User.objects.annotate(
    post_count=Count('posts')
).prefetch_related('posts').order_by('-post_count')
```

---

## Testing Query Optimization

```python
import pytest
from django.test.utils import CaptureQueriesContext
from django.db import connection
from tests.factories import UserFactory, PostFactory

@pytest.mark.django_db
def test_post_list__optimized_queries__no_n_plus_1():
    """Test post list has optimized queries.

    Given: 10 posts with authors and tags
    When: Fetching posts with select/prefetch related
    Then: Fixed number of queries (no N+1)
    """
    # given: Posts with related data
    users = UserFactory.create_batch(10)
    posts = [PostFactory(author=user) for user in users]
    for post in posts:
        post.tags.add(*TagFactory.create_batch(3))

    # when: Fetch with optimization
    with CaptureQueriesContext(connection) as context:
        fetched_posts = Post.objects.select_related(
            'author',
        ).prefetch_related(
            'tags',
        ).all()

        # Access related data
        for post in fetched_posts:
            _ = post.author.name
            _ = [tag.name for tag in post.tags.all()]

    # then: Fixed queries (1 for posts+author, 1 for tags)
    assert len(context.captured_queries) == 2


@pytest.mark.django_db
def test_post_list__without_optimization__has_n_plus_1():
    """Test that unoptimized queries cause N+1 problem."""
    # given: 10 posts
    users = UserFactory.create_batch(10)
    posts = [PostFactory(author=user) for user in users]

    # when: Fetch WITHOUT optimization
    with CaptureQueriesContext(connection) as context:
        fetched_posts = Post.objects.all()  # No select_related!

        for post in fetched_posts:
            _ = post.author.name  # Query for each post!

    # then: N+1 queries (1 for posts + 10 for authors)
    assert len(context.captured_queries) == 11  # Documents the problem!
```

---

## Best Practices

1. **Always use select_related/prefetch_related** for related data access
2. **Test query counts** in tests to catch N+1 problems
3. **Use debug toolbar** in development to see queries
4. **Profile production** with Django Silk or similar
5. **Bulk operations** for creating/updating many records
6. **Index foreign keys** for JOIN performance
7. **Only/defer** for large fields you don't need
8. **Cache** query results when appropriate

---

*Related: See `skill.md` for complete Django models guide*
