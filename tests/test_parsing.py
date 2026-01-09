# mypy: disable-error-code="no-untyped-def"
"""Value assertion tests using real API fixtures."""

from mcsrranked.types.leaderboard import EloLeaderboard, PhaseLeaderboard, RecordEntry
from mcsrranked.types.live import LiveData
from mcsrranked.types.match import MatchInfo, VersusStats
from mcsrranked.types.user import User, UserSeasons
from mcsrranked.types.weekly_race import WeeklyRace


class TestUserParsing:
    """Test User type parsing from real API response."""

    def test_user_basic_fields(self, user_fixture):
        """Verify basic fields are parsed."""
        user = User.model_validate(user_fixture)

        assert user.uuid == "9a8e24df4c8549d696a6951da84fa5c4"
        assert user.nickname == "Feinberg"
        assert user.role_type == 3
        assert user.elo_rate == 2100
        assert user.elo_rank == 2
        assert user.country == "us"

    def test_user_statistics_season_ranked(self, user_fixture):
        """Verify season stats are parsed (not defaulting to 0)."""
        user = User.model_validate(user_fixture)

        # Feinberg has many matches, should not be 0
        assert user.statistics.season.ranked.wins > 0
        assert user.statistics.season.ranked.losses > 0
        assert user.statistics.season.ranked.played_matches > 0
        assert user.statistics.season.ranked.best_time is not None
        assert user.statistics.season.ranked.highest_winstreak > 0
        assert user.statistics.season.ranked.playtime > 0

        # Verify actual values from fixture
        assert user.statistics.season.ranked.wins == 57
        assert user.statistics.season.ranked.losses == 15
        assert user.statistics.season.ranked.played_matches == 73
        assert user.statistics.season.ranked.best_time == 408296

    def test_user_statistics_season_casual(self, user_fixture):
        """Verify casual season stats are parsed."""
        user = User.model_validate(user_fixture)

        # Feinberg has 0 casual games this season
        assert user.statistics.season.casual.wins == 0
        assert user.statistics.season.casual.losses == 0

    def test_user_statistics_total_ranked(self, user_fixture):
        """Verify total stats are parsed."""
        user = User.model_validate(user_fixture)

        # Feinberg has thousands of matches
        assert user.statistics.total.ranked.wins > 100
        assert user.statistics.total.ranked.losses > 100
        assert user.statistics.total.ranked.played_matches > 1000

        # Verify actual values from fixture
        assert user.statistics.total.ranked.wins == 1730
        assert user.statistics.total.ranked.losses == 921
        assert user.statistics.total.ranked.played_matches == 2684
        assert user.statistics.total.ranked.highest_winstreak == 29

    def test_user_statistics_total_casual(self, user_fixture):
        """Verify casual total stats are parsed."""
        user = User.model_validate(user_fixture)

        assert user.statistics.total.casual.wins == 6
        assert user.statistics.total.casual.losses == 4
        assert user.statistics.total.casual.best_time == 552108

    def test_user_achievements_display(self, user_fixture):
        """Verify display achievements are parsed."""
        user = User.model_validate(user_fixture)

        assert len(user.achievements.display) > 0

        # Check first achievement
        ach = user.achievements.display[0]
        assert ach.id is not None
        assert ach.date > 0
        assert ach.level >= 0

    def test_user_achievements_total(self, user_fixture):
        """Verify total achievements are parsed."""
        user = User.model_validate(user_fixture)

        assert len(user.achievements.total) > 0

        # Find an achievement with value/goal
        achievements_with_values = [
            a for a in user.achievements.total if a.value is not None
        ]
        assert len(achievements_with_values) > 0

        # Verify one with value
        ach = achievements_with_values[0]
        assert ach.value is not None
        assert ach.value > 0

    def test_user_connections(self, user_fixture):
        """Verify connections are parsed."""
        user = User.model_validate(user_fixture)

        # Feinberg has Discord, YouTube, and Twitch connected
        assert user.connections.discord is not None
        assert user.connections.discord.id == "75707773723086848"
        assert user.connections.discord.name == "Feinberg#0001"

        assert user.connections.youtube is not None
        assert user.connections.youtube.name == "Feinberg"

        assert user.connections.twitch is not None
        assert user.connections.twitch.id == "feinberg"

    def test_user_timestamps(self, user_fixture):
        """Verify timestamps are parsed."""
        user = User.model_validate(user_fixture)

        assert user.timestamp is not None
        assert user.timestamp.first_online > 0
        assert user.timestamp.last_online > 0
        assert user.timestamp.last_ranked is not None
        assert user.timestamp.next_decay is not None

    def test_user_season_result(self, user_fixture):
        """Verify season result is parsed."""
        user = User.model_validate(user_fixture)

        assert user.season_result is not None
        assert user.season_result.last is not None
        assert user.season_result.last.elo_rate == 2100
        assert user.season_result.last.elo_rank == 2
        assert user.season_result.highest == 2100
        assert user.season_result.lowest == 1623


