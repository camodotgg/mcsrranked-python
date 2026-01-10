# mypy: disable-error-code="no-untyped-def"
"""Tests to ensure model fields match API fixture fields."""

import pytest
from pydantic import BaseModel

from mcsrranked.types.leaderboard import (
    EloLeaderboard,
    LeaderboardSeasonResult,
    LeaderboardUser,
    PhaseInfo,
    PhaseLeaderboard,
    PhaseLeaderboardUser,
    RecordEntry,
    SeasonInfo,
)
from mcsrranked.types.live import (
    LiveData,
    LiveMatch,
    LivePlayerData,
    LivePlayerTimeline,
    UserLiveMatch,
)
from mcsrranked.types.match import (
    Completion,
    MatchInfo,
    MatchRank,
    MatchResult,
    Timeline,
    VersusResults,
    VersusStats,
)
from mcsrranked.types.shared import (
    Achievement,
    EloChange,
    MatchSeed,
    UserProfile,
    VodInfo,
)
from mcsrranked.types.user import (
    Connection,
    LastSeasonState,
    MatchTypeStats,
    PhaseResult,
    SeasonResult,
    SeasonResultEntry,
    User,
    UserConnections,
    UserSeasons,
    UserStatistics,
    UserTimestamps,
    WeeklyRaceResult,
)
from mcsrranked.types.weekly_race import (
    RaceLeaderboardEntry,
    WeeklyRace,
    WeeklyRaceSeed,
)


def get_model_aliases(model: type[BaseModel]) -> set[str]:
    """Get all field aliases for a model."""
    aliases = set()
    for name, field in model.model_fields.items():
        alias = field.alias or name
        aliases.add(alias)
    return aliases


def check_parity(
    model: type[BaseModel],
    fixture_data: dict[str, object],
    optional_fields: set[str] | None = None,
) -> tuple[set[str], set[str]]:
    """Check field parity between model and fixture.

    Returns:
        (missing_from_model, not_in_fixture)
    """
    optional_fields = optional_fields or set()
    model_aliases = get_model_aliases(model)
    api_keys = set(fixture_data.keys())

    missing_from_model = api_keys - model_aliases
    not_in_fixture = model_aliases - api_keys - optional_fields

    return missing_from_model, not_in_fixture


class TestUserFixtureParity:
    """Verify User models match user.json fixture."""

    def test_user_parity(self, user_fixture):
        missing, extra = check_parity(User, user_fixture)
        assert not missing, f"Fields in API but not in User model: {missing}"
        assert not extra, f"Fields in User model but not in API: {extra}"

    def test_user_timestamps_parity(self, user_fixture):
        missing, extra = check_parity(UserTimestamps, user_fixture["timestamp"])
        assert not missing, f"Missing from UserTimestamps: {missing}"
        assert not extra, f"Extra in UserTimestamps: {extra}"

    def test_user_connections_parity(self, user_fixture):
        missing, extra = check_parity(UserConnections, user_fixture["connections"])
        assert not missing, f"Missing from UserConnections: {missing}"
        assert not extra, f"Extra in UserConnections: {extra}"

    def test_connection_parity(self, user_fixture):
        missing, extra = check_parity(
            Connection, user_fixture["connections"]["discord"]
        )
        assert not missing, f"Missing from Connection: {missing}"
        assert not extra, f"Extra in Connection: {extra}"

    def test_season_result_parity(self, user_fixture):
        missing, extra = check_parity(SeasonResult, user_fixture["seasonResult"])
        assert not missing, f"Missing from SeasonResult: {missing}"
        assert not extra, f"Extra in SeasonResult: {extra}"

    def test_last_season_state_parity(self, user_fixture):
        missing, extra = check_parity(
            LastSeasonState, user_fixture["seasonResult"]["last"]
        )
        assert not missing, f"Missing from LastSeasonState: {missing}"
        assert not extra, f"Extra in LastSeasonState: {extra}"

    def test_achievement_parity(self, user_fixture):
        missing, extra = check_parity(
            Achievement, user_fixture["achievements"]["display"][0]
        )
        assert not missing, f"Missing from Achievement: {missing}"
        assert not extra, f"Extra in Achievement: {extra}"


class TestUserSeasonsFixtureParity:
    """Verify UserSeasons models match user_seasons.json fixture."""

    def test_user_seasons_parity(self, user_seasons_fixture):
        missing, extra = check_parity(UserSeasons, user_seasons_fixture)
        assert not missing, f"Missing from UserSeasons: {missing}"
        assert not extra, f"Extra in UserSeasons: {extra}"

    def test_season_result_entry_parity(self, user_seasons_fixture):
        # Get first season result entry
        for entry in user_seasons_fixture["seasonResults"].values():
            missing, extra = check_parity(SeasonResultEntry, entry)
            assert not missing, f"Missing from SeasonResultEntry: {missing}"
            assert not extra, f"Extra in SeasonResultEntry: {extra}"
            break

    def test_phase_result_parity(self, user_seasons_fixture):
        # Find a season with phases
        for entry in user_seasons_fixture["seasonResults"].values():
            if entry.get("phases"):
                missing, extra = check_parity(PhaseResult, entry["phases"][0])
                assert not missing, f"Missing from PhaseResult: {missing}"
                assert not extra, f"Extra in PhaseResult: {extra}"
                return
        pytest.skip("No phases in fixture")


