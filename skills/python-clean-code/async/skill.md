---
name: "Python with Async Code"
description: "Write robust async/await code using asyncio with proper non-blocking patterns"
approved: Yes
created: 2026-02-02
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.0"
  last_updated: "2026-02-02"
tags:
  - python
  - asyncio
  - async
  - concurrency
files:
  - examples/async-best-practices.py: "Complete async/await patterns and examples"
---

# Python with Async Code

## When to Use This Skill

Read this when **writing async/await code with asyncio** (not sync or tests). This covers:

- Using asyncio as async runtime
- Non-blocking I/O patterns
- Task spawning and coordination
- Avoiding blocking the event loop
- Async testing patterns

**Do NOT read this for:**
- Synchronous code → See [implementation](../implementation/skill.md)
- Testing patterns → See [testing](../testing/skill.md)

---

## Core Principle: Never Block the Event Loop

**Use async for I/O-bound operations. Use sync or `asyncio.to_thread` for CPU-intensive work.**

### Async/Sync Decision Matrix

| Operation Type | Approach |
|---------------|----------|
| **I/O-bound** (network, files) | `asyncio` async APIs (`aiofiles`, `httpx`) |
| **CPU-intensive** (parsing, crypto) | `asyncio.to_thread` or `concurrent.futures` |
| **Waiting** (timers, events) | `asyncio.sleep`, `asyncio.wait_for` |
| **Blocking APIs** (sync libraries) | `asyncio.to_thread` |

---

## Essential Patterns

### 1. Non-Blocking I/O with Timeouts

Always use asyncio's non-blocking APIs with timeouts:

```python
import asyncio
import httpx

async def fetch_with_timeout(url: str) -> bytes:
    """Fetch URL with timeout.

    Args:
        url: URL to fetch.

    Returns:
        Response body bytes.

    Raises:
        asyncio.TimeoutError: If request takes too long.
        httpx.HTTPError: On HTTP errors.
    """
    async with httpx.AsyncClient() as client:
        # Non-blocking request with timeout
        response = await asyncio.wait_for(
            client.get(url),
            timeout=30.0
        )
        response.raise_for_status()
        return response.content
```

### 2. Offload CPU Work with asyncio.to_thread

**CRITICAL:** Never block the event loop with CPU-intensive work.

```python
import asyncio

def expensive_computation(data: bytes) -> bytes:
    """CPU-intensive synchronous computation."""
    # Expensive work here
    return processed_data

# BAD ❌ - Blocks event loop
async def process_data_bad(data: bytes) -> bytes:
    """DON'T DO THIS - blocks event loop!"""
    return expensive_computation(data)  # Blocks all other tasks!

# GOOD ✅ - Offloads to thread pool
async def process_data_good(data: bytes) -> bytes:
    """Process data without blocking event loop."""
    return await asyncio.to_thread(expensive_computation, data)
```

### 3. Async Test Patterns

Use pytest-asyncio for async test support:

```python
import pytest
import asyncio

# Install: pip install pytest-asyncio

# Enable in pyproject.toml:
# [tool.pytest.ini_options]
# asyncio_mode = "auto"

@pytest.mark.asyncio
async def test_async_operation():
    """Test async function."""
    result = await fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_timeout():
    """Test timeout handling."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)
```

---

## Task Management

### Spawning Concurrent Tasks

```python
import asyncio
from typing import List

async def process_item(item: str) -> str:
    """Process single item asynchronously."""
    await asyncio.sleep(0.1)
    return f"processed_{item}"

async def process_all(items: List[str]) -> List[str]:
    """Process all items concurrently.

    Args:
        items: List of items to process.

    Returns:
        List of processed results.
    """
    # Create tasks for concurrent execution
    tasks = [asyncio.create_task(process_item(item)) for item in items]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    return results

# Usage
async def main():
    items = ["a", "b", "c", "d"]
    results = await process_all(items)
    print(results)

# Run
asyncio.run(main())
```

### Using asyncio.gather for Multiple Operations

