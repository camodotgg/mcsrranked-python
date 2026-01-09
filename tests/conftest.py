"""Pytest configuration and fixtures."""

import json
from pathlib import Path

import pytest
import respx

from mcsrranked import MCSRRanked

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict | list:
    """Load a JSON fixture file."""
    with open(FIXTURES_DIR / name) as f:
        return json.load(f)


@pytest.fixture
def client() -> MCSRRanked:
    """Create a test client."""
    return MCSRRanked()


@pytest.fixture
def mock_api() -> respx.MockRouter:
    """Create a mock API router."""
    with respx.mock(base_url="https://api.mcsrranked.com") as respx_mock:
        yield respx_mock


@pytest.fixture
def user_fixture() -> dict:
    """Load user.json fixture (Feinberg's profile)."""
    return load_fixture("user.json")


@pytest.fixture
def user_matches_fixture() -> list:
    """Load user_matches.json fixture (Feinberg's recent matches)."""
    return load_fixture("user_matches.json")


@pytest.fixture
def user_seasons_fixture() -> dict:
    """Load user_seasons.json fixture (Feinberg's season history)."""
    return load_fixture("user_seasons.json")


@pytest.fixture
def versus_fixture() -> dict:
    """Load versus.json fixture (Feinberg vs Couriway stats)."""
    return load_fixture("versus.json")


@pytest.fixture
def versus_matches_fixture() -> list:
    """Load versus_matches.json fixture (Feinberg vs Couriway matches)."""
    return load_fixture("versus_matches.json")


@pytest.fixture
def matches_fixture() -> list:
    """Load matches.json fixture (recent ranked matches)."""
    return load_fixture("matches.json")


@pytest.fixture
def match_detail_fixture() -> dict:
    """Load match_detail.json fixture (single match details)."""
    return load_fixture("match_detail.json")


@pytest.fixture
def leaderboard_fixture() -> dict:
    """Load leaderboard.json fixture (elo leaderboard)."""
    return load_fixture("leaderboard.json")


@pytest.fixture
def phase_leaderboard_fixture() -> dict:
    """Load phase_leaderboard.json fixture."""
    return load_fixture("phase_leaderboard.json")


@pytest.fixture
def record_leaderboard_fixture() -> dict:
    """Load record_leaderboard.json fixture."""
    return load_fixture("record_leaderboard.json")


@pytest.fixture
def live_fixture() -> dict:
    """Load live.json fixture (live matches)."""
    return load_fixture("live.json")


@pytest.fixture
def weekly_race_fixture() -> dict:
    """Load weekly_race.json fixture."""
    return load_fixture("weekly_race.json")