class TestMatchTypeStatsParity:
    """Verify MatchTypeStats pivot mapping matches API."""

    def test_pivot_mapping_covers_all_api_fields(self, user_fixture):
        """Ensure _pivot_stats mapping includes all API statistics fields."""
        # Collect all unique stat keys from API
        api_stats_keys = set()
        for section in ["season", "total"]:
            for key in user_fixture["statistics"][section]:
                api_stats_keys.add(key)

        # Current mapping in _pivot_stats (must match user.py)
        mapped_keys = {
            "wins",
            "loses",
            "forfeits",
            "completions",
            "playtime",
            "completionTime",
            "bestTime",
            "playedMatches",
            "currentWinStreak",
            "highestWinStreak",
        }

        missing = api_stats_keys - mapped_keys
        assert not missing, f"API stats fields not in _pivot_stats mapping: {missing}"

    def test_match_type_stats_model_fields(self, user_fixture):
        """Ensure MatchTypeStats model can parse pivoted stats."""
        user = User.model_validate(user_fixture)
        mts = user.statistics.season.ranked

        # Verify all model fields are accessible (not hallucinated)
        model_aliases = get_model_aliases(MatchTypeStats)
        # These are the expected aliases after pivot transformation
        expected_aliases = {
            "playedMatches",
            "wins",
            "losses",  # Note: API 'loses' maps to model 'losses'
            "forfeits",
            "highestWinStreak",
            "currentWinStreak",
            "playtime",
            "completionTime",
            "bestTime",
            "completions",
        }

        extra = model_aliases - expected_aliases
        assert not extra, f"MatchTypeStats has unmapped fields: {extra}"

        # Verify the model actually parsed the data
        assert isinstance(mts.played_matches, int)
        assert isinstance(mts.wins, int)
        assert isinstance(mts.losses, int)
        assert isinstance(mts.completion_time, int)


class TestMatchFixtureParity:
    """Verify Match models match match_detail.json fixture."""

    def test_match_info_parity(self, match_detail_fixture):
        # completions, timelines, replayExist are detail-only (optional in list endpoints)
        missing, extra = check_parity(
            MatchInfo,
            match_detail_fixture,
            optional_fields={"completions", "timelines", "replayExist"},
        )
        assert not missing, f"Missing from MatchInfo: {missing}"
        assert not extra, f"Extra in MatchInfo: {extra}"

    def test_match_result_parity(self, match_detail_fixture):
        missing, extra = check_parity(MatchResult, match_detail_fixture["result"])
        assert not missing, f"Missing from MatchResult: {missing}"
        assert not extra, f"Extra in MatchResult: {extra}"

    def test_match_seed_parity(self, match_detail_fixture):
        seed = match_detail_fixture.get("info", {}).get("seed")
        if seed:
            missing, extra = check_parity(MatchSeed, seed)
            assert not missing, f"Missing from MatchSeed: {missing}"
            assert not extra, f"Extra in MatchSeed: {extra}"

    def test_match_rank_parity(self, match_detail_fixture):
        rank = match_detail_fixture.get("rank")
        if rank:
            missing, extra = check_parity(MatchRank, rank)
            assert not missing, f"Missing from MatchRank: {missing}"
            assert not extra, f"Extra in MatchRank: {extra}"

    def test_timeline_parity(self, match_detail_fixture):
        timelines = match_detail_fixture.get("timelines", [])
        if timelines:
            missing, extra = check_parity(Timeline, timelines[0])
            assert not missing, f"Missing from Timeline: {missing}"
            assert not extra, f"Extra in Timeline: {extra}"

    def test_elo_change_parity(self, match_detail_fixture):
        changes = match_detail_fixture.get("changes", [])
        if changes:
            missing, extra = check_parity(EloChange, changes[0])
            assert not missing, f"Missing from EloChange: {missing}"
            assert not extra, f"Extra in EloChange: {extra}"

    def test_completion_parity(self, match_detail_fixture):
        completions = match_detail_fixture.get("completions", [])
        if completions:
            missing, extra = check_parity(Completion, completions[0])
            assert not missing, f"Missing from Completion: {missing}"
            assert not extra, f"Extra in Completion: {extra}"


