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
    AchievementsContainer,
    Connection,
    LastSeasonState,
    MatchTypeStats,
    PhaseResult,
    SeasonResult,
    SeasonResultEntry,
    SeasonStats,
    TotalStats,
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


class TestUserFieldCoverage:
    """Test every field in User and related types."""

    def test_user_all_fields(self, user_fixture):
        """Verify all User fields are accessible."""
        user = User.model_validate(user_fixture)

        # User fields
        assert isinstance(user.uuid, str)
        assert isinstance(user.nickname, str)
        assert isinstance(user.role_type, int)
        assert user.elo_rate is None or isinstance(user.elo_rate, int)
        assert user.elo_rank is None or isinstance(user.elo_rank, int)
        assert user.country is None or isinstance(user.country, str)
        assert isinstance(user.achievements, AchievementsContainer)
        assert user.timestamp is None or isinstance(user.timestamp, UserTimestamps)
        assert isinstance(user.statistics, UserStatistics)
        assert isinstance(user.connections, UserConnections)
        assert user.season_result is None or isinstance(
            user.season_result, SeasonResult
        )
        assert isinstance(user.weekly_races, list)

    def test_user_timestamps_all_fields(self, user_fixture):
        """Verify all UserTimestamps fields."""
        user = User.model_validate(user_fixture)
        ts = user.timestamp

        assert ts is not None
        assert isinstance(ts.first_online, int)
        assert isinstance(ts.last_online, int)
        assert ts.last_ranked is None or isinstance(ts.last_ranked, int)
        assert ts.next_decay is None or isinstance(ts.next_decay, int)

    def test_user_statistics_all_fields(self, user_fixture):
        """Verify all UserStatistics fields."""
        user = User.model_validate(user_fixture)
        stats = user.statistics

        assert isinstance(stats.season, SeasonStats)
        assert isinstance(stats.total, TotalStats)
        assert isinstance(stats.season.ranked, MatchTypeStats)
        assert isinstance(stats.season.casual, MatchTypeStats)
        assert isinstance(stats.total.ranked, MatchTypeStats)
        assert isinstance(stats.total.casual, MatchTypeStats)

    def test_match_type_stats_all_fields(self, user_fixture):
        """Verify all MatchTypeStats fields."""
        user = User.model_validate(user_fixture)
        mts = user.statistics.season.ranked

        assert isinstance(mts.played_matches, int)
        assert isinstance(mts.wins, int)
        assert isinstance(mts.losses, int)
        assert isinstance(mts.draws, int)
        assert isinstance(mts.forfeits, int)
        assert isinstance(mts.highest_winstreak, int)
        assert isinstance(mts.current_winstreak, int)
        assert isinstance(mts.playtime, int)
        assert mts.best_time is None or isinstance(mts.best_time, int)
        assert mts.best_time_id is None or isinstance(mts.best_time_id, int)
        assert isinstance(mts.completions, int)

    def test_season_result_all_fields(self, user_fixture):
        """Verify all SeasonResult fields."""
        user = User.model_validate(user_fixture)
        sr = user.season_result

        assert sr is not None
        assert isinstance(sr.last, LastSeasonState)
        assert sr.highest is None or isinstance(sr.highest, int)
        assert sr.lowest is None or isinstance(sr.lowest, int)
        assert isinstance(sr.phases, list)

    def test_last_season_state_all_fields(self, user_fixture):
        """Verify all LastSeasonState fields."""
        user = User.model_validate(user_fixture)
        last = user.season_result.last

        assert last.elo_rate is None or isinstance(last.elo_rate, int)
        assert last.elo_rank is None or isinstance(last.elo_rank, int)
        assert last.phase_point is None or isinstance(last.phase_point, int)

    def test_connection_all_fields(self, user_fixture):
        """Verify all Connection fields."""
        user = User.model_validate(user_fixture)

        # Feinberg has discord connected
        if user.connections.discord:
            assert isinstance(user.connections.discord.id, str)
            assert isinstance(user.connections.discord.name, str)

    def test_user_connections_all_fields(self, user_fixture):
        """Verify all UserConnections fields."""
        user = User.model_validate(user_fixture)
        conn = user.connections

        assert conn.discord is None or isinstance(conn.discord, Connection)
        assert conn.twitch is None or isinstance(conn.twitch, Connection)
        assert conn.youtube is None or isinstance(conn.youtube, Connection)

    def test_achievements_container_all_fields(self, user_fixture):
        """Verify all AchievementsContainer fields."""
        user = User.model_validate(user_fixture)
        ach = user.achievements

        assert isinstance(ach.display, list)
        assert isinstance(ach.total, list)

    def test_achievement_all_fields(self, user_fixture):
        """Verify all Achievement fields."""
        user = User.model_validate(user_fixture)

        if user.achievements.display:
            a = user.achievements.display[0]
            assert isinstance(a, Achievement)
            assert isinstance(a.id, str)
            assert isinstance(a.date, int)
            assert isinstance(a.data, list)
            assert isinstance(a.level, int)
            assert a.value is None or isinstance(a.value, int)
            assert a.goal is None or isinstance(a.goal, int)


