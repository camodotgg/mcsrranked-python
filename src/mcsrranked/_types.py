from enum import IntEnum
from typing import Literal

__all__ = ["MatchType", "SortOrder"]


class MatchType(IntEnum):
    """Match type enumeration."""

    CASUAL = 1
    """Casual match."""
    RANKED = 2
    """Ranked match."""
    PRIVATE = 3
    """Private room match."""
    EVENT = 4
    """Event match."""


SortOrder = Literal["newest", "oldest", "fastest", "slowest"]
"""Sort order for match listings.

- `"newest"`: Most recent first
- `"oldest"`: Oldest first
- `"fastest"`: Fastest completion time first
- `"slowest"`: Slowest completion time first
"""