class TestUserSeasonsParsing:
    """Test UserSeasons type parsing."""

    def test_user_seasons_basic_fields(self, user_seasons_fixture):
        """Verify basic fields are parsed."""
        seasons = UserSeasons.model_validate(user_seasons_fixture)

        assert seasons.uuid is not None
        assert seasons.nickname == "Feinberg"

    def test_user_seasons_results(self, user_seasons_fixture):
        """Verify season results dict is parsed."""
        seasons = UserSeasons.model_validate(user_seasons_fixture)

        # Should have multiple seasons
        assert len(seasons.season_results) > 0

        # Check a specific season
        for _season_num, result in seasons.season_results.items():
            assert result.last is not None
            # highest/lowest can be None if no ranked matches that season
            if result.highest is not None:
                assert isinstance(result.highest, int)


class TestMatchParsing:
    """Test MatchInfo type parsing."""

    def test_match_basic_fields(self, match_detail_fixture):
        """Verify basic fields are parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert match.id == 4816894
        assert match.type == 2  # Ranked
        assert match.season == 10
        assert match.date > 0
        assert match.category == "ANY"

    def test_match_players(self, match_detail_fixture):
        """Verify players are parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert len(match.players) == 2

        player = match.players[0]
        assert player.uuid is not None
        assert player.nickname is not None
        assert isinstance(player.role_type, int)

    def test_match_seed_fields(self, match_detail_fixture):
        """Verify seed is parsed correctly."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert match.seed is not None
        assert match.seed.id == "m723auzy73cgue8f"
        assert match.seed.overworld == "SHIPWRECK"
        assert match.seed.nether == "HOUSING"  # This was previously broken
        assert match.seed.bastion == "HOUSING"  # Alias should work
        assert match.seed.end_towers is not None
        assert len(match.seed.end_towers) == 4
        assert len(match.seed.variations) > 0

    def test_match_result(self, match_detail_fixture):
        """Verify result is parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert match.result is not None
        assert match.result.uuid is not None
        assert match.result.time > 0

    def test_match_changes(self, match_detail_fixture):
        """Verify elo changes are parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert len(match.changes) == 2

        for change in match.changes:
            assert change.uuid is not None
            assert change.change is not None
            assert change.elo_rate is not None

    def test_match_timelines(self, match_detail_fixture):
        """Verify timelines are parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert len(match.timelines) > 0

        timeline = match.timelines[0]
        assert timeline.uuid is not None
        assert timeline.time > 0
        assert timeline.type is not None

    def test_match_forfeited(self, match_detail_fixture):
        """Verify forfeited flag is parsed."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert match.forfeited is True  # This match was forfeited


class TestMatchListParsing:
    """Test parsing list of matches."""

    def test_matches_list(self, matches_fixture):
        """Verify list of matches parses correctly."""
        matches = [MatchInfo.model_validate(m) for m in matches_fixture]

        assert len(matches) == 5

        for match in matches:
            assert match.id > 0
            assert match.type == 2  # All ranked
            assert len(match.players) >= 1


class TestVersusStatsParsing:
    """Test VersusStats type parsing."""

    def test_versus_basic_fields(self, versus_fixture):
        """Verify basic fields are parsed."""
        versus = VersusStats.model_validate(versus_fixture)

        assert len(versus.players) == 2

    def test_versus_players(self, versus_fixture):
        """Verify players are parsed."""
        versus = VersusStats.model_validate(versus_fixture)

        player_names = {p.nickname for p in versus.players}
        assert "Feinberg" in player_names
        assert "Couriway" in player_names

    def test_versus_results(self, versus_fixture):
        """Verify results are parsed."""
        versus = VersusStats.model_validate(versus_fixture)

        assert "total" in versus.results.ranked
        assert "total" in versus.results.casual

    def test_versus_changes(self, versus_fixture):
        """Verify changes are parsed."""
        versus = VersusStats.model_validate(versus_fixture)

        # Feinberg vs Couriway have 0 matches so 0 changes
        assert len(versus.changes) == 2


class TestLeaderboardParsing:
    """Test leaderboard type parsing."""

    def test_elo_leaderboard_season(self, leaderboard_fixture):
        """Verify season info is parsed."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        assert lb.season.number == 10
        assert lb.season.starts_at > 0
        assert lb.season.ends_at > 0

    def test_elo_leaderboard_users(self, leaderboard_fixture):
        """Verify users are parsed."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        assert len(lb.users) > 0

        # Check top user
        top_user = lb.users[0]
        assert top_user.uuid is not None
        assert top_user.nickname is not None
        assert top_user.elo_rate is not None
        assert top_user.elo_rank == 1
        assert top_user.season_result is not None
        assert top_user.season_result.elo_rate > 0

    def test_elo_leaderboard_has_feinberg(self, leaderboard_fixture):
        """Verify Feinberg is in leaderboard."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        feinberg = next((u for u in lb.users if u.nickname == "Feinberg"), None)
        assert feinberg is not None
        assert feinberg.elo_rank == 2