class TestUserSeasonsFieldCoverage:
    """Test every field in UserSeasons and related types."""

    def test_user_seasons_all_fields(self, user_seasons_fixture):
        """Verify all UserSeasons fields."""
        seasons = UserSeasons.model_validate(user_seasons_fixture)

        assert isinstance(seasons.uuid, str)
        assert isinstance(seasons.nickname, str)
        assert isinstance(seasons.role_type, int)
        assert seasons.elo_rate is None or isinstance(seasons.elo_rate, int)
        assert seasons.elo_rank is None or isinstance(seasons.elo_rank, int)
        assert seasons.country is None or isinstance(seasons.country, str)
        assert isinstance(seasons.season_results, dict)

    def test_season_result_entry_all_fields(self, user_seasons_fixture):
        """Verify all SeasonResultEntry fields."""
        seasons = UserSeasons.model_validate(user_seasons_fixture)

        for _season_num, entry in seasons.season_results.items():
            assert isinstance(entry, SeasonResultEntry)
            assert isinstance(entry.last, LastSeasonState)
            assert entry.highest is None or isinstance(entry.highest, int | float)
            assert entry.lowest is None or isinstance(entry.lowest, int | float)
            assert isinstance(entry.phases, list)


class TestMatchFieldCoverage:
    """Test every field in Match and related types."""

    def test_match_info_all_fields(self, match_detail_fixture):
        """Verify all MatchInfo fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        assert isinstance(match.id, int)
        assert isinstance(match.type, int)
        assert isinstance(match.season, int)
        assert match.category is None or isinstance(match.category, str)
        assert isinstance(match.date, int)
        assert isinstance(match.players, list)
        assert isinstance(match.spectators, list)
        assert match.seed is None or isinstance(match.seed, MatchSeed)
        assert match.result is None or isinstance(match.result, MatchResult)
        assert isinstance(match.forfeited, bool)
        assert isinstance(match.decayed, bool)
        assert match.rank is None or isinstance(match.rank, MatchRank)
        assert isinstance(match.changes, list)
        assert match.tag is None or isinstance(match.tag, str)
        assert isinstance(match.beginner, bool)
        assert isinstance(match.vod, list)
        assert isinstance(match.completions, list)
        assert isinstance(match.timelines, list)
        assert isinstance(match.replay_exist, bool)

    def test_match_result_all_fields(self, match_detail_fixture):
        """Verify all MatchResult fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.result:
            assert match.result.uuid is None or isinstance(match.result.uuid, str)
            assert isinstance(match.result.time, int)

    def test_match_rank_all_fields(self, match_detail_fixture):
        """Verify all MatchRank fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.rank:
            assert match.rank.season is None or isinstance(match.rank.season, int)
            assert match.rank.all_time is None or isinstance(match.rank.all_time, int)

    def test_timeline_all_fields(self, match_detail_fixture):
        """Verify all Timeline fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.timelines:
            tl = match.timelines[0]
            assert isinstance(tl, Timeline)
            assert isinstance(tl.uuid, str)
            assert isinstance(tl.time, int)
            assert isinstance(tl.type, str)

    def test_completion_all_fields(self, match_detail_fixture):
        """Verify all Completion fields (from match with completions)."""
        match = MatchInfo.model_validate(match_detail_fixture)

        # This match was forfeited so no completions
        # Test the type definition instead
        if match.completions:
            c = match.completions[0]
            assert isinstance(c.uuid, str)
            assert isinstance(c.time, int)

    def test_elo_change_all_fields(self, match_detail_fixture):
        """Verify all EloChange fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.changes:
            ec = match.changes[0]
            assert isinstance(ec, EloChange)
            assert isinstance(ec.uuid, str)
            assert ec.change is None or isinstance(ec.change, int)
            assert ec.elo_rate is None or isinstance(ec.elo_rate, int)

    def test_match_seed_all_fields(self, match_detail_fixture):
        """Verify all MatchSeed fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.seed:
            s = match.seed
            assert s.id is None or isinstance(s.id, str)
            assert s.overworld is None or isinstance(s.overworld, str)
            assert s.nether is None or isinstance(s.nether, str)
            assert s.end_towers is None or isinstance(s.end_towers, list)
            assert isinstance(s.variations, list)
            # Test the bastion property alias
            assert s.bastion == s.nether

    def test_user_profile_all_fields(self, match_detail_fixture):
        """Verify all UserProfile fields."""
        match = MatchInfo.model_validate(match_detail_fixture)

        if match.players:
            p = match.players[0]
            assert isinstance(p.uuid, str)
            assert isinstance(p.nickname, str)
            assert isinstance(p.role_type, int)
            assert p.elo_rate is None or isinstance(p.elo_rate, int)
            assert p.elo_rank is None or isinstance(p.elo_rank, int)
            assert p.country is None or isinstance(p.country, str)


