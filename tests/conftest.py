"""Pytest configuration and fixtures."""

import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
import respx

from mcsrranked import MCSRRanked

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any] | list[Any]:
    """Load a JSON fixture file."""
    with open(FIXTURES_DIR / name) as f:
        data: dict[str, Any] | list[Any] = json.load(f)
        return data


@pytest.fixture
def client() -> MCSRRanked:
    """Create a test client."""
    return MCSRRanked()


@pytest.fixture
def mock_api() -> Generator[respx.MockRouter, None, None]:
    """Create a mock API router."""
    with respx.mock(base_url="https://api.mcsrranked.com") as respx_mock:
        yield respx_mock


@pytest.fixture
def user_fixture() -> dict[str, Any]:
    """Load user.json fixture (Feinberg's profile)."""
    result = load_fixture("user.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def user_matches_fixture() -> list[Any]:
    """Load user_matches.json fixture (Feinberg's recent matches)."""
    result = load_fixture("user_matches.json")
    assert isinstance(result, list)
    return result


@pytest.fixture
def user_seasons_fixture() -> dict[str, Any]:
    """Load user_seasons.json fixture (Feinberg's season history)."""
    result = load_fixture("user_seasons.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def versus_fixture() -> dict[str, Any]:
    """Load versus.json fixture (Feinberg vs Couriway stats)."""
    result = load_fixture("versus.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def versus_matches_fixture() -> list[Any]:
    """Load versus_matches.json fixture (Feinberg vs Couriway matches)."""
    result = load_fixture("versus_matches.json")
    assert isinstance(result, list)
    return result


@pytest.fixture
def matches_fixture() -> list[Any]:
    """Load matches.json fixture (recent ranked matches)."""
    result = load_fixture("matches.json")
    assert isinstance(result, list)
    return result


@pytest.fixture
def match_detail_fixture() -> dict[str, Any]:
    """Load match_detail.json fixture (single match details)."""
    result = load_fixture("match_detail.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def leaderboard_fixture() -> dict[str, Any]:
    """Load leaderboard.json fixture (elo leaderboard)."""
    result = load_fixture("leaderboard.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def phase_leaderboard_fixture() -> dict[str, Any]:
    """Load phase_leaderboard.json fixture."""
    result = load_fixture("phase_leaderboard.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def record_leaderboard_fixture() -> list[Any]:
    """Load record_leaderboard.json fixture."""
    result = load_fixture("record_leaderboard.json")
    assert isinstance(result, list)
    return result


@pytest.fixture
def live_fixture() -> dict[str, Any]:
    """Load live.json fixture (live matches)."""
    result = load_fixture("live.json")
    assert isinstance(result, dict)
    return result


@pytest.fixture
def weekly_race_fixture() -> dict[str, Any]:
    """Load weekly_race.json fixture."""
    result = load_fixture("weekly_race.json")
    assert isinstance(result, dict)
    return result