```python
async def fetch_user(user_id: int) -> dict:
    """Fetch user data."""
    # Simulate async operation
    await asyncio.sleep(0.1)
    return {"id": user_id, "name": f"User{user_id}"}

async def fetch_posts(user_id: int) -> list:
    """Fetch user posts."""
    await asyncio.sleep(0.1)
    return [{"id": 1, "title": "Post 1"}]

async def get_user_with_posts(user_id: int) -> dict:
    """Fetch user and posts concurrently.

    Args:
        user_id: User ID to fetch.

    Returns:
        Dictionary with user data and posts.
    """
    # Run both operations concurrently
    user, posts = await asyncio.gather(
        fetch_user(user_id),
        fetch_posts(user_id)
    )

    return {
        "user": user,
        "posts": posts
    }
```

### Error Handling with gather

```python
async def fetch_with_error_handling(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs with error handling.

    Args:
        urls: List of URLs to fetch.

    Returns:
        List of results (None for failed requests).
    """
    async def fetch_safe(url: str) -> dict | None:
        try:
            return await fetch_url(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    results = await asyncio.gather(*[fetch_safe(url) for url in urls])
    return results
```

---

## Queue Patterns

### Producer-Consumer with asyncio.Queue

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, n: int):
    """Produce items into queue.

    Args:
        queue: Queue to put items into.
        n: Number of items to produce.
    """
    for i in range(n):
        await queue.put(f"item_{i}")
        await asyncio.sleep(0.1)

    # Signal completion
    await queue.put(None)

async def consumer(queue: Queue):
    """Consume items from queue.

    Args:
        queue: Queue to get items from.
    """
    while True:
        item = await queue.get()

        if item is None:
            break

        # Process item
        print(f"Processing {item}")
        await asyncio.sleep(0.2)

        queue.task_done()

async def main():
    """Run producer-consumer pattern."""
    queue = Queue(maxsize=10)  # Bounded queue for backpressure

    # Start producer and consumer
    producer_task = asyncio.create_task(producer(queue, 5))
    consumer_task = asyncio.create_task(consumer(queue))

    # Wait for completion
    await producer_task
    await consumer_task

asyncio.run(main())
```

---

## Timeout and Cancellation

### Using asyncio.wait_for

```python
async def operation_with_timeout(url: str) -> dict:
    """Perform operation with timeout.

    Args:
        url: URL to fetch.

    Returns:
        Response data.

    Raises:
        asyncio.TimeoutError: If operation takes too long.
    """
    try:
        result = await asyncio.wait_for(
            fetch_data(url),
            timeout=5.0
        )
        return result
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
        raise
```

### Using asyncio.wait with Multiple Tasks

```python
async def wait_for_first(urls: List[str]) -> dict:
    """Wait for first successful response.

    Args:
        urls: List of URLs to try.

    Returns:
        First successful response.

    Raises:
        Exception: If all requests fail.
    """
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]

    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel pending tasks
    for task in pending:
        task.cancel()

    # Return first successful result
    for task in done:
        try:
            return task.result()
        except Exception:
            continue

    raise Exception("All requests failed")
```

---

## Common Pitfalls

### Pitfall 1: Blocking the Event Loop

```python
import time

# BAD ❌ - Blocks event loop
async def bad_sleep():
    """DON'T DO THIS - blocks all other tasks!"""
    time.sleep(1)  # Blocks the entire event loop!

# GOOD ✅ - Non-blocking sleep
async def good_sleep():
    """Properly yields control to event loop."""
    await asyncio.sleep(1)

# BAD ❌ - Blocking I/O
async def bad_read_file():
    """DON'T DO THIS - blocking file I/O!"""
    with open('file.txt') as f:
        return f.read()  # Blocks!

# GOOD ✅ - Async file I/O
import aiofiles

async def good_read_file():
    """Non-blocking file I/O."""
    async with aiofiles.open('file.txt') as f:
        return await f.read()