class TestLeaderboardFixtureParity:
    """Verify Leaderboard models match leaderboard.json fixture."""

    def test_elo_leaderboard_parity(self, leaderboard_fixture):
        missing, extra = check_parity(EloLeaderboard, leaderboard_fixture)
        assert not missing, f"Missing from EloLeaderboard: {missing}"
        assert not extra, f"Extra in EloLeaderboard: {extra}"

    def test_season_info_parity(self, leaderboard_fixture):
        missing, extra = check_parity(SeasonInfo, leaderboard_fixture["season"])
        assert not missing, f"Missing from SeasonInfo: {missing}"
        assert not extra, f"Extra in SeasonInfo: {extra}"

    def test_leaderboard_user_parity(self, leaderboard_fixture):
        if leaderboard_fixture["users"]:
            missing, extra = check_parity(
                LeaderboardUser, leaderboard_fixture["users"][0]
            )
            assert not missing, f"Missing from LeaderboardUser: {missing}"
            assert not extra, f"Extra in LeaderboardUser: {extra}"

    def test_leaderboard_season_result_parity(self, leaderboard_fixture):
        if leaderboard_fixture["users"]:
            missing, extra = check_parity(
                LeaderboardSeasonResult,
                leaderboard_fixture["users"][0]["seasonResult"],
            )
            assert not missing, f"Missing from LeaderboardSeasonResult: {missing}"
            assert not extra, f"Extra in LeaderboardSeasonResult: {extra}"


class TestPhaseLeaderboardFixtureParity:
    """Verify PhaseLeaderboard models match phase_leaderboard.json fixture."""

    def test_phase_leaderboard_parity(self, phase_leaderboard_fixture):
        missing, extra = check_parity(PhaseLeaderboard, phase_leaderboard_fixture)
        assert not missing, f"Missing from PhaseLeaderboard: {missing}"
        assert not extra, f"Extra in PhaseLeaderboard: {extra}"

    def test_phase_info_parity(self, phase_leaderboard_fixture):
        missing, extra = check_parity(PhaseInfo, phase_leaderboard_fixture["phase"])
        assert not missing, f"Missing from PhaseInfo: {missing}"
        assert not extra, f"Extra in PhaseInfo: {extra}"

    def test_phase_leaderboard_user_parity(self, phase_leaderboard_fixture):
        if phase_leaderboard_fixture["users"]:
            # predPhasePoint may not appear if no predictions yet
            missing, extra = check_parity(
                PhaseLeaderboardUser,
                phase_leaderboard_fixture["users"][0],
                optional_fields={"predPhasePoint"},
            )
            assert not missing, f"Missing from PhaseLeaderboardUser: {missing}"
            assert not extra, f"Extra in PhaseLeaderboardUser: {extra}"


class TestRecordLeaderboardFixtureParity:
    """Verify RecordEntry model matches record_leaderboard.json fixture."""

    def test_record_entry_parity(self, record_leaderboard_fixture):
        if record_leaderboard_fixture:
            missing, extra = check_parity(RecordEntry, record_leaderboard_fixture[0])
            assert not missing, f"Missing from RecordEntry: {missing}"
            assert not extra, f"Extra in RecordEntry: {extra}"

    def test_record_seed_parity(self, record_leaderboard_fixture):
        if record_leaderboard_fixture and record_leaderboard_fixture[0].get("seed"):
            missing, extra = check_parity(
                MatchSeed, record_leaderboard_fixture[0]["seed"]
            )
            assert not missing, f"Missing from MatchSeed (record): {missing}"
            assert not extra, f"Extra in MatchSeed (record): {extra}"


class TestLiveFixtureParity:
    """Verify Live models match live.json fixture."""

    def test_live_data_parity(self, live_fixture):
        missing, extra = check_parity(LiveData, live_fixture)
        assert not missing, f"Missing from LiveData: {missing}"
        assert not extra, f"Extra in LiveData: {extra}"

    def test_live_match_parity(self, live_fixture):
        if live_fixture["liveMatches"]:
            missing, extra = check_parity(LiveMatch, live_fixture["liveMatches"][0])
            assert not missing, f"Missing from LiveMatch: {missing}"
            assert not extra, f"Extra in LiveMatch: {extra}"

    def test_live_player_data_parity(self, live_fixture):
        if live_fixture["liveMatches"]:
            match = live_fixture["liveMatches"][0]
            if match["data"]:
                player_data = next(iter(match["data"].values()))
                missing, extra = check_parity(LivePlayerData, player_data)
                assert not missing, f"Missing from LivePlayerData: {missing}"
                assert not extra, f"Extra in LivePlayerData: {extra}"

    def test_live_player_timeline_parity(self, live_fixture):
        for match in live_fixture.get("liveMatches", []):
            for player_data in match.get("data", {}).values():
                if player_data.get("timeline"):
                    missing, extra = check_parity(
                        LivePlayerTimeline, player_data["timeline"]
                    )
                    assert not missing, f"Missing from LivePlayerTimeline: {missing}"
                    assert not extra, f"Extra in LivePlayerTimeline: {extra}"
                    return
        pytest.skip("No timeline in live fixture")