class TestVersusFieldCoverage:
    """Test every field in Versus types."""

    def test_versus_stats_all_fields(self, versus_fixture):
        """Verify all VersusStats fields."""
        vs = VersusStats.model_validate(versus_fixture)

        assert isinstance(vs.players, list)
        assert isinstance(vs.results, VersusResults)
        assert isinstance(vs.changes, dict)

    def test_versus_results_all_fields(self, versus_fixture):
        """Verify all VersusResults fields."""
        vs = VersusStats.model_validate(versus_fixture)

        assert isinstance(vs.results.ranked, dict)
        assert isinstance(vs.results.casual, dict)


class TestLeaderboardFieldCoverage:
    """Test every field in Leaderboard types."""

    def test_elo_leaderboard_all_fields(self, leaderboard_fixture):
        """Verify all EloLeaderboard fields."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        assert isinstance(lb.season, SeasonInfo)
        assert isinstance(lb.users, list)

    def test_season_info_all_fields(self, leaderboard_fixture):
        """Verify all SeasonInfo fields."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        assert isinstance(lb.season.number, int)
        assert isinstance(lb.season.starts_at, int)
        assert isinstance(lb.season.ends_at, int)

    def test_leaderboard_user_all_fields(self, leaderboard_fixture):
        """Verify all LeaderboardUser fields."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        if lb.users:
            u = lb.users[0]
            assert isinstance(u, LeaderboardUser)
            assert isinstance(u.uuid, str)
            assert isinstance(u.nickname, str)
            assert isinstance(u.role_type, int)
            assert u.elo_rate is None or isinstance(u.elo_rate, int)
            assert u.elo_rank is None or isinstance(u.elo_rank, int)
            assert u.country is None or isinstance(u.country, str)
            assert isinstance(u.season_result, LeaderboardSeasonResult)

    def test_leaderboard_season_result_all_fields(self, leaderboard_fixture):
        """Verify all LeaderboardSeasonResult fields."""
        lb = EloLeaderboard.model_validate(leaderboard_fixture)

        if lb.users:
            sr = lb.users[0].season_result
            assert isinstance(sr.elo_rate, int)
            assert isinstance(sr.elo_rank, int)
            assert isinstance(sr.phase_point, int)

    def test_phase_leaderboard_all_fields(self, phase_leaderboard_fixture):
        """Verify all PhaseLeaderboard fields."""
        lb = PhaseLeaderboard.model_validate(phase_leaderboard_fixture)

        assert isinstance(lb.phase, PhaseInfo)
        assert isinstance(lb.users, list)

    def test_phase_info_all_fields(self, phase_leaderboard_fixture):
        """Verify all PhaseInfo fields."""
        lb = PhaseLeaderboard.model_validate(phase_leaderboard_fixture)

        assert isinstance(lb.phase.season, int)
        assert lb.phase.number is None or isinstance(lb.phase.number, int)
        assert lb.phase.ends_at is None or isinstance(lb.phase.ends_at, int)

    def test_phase_leaderboard_user_all_fields(self, phase_leaderboard_fixture):
        """Verify all PhaseLeaderboardUser fields."""
        lb = PhaseLeaderboard.model_validate(phase_leaderboard_fixture)

        if lb.users:
            u = lb.users[0]
            assert isinstance(u, PhaseLeaderboardUser)
            assert isinstance(u.uuid, str)
            assert isinstance(u.nickname, str)
            assert isinstance(u.season_result, LeaderboardSeasonResult)
            assert isinstance(u.pred_phase_point, int)

    def test_record_entry_all_fields(self, record_leaderboard_fixture):
        """Verify all RecordEntry fields."""
        records = [RecordEntry.model_validate(r) for r in record_leaderboard_fixture]

        if records:
            r = records[0]
            assert isinstance(r.rank, int)
            assert isinstance(r.season, int)
            assert isinstance(r.date, int)
            assert isinstance(r.id, int)
            assert isinstance(r.time, int)
            assert isinstance(r.user, UserProfile)
            assert r.seed is None or isinstance(r.seed, MatchSeed)


class TestLiveFieldCoverage:
    """Test every field in Live types."""

    def test_live_data_all_fields(self, live_fixture):
        """Verify all LiveData fields."""
        live = LiveData.model_validate(live_fixture)

        assert isinstance(live.players, int)
        assert isinstance(live.live_matches, list)

    def test_live_match_all_fields(self, live_fixture):
        """Verify all LiveMatch fields."""
        live = LiveData.model_validate(live_fixture)

        if live.live_matches:
            m = live.live_matches[0]
            assert isinstance(m, LiveMatch)
            assert isinstance(m.current_time, int)
            assert isinstance(m.players, list)
            assert isinstance(m.data, dict)

    def test_live_player_data_all_fields(self, live_fixture):
        """Verify all LivePlayerData fields."""
        live = LiveData.model_validate(live_fixture)

        if live.live_matches:
            m = live.live_matches[0]
            if m.data:
                uuid, pd = next(iter(m.data.items()))
                assert isinstance(pd, LivePlayerData)
                assert pd.live_url is None or isinstance(pd.live_url, str)
                assert pd.timeline is None or isinstance(
                    pd.timeline, LivePlayerTimeline
                )

    def test_live_player_timeline_all_fields(self, live_fixture):
        """Verify all LivePlayerTimeline fields."""
        live = LiveData.model_validate(live_fixture)

        # Find a match with a timeline
        for m in live.live_matches:
            for _uuid, pd in m.data.items():
                if pd.timeline:
                    assert isinstance(pd.timeline.time, int)
                    assert isinstance(pd.timeline.type, str)
                    return

        # If no timeline found, that's OK - it's nullable


class TestWeeklyRaceFieldCoverage:
    """Test every field in WeeklyRace types."""

    def test_weekly_race_all_fields(self, weekly_race_fixture):
        """Verify all WeeklyRace fields."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        assert isinstance(race.id, int)
        assert isinstance(race.seed, WeeklyRaceSeed)
        assert isinstance(race.ends_at, int)
        assert isinstance(race.leaderboard, list)

    def test_weekly_race_seed_all_fields(self, weekly_race_fixture):
        """Verify all WeeklyRaceSeed fields."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        # Weekly race uses numeric string seeds, different from match seeds
        assert race.seed.overworld is None or isinstance(race.seed.overworld, str)
        assert race.seed.nether is None or isinstance(race.seed.nether, str)
        assert race.seed.the_end is None or isinstance(race.seed.the_end, str)
        assert race.seed.rng is None or isinstance(race.seed.rng, str)

    def test_race_leaderboard_entry_all_fields(self, weekly_race_fixture):
        """Verify all RaceLeaderboardEntry fields."""
        race = WeeklyRace.model_validate(weekly_race_fixture)

        if race.leaderboard:
            e = race.leaderboard[0]
            assert isinstance(e, RaceLeaderboardEntry)
            assert isinstance(e.rank, int)
            assert isinstance(e.player, UserProfile)
            assert isinstance(e.time, int)
            assert isinstance(e.replay_exist, bool)


class TestVodInfoFieldCoverage:
    """Test VodInfo fields - need to find a match with VOD."""

    def test_vod_info_structure(self):
        """Test VodInfo can be constructed with all fields."""
        # VodInfo is rare in the fixtures, so test the model directly
        vod = VodInfo(uuid="abc123", url="https://twitch.tv/example", startsAt=12345)

        assert isinstance(vod.uuid, str)
        assert isinstance(vod.url, str)
        assert isinstance(vod.starts_at, int)


class TestWeeklyRaceResultFieldCoverage:
    """Test WeeklyRaceResult fields."""

    def test_weekly_race_result_structure(self):
        """Test WeeklyRaceResult can be constructed with all fields."""
        # User.weekly_races is usually empty, so test the model directly
        result = WeeklyRaceResult(id=1, time=300000, rank=5)

        assert isinstance(result.id, int)
        assert isinstance(result.time, int)
        assert isinstance(result.rank, int)


class TestPhaseResultFieldCoverage:
    """Test PhaseResult fields."""

    def test_phase_result_structure(self):
        """Test PhaseResult can be constructed with all fields."""
        # Phases are often empty, so test the model directly
        phase = PhaseResult(phase=1, eloRate=1500, eloRank=100, point=50)

        assert isinstance(phase.phase, int)
        assert isinstance(phase.elo_rate, int)
        assert isinstance(phase.elo_rank, int)
        assert isinstance(phase.point, int)


class TestCompletionFieldCoverage:
    """Test Completion fields."""

    def test_completion_structure(self):
        """Test Completion can be constructed with all fields."""
        # Our fixture match was forfeited, so test the model directly
        completion = Completion(uuid="abc123", time=300000)

        assert isinstance(completion.uuid, str)
        assert isinstance(completion.time, int)
