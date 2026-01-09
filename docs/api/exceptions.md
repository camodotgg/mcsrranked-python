# Exceptions Reference

## Exception Hierarchy

```
MCSRRankedError
├── APIError
│   ├── APIStatusError
│   │   ├── BadRequestError
│   │   ├── AuthenticationError
│   │   ├── NotFoundError
│   │   └── RateLimitError
│   └── APIConnectionError
│       └── APITimeoutError
```

---

## Base Exceptions

::: mcsrranked.MCSRRankedError
    options:
      show_docstring_attributes: true

::: mcsrranked.APIError
    options:
      show_docstring_attributes: true

---

## HTTP Status Exceptions

::: mcsrranked.APIStatusError
    options:
      show_docstring_attributes: true

::: mcsrranked.BadRequestError

::: mcsrranked.AuthenticationError

::: mcsrranked.NotFoundError

::: mcsrranked.RateLimitError

---

## Connection Exceptions

::: mcsrranked.APIConnectionError

::: mcsrranked.APITimeoutError

---

## Usage Examples

### Catching all SDK errors

```python
from mcsrranked import MCSRRankedError

try:
    user = mcsrranked.users.get("someone")
except MCSRRankedError as e:
    print(f"SDK error: {e}")
```

### Catching specific errors

```python
from mcsrranked import NotFoundError, RateLimitError

try:
    user = mcsrranked.users.get("nonexistent")
except NotFoundError as e:
    print(f"User not found: {e.status_code}")
except RateLimitError as e:
    print(f"Rate limited: {e.status_code}")
```

### Accessing error details

```python
from mcsrranked import APIStatusError

try:
    user = mcsrranked.users.get("invalid")
except APIStatusError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Body: {e.body}")
```
