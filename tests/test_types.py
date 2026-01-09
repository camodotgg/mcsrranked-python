import pytest

from mcsrranked.types.shared import MatchSeed
from mcsrranked.types.user import SeasonStats, TotalStats


class TestSeasonStatsParsing:
    """Test that season stats are correctly parsed from API format."""

    def test_pivot_stats_from_api_format(self):
        """Test parsing API stat-first format to mode-first format."""
        # This is how the API actually returns data
        api_data = {
            "wins": {"ranked": 55, "casual": 10},
            "loses": {"ranked": 42, "casual": 5},  # Note: API uses 'loses'
            "bestTime": {"ranked": 505888, "casual": None},
            "playedMatches": {"ranked": 108, "casual": 15},
            "currentWinStreak": {"ranked": 3, "casual": 0},
            "highestWinStreak": {"ranked": 8, "casual": 2},
            "playtime": {"ranked": 72151968, "casual": 1000000},
            "forfeits": {"ranked": 0, "casual": 1},
            "completions": {"ranked": 40, "casual": 8},
        }

        stats = SeasonStats.model_validate(api_data)

        # Verify ranked stats
        assert stats.ranked.wins == 55
        assert stats.ranked.losses == 42
        assert stats.ranked.best_time == 505888
        assert stats.ranked.played_matches == 108
        assert stats.ranked.current_winstreak == 3
        assert stats.ranked.highest_winstreak == 8
        assert stats.ranked.playtime == 72151968
        assert stats.ranked.forfeits == 0
        assert stats.ranked.completions == 40

        # Verify casual stats
        assert stats.casual.wins == 10
        assert stats.casual.losses == 5
        assert stats.casual.best_time is None
        assert stats.casual.played_matches == 15

    def test_already_correct_format_passthrough(self):
        """Test that already-correct format is not modified."""
        # This is the format we expect (mode-first)
        correct_data = {
            "ranked": {"wins": 55, "losses": 42, "best_time": 505888},
            "casual": {"wins": 10, "losses": 5},
        }

        stats = SeasonStats.model_validate(correct_data)

        assert stats.ranked.wins == 55
        assert stats.ranked.losses == 42
        assert stats.casual.wins == 10

    def test_empty_stats(self):
        """Test parsing empty/default stats."""
        stats = SeasonStats.model_validate({})

        assert stats.ranked.wins == 0
        assert stats.ranked.losses == 0
        assert stats.casual.wins == 0

    def test_partial_api_data(self):
        """Test parsing partial API data."""
        api_data = {
            "wins": {"ranked": 10},
            "loses": {"ranked": 5},
        }

        stats = SeasonStats.model_validate(api_data)

        assert stats.ranked.wins == 10
        assert stats.ranked.losses == 5
        assert stats.casual.wins == 0


class TestTotalStatsParsing:
    """Test that total stats are correctly parsed from API format."""

    def test_pivot_stats_from_api_format(self):
        """Test parsing API stat-first format to mode-first format."""
        api_data = {
            "wins": {"ranked": 3571, "casual": 76},
            "loses": {"ranked": 3238, "casual": 44},
            "bestTime": {"ranked": 503742, "casual": 663441},
            "playedMatches": {"ranked": 7035, "casual": 126},
        }

        stats = TotalStats.model_validate(api_data)

        assert stats.ranked.wins == 3571
        assert stats.ranked.losses == 3238
        assert stats.ranked.best_time == 503742
        assert stats.casual.wins == 76
        assert stats.casual.losses == 44


class TestMatchSeedParsing:
    """Test that match seed is correctly parsed."""

    def test_nether_field(self):
        """Test that nether field is parsed correctly."""
        api_data = {
            "id": "m723ang1dmwgfu9d",
            "overworld": "VILLAGE",
            "nether": "STABLES",
            "endTowers": [88, 94, 85, 91],
            "variations": ["bastion:good_gap:1"],
        }

        seed = MatchSeed.model_validate(api_data)

        assert seed.id == "m723ang1dmwgfu9d"
        assert seed.overworld == "VILLAGE"
        assert seed.nether == "STABLES"
        assert seed.bastion == "STABLES"  # Alias property
        assert seed.end_towers == [88, 94, 85, 91]

    def test_missing_nether(self):
        """Test parsing seed without nether field."""
        api_data = {
            "id": "test",
            "overworld": "VILLAGE",
        }

        seed = MatchSeed.model_validate(api_data)

        assert seed.nether is None
        assert seed.bastion is None

    def test_null_end_towers(self):
        """Test parsing seed with null endTowers (occurs in record leaderboard)."""
        api_data = {
            "id": "test",
            "overworld": "VILLAGE",
            "nether": "STABLES",
            "endTowers": None,
            "variations": [],
        }

        seed = MatchSeed.model_validate(api_data)

        assert seed.end_towers is None


class TestIntegrationWithRealAPI:
    """Integration tests that verify parsing works with real API data."""

    @pytest.mark.asyncio
    async def test_user_stats_from_real_api(self):
        """Test that user stats are correctly parsed from real API."""
        import mcsrranked

        # TapL is a well-known player with stats
        user = mcsrranked.users.get("TapL")

        # Should have non-zero stats (TapL has thousands of matches)
        assert (
            user.statistics.season.ranked.wins > 0
            or user.statistics.total.ranked.wins > 0
        )
        assert user.statistics.total.ranked.wins > 100  # TapL has 3500+ wins

    @pytest.mark.asyncio
    async def test_match_seed_from_real_api(self):
        """Test that match seed is correctly parsed from real API."""
        import mcsrranked

        matches = mcsrranked.matches.list(count=1, type=2)

        if matches:
            match = matches[0]
            if match.seed:
                # Seed should have overworld and nether (bastion) types
                assert match.seed.overworld is not None
                # nether might be None for some seeds, but the field should exist
                assert hasattr(match.seed, "nether")
                assert hasattr(match.seed, "bastion")