class TestPhaseLeaderboardParsing:
    """Test phase leaderboard parsing."""

    def test_phase_leaderboard_phase(self, phase_leaderboard_fixture):
        """Verify phase info is parsed."""
        lb = PhaseLeaderboard.model_validate(phase_leaderboard_fixture)

        assert lb.phase.season is not None

    def test_phase_leaderboard_users(self, phase_leaderboard_fixture):
        """Verify users are parsed."""
        lb = PhaseLeaderboard.model_validate(phase_leaderboard_fixture)

        if len(lb.users) > 0:
            user = lb.users[0]
            assert user.uuid is not None
            assert user.season_result is not None


class TestRecordLeaderboardParsing:
    """Test record leaderboard parsing."""

    def test_record_entries(self, record_leaderboard_fixture):
        """Verify record entries are parsed."""
        records = [RecordEntry.model_validate(r) for r in record_leaderboard_fixture]

        assert len(records) > 0

        record = records[0]
        assert record.rank == 1
        assert record.time > 0
        assert record.id > 0
        assert record.user is not None
        assert record.user.nickname is not None

    def test_record_seed(self, record_leaderboard_fixture):
        """Verify record seed is parsed."""
        records = [RecordEntry.model_validate(r) for r in record_leaderboard_fixture]

        # Find a record with seed
        record_with_seed = next((r for r in records if r.seed is not None), None)
        if record_with_seed:
            assert record_with_seed.seed is not None
            assert record_with_seed.seed.overworld is not None
            # end_towers can be None for some seeds
            if record_with_seed.seed.end_towers is not None:
                assert isinstance(record_with_seed.seed.end_towers, list)


class TestLiveParsing:
    """Test LiveData type parsing."""

    def test_live_basic_fields(self, live_fixture):
        """Verify basic fields are parsed."""
        live = LiveData.model_validate(live_fixture)

        assert live.players > 0  # Should have some concurrent players
        assert isinstance(live.live_matches, list)

    def test_live_matches(self, live_fixture):
        """Verify live matches are parsed."""
        live = LiveData.model_validate(live_fixture)

        if len(live.live_matches) > 0:
            match = live.live_matches[0]
            assert match.current_time >= 0
            assert isinstance(match.players, list)
            assert isinstance(match.data, dict)

    def test_live_match_players(self, live_fixture):
        """Verify live match players are parsed."""
        live = LiveData.model_validate(live_fixture)

        if len(live.live_matches) > 0:
            match = live.live_matches[0]
            if len(match.players) > 0:
                player = match.players[0]
                assert player.uuid is not None
                assert player.nickname is not None

    def test_live_match_data(self, live_fixture):
        """Verify live match data (player timelines) are parsed."""
        live = LiveData.model_validate(live_fixture)

        if len(live.live_matches) > 0:
            match = live.live_matches[0]
            if match.data:
                for _uuid, player_data in match.data.items():
                    # live_url can be None or a string
                    assert player_data.live_url is None or isinstance(
                        player_data.live_url, str
                    )
                    # timeline can be None or have time/type
                    if player_data.timeline is not None:
                        assert player_data.timeline.time >= 0
                        assert player_data.timeline.type is not None


class TestWeeklyRaceParsing:
    """Test WeeklyRace type parsing."""

    def test_weekly_race_basic_fields(self, weekly_race_fixture):
        """Verify basic fields are parsed."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        assert race.id > 0
        assert race.ends_at > 0

    def test_weekly_race_seed(self, weekly_race_fixture):
        """Verify seed is parsed."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        assert race.seed is not None
        assert race.seed.overworld is not None  # Weekly race uses numeric seed strings

    def test_weekly_race_leaderboard(self, weekly_race_fixture):
        """Verify leaderboard is parsed."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        assert len(race.leaderboard) > 0

        entry = race.leaderboard[0]
        assert entry.rank == 1
        assert entry.time > 0
        assert entry.player is not None
        assert entry.player.nickname is not None

    def test_weekly_race_leaderboard_players(self, weekly_race_fixture):
        """Verify leaderboard player profiles are parsed."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        for entry in race.leaderboard[:5]:  # Check first 5
            assert entry.player.uuid is not None
            # elo_rate can be None (placement matches)
            # elo_rank can be None