class TestWeeklyRaceFixtureParity:
    """Verify WeeklyRace models match weekly_race.json fixture."""

    def test_weekly_race_parity(self, weekly_race_fixture):
        missing, extra = check_parity(WeeklyRace, weekly_race_fixture)
        assert not missing, f"Missing from WeeklyRace: {missing}"
        assert not extra, f"Extra in WeeklyRace: {extra}"

    def test_weekly_race_seed_parity(self, weekly_race_fixture):
        missing, extra = check_parity(WeeklyRaceSeed, weekly_race_fixture["seed"])
        assert not missing, f"Missing from WeeklyRaceSeed: {missing}"
        assert not extra, f"Extra in WeeklyRaceSeed: {extra}"

    def test_race_leaderboard_entry_parity(self, weekly_race_fixture):
        if weekly_race_fixture["leaderboard"]:
            missing, extra = check_parity(
                RaceLeaderboardEntry, weekly_race_fixture["leaderboard"][0]
            )
            assert not missing, f"Missing from RaceLeaderboardEntry: {missing}"
            assert not extra, f"Extra in RaceLeaderboardEntry: {extra}"


class TestVersusFixtureParity:
    """Verify Versus models match versus.json fixture."""

    def test_versus_stats_parity(self, versus_fixture):
        missing, extra = check_parity(VersusStats, versus_fixture)
        assert not missing, f"Missing from VersusStats: {missing}"
        assert not extra, f"Extra in VersusStats: {extra}"

    def test_versus_results_parity(self, versus_fixture):
        missing, extra = check_parity(VersusResults, versus_fixture["results"])
        assert not missing, f"Missing from VersusResults: {missing}"
        assert not extra, f"Extra in VersusResults: {extra}"


class TestUserProfileParity:
    """Verify UserProfile matches across different fixtures."""

    def test_user_profile_in_match(self, match_detail_fixture):
        if match_detail_fixture["players"]:
            # UserProfile in match has extra nested fields we skip
            player = match_detail_fixture["players"][0]
            profile_keys = {
                k for k in player if k not in {"timeline", "completion", "eloChange"}
            }
            model_aliases = get_model_aliases(UserProfile)

            missing = profile_keys - model_aliases
            extra = model_aliases - profile_keys

            assert not missing, f"Missing from UserProfile: {missing}"
            assert not extra, f"Extra in UserProfile: {extra}"

    def test_user_profile_in_leaderboard(self, leaderboard_fixture):
        if leaderboard_fixture["users"]:
            # LeaderboardUser extends UserProfile, check base fields exist
            profile_keys = {
                "uuid",
                "nickname",
                "roleType",
                "eloRate",
                "eloRank",
                "country",
            }
            model_aliases = get_model_aliases(UserProfile)

            missing = profile_keys - model_aliases
            assert not missing, f"Missing from UserProfile: {missing}"


class TestUserStatisticsParity:
    """Verify UserStatistics model structure."""

    def test_user_statistics_contains_season_and_total(self, user_fixture):
        """Ensure UserStatistics has expected nested structure."""
        user = User.model_validate(user_fixture)
        stats = user.statistics

        assert isinstance(stats, UserStatistics)
        # Verify the nested structure exists
        assert hasattr(stats, "season")
        assert hasattr(stats, "total")


class TestWeeklyRaceResultParity:
    """Verify WeeklyRaceResult model structure."""

    def test_weekly_race_result_fields(self):
        """Ensure WeeklyRaceResult has all expected fields."""
        model_aliases = get_model_aliases(WeeklyRaceResult)
        expected = {"id", "time", "rank"}

        assert (
            model_aliases == expected
        ), f"WeeklyRaceResult aliases mismatch: {model_aliases}"


class TestVodInfoParity:
    """Verify VodInfo model structure."""

    def test_vod_info_fields(self):
        """Ensure VodInfo has all expected fields."""
        model_aliases = get_model_aliases(VodInfo)
        expected = {"uuid", "url", "startsAt"}

        assert model_aliases == expected, f"VodInfo aliases mismatch: {model_aliases}"


class TestUserLiveMatchParity:
    """Verify UserLiveMatch model structure."""

    def test_user_live_match_fields(self):
        """Ensure UserLiveMatch has all expected fields."""
        model_aliases = get_model_aliases(UserLiveMatch)
        expected = {
            "lastId",
            "type",
            "status",
            "time",
            "players",
            "spectators",
            "timelines",
            "completions",
        }

        assert (
            model_aliases == expected
        ), f"UserLiveMatch aliases mismatch: {model_aliases}"