```

### Pitfall 2: Forgetting to Await

```python
# BAD ❌ - Forgot to await
async def bad_example():
    """DON'T DO THIS - coroutine never executes!"""
    result = fetch_data()  # Returns coroutine, doesn't execute!
    # result is <coroutine object>, not the actual data!

# GOOD ✅ - Properly await
async def good_example():
    """Properly awaits coroutine."""
    result = await fetch_data()  # Actually executes
    return result
```

### Pitfall 3: Mixing Sync and Async

```python
import asyncio
import requests  # Synchronous library

# BAD ❌ - Mixing sync library in async code
async def bad_fetch(url: str):
    """DON'T DO THIS - blocks event loop!"""
    response = requests.get(url)  # Blocking!
    return response.json()

# GOOD ✅ - Use async library
import httpx

async def good_fetch(url: str):
    """Use async HTTP library."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# ACCEPTABLE ✅ - Offload to thread
async def acceptable_fetch(url: str):
    """Offload blocking library to thread."""
    def sync_fetch():
        return requests.get(url).json()

    return await asyncio.to_thread(sync_fetch)
```

### Pitfall 4: Not Cancelling Tasks

```python
# BAD ❌ - Leaking tasks
async def bad_timeout():
    """Tasks keep running even after timeout!"""
    tasks = [asyncio.create_task(fetch(url)) for url in urls]

    try:
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=5)
    except asyncio.TimeoutError:
        pass  # Tasks still running!

# GOOD ✅ - Properly cancel tasks
async def good_timeout():
    """Cancels tasks on timeout."""
    tasks = [asyncio.create_task(fetch(url)) for url in urls]

    try:
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=5)
    except asyncio.TimeoutError:
        for task in tasks:
            task.cancel()
        # Wait for cancellation
        await asyncio.gather(*tasks, return_exceptions=True)
```

---

## Async Context Managers

```python
class AsyncResource:
    """Async context manager example."""

    async def __aenter__(self):
        """Async setup."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async cleanup."""
        await self.close()

    async def connect(self):
        """Connect to resource."""
        await asyncio.sleep(0.1)

    async def close(self):
        """Close resource."""
        await asyncio.sleep(0.1)

# Usage
async def main():
    async with AsyncResource() as resource:
        # Use resource
        pass
    # Automatically closed
```

---

## Async Generators

```python
async def async_range(start: int, stop: int):
    """Async generator example.

    Args:
        start: Start value.
        stop: Stop value.

    Yields:
        Values from start to stop.
    """
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i

# Usage
async def main():
    async for value in async_range(0, 5):
        print(value)

asyncio.run(main())
```

---

## Dependency Configuration

```toml
# pyproject.toml
[tool.poetry.dependencies]
# Async HTTP client
httpx = "^0.27"

# Async file I/O
aiofiles = "^23.2"

# Async database drivers
asyncpg = "^0.29"  # PostgreSQL
aiomysql = "^0.2"  # MySQL

[tool.poetry.group.dev.dependencies]
# Async testing
pytest-asyncio = "^0.23"

[tool.pytest.ini_options]
# Enable async test support
asyncio_mode = "auto"
```

---

## Learning Log

### 2026-02-02: Python Async Code Skill Created

**Issue:** Creating Python equivalent of Rust async code skill.

**Learning:** Adapted Rust tokio patterns to Python asyncio:
- `asyncio.to_thread` instead of `tokio::spawn_blocking`
- `asyncio.gather` instead of `tokio::join!`
- `asyncio.Queue` instead of tokio channels
- pytest-asyncio for async testing
- Event loop blocking prevention

**New Standard:** All Python async code must follow these patterns.

---

## Examples

See `examples/` directory for working code:

- `async-best-practices.py` - Complete async/await patterns with asyncio

## Related Skills

- [Python Clean Implementation](../implementation/skill.md) - For sync implementation patterns
- [Python Testing Excellence](../testing/skill.md) - For testing async code

---

*Last Updated: 2026-02-02*
*Version: 1.0*
