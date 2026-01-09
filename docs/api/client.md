# Client Reference

## Synchronous Client

::: mcsrranked.MCSRRanked
    options:
      members:
        - __init__
        - users
        - matches
        - leaderboards
        - live
        - weekly_races
        - with_options
        - close

---

## Asynchronous Client

::: mcsrranked.AsyncMCSRRanked
    options:
      members:
        - __init__
        - users
        - matches
        - leaderboards
        - live
        - weekly_races
        - with_options
        - close

---

## Module-Level Access

The SDK provides module-level access without creating a client:

```python
import mcsrranked

user = mcsrranked.users.get("Feinberg")
matches = mcsrranked.matches.list()
```

!!! note
    Module-level access uses a lazily-created internal client. For async usage, you must use `AsyncMCSRRanked` explicitly.
