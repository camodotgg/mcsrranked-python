from __future__ import annotations

from pydantic import BaseModel, Field

from mcsrranked.types.shared import Achievement

__all__ = [
    "User",
    "UserTimestamps",
    "UserStatistics",
    "MatchTypeStats",
    "SeasonResult",
    "PhaseResult",
    "Connection",
    "UserConnections",
    "WeeklyRaceResult",
    "UserSeasons",
]


class MatchTypeStats(BaseModel):
    """Statistics for a specific match type (ranked/casual)."""

    played_matches: int = Field(
        default=0, alias="playedMatches", description="Total matches played"
    )
    wins: int = Field(default=0, description="Total wins")
    losses: int = Field(default=0, description="Total losses")
    draws: int = Field(default=0, description="Total draws")
    forfeits: int = Field(default=0, description="Total forfeits")
    highest_winstreak: int = Field(
        default=0, alias="highestWinstreak", description="Highest win streak achieved"
    )
    current_winstreak: int = Field(
        default=0, alias="currentWinstreak", description="Current win streak"
    )
    playtime: int = Field(default=0, description="Total playtime in milliseconds")
    best_time: int | None = Field(
        default=None,
        alias="bestTime",
        description="Best completion time in milliseconds",
    )
    best_time_id: int | None = Field(
        default=None, alias="bestTimeId", description="Match ID of best time"
    )
    completions: int = Field(default=0, description="Total completions")

    model_config = {"populate_by_name": True}


class SeasonStats(BaseModel):
    """Season statistics container."""

    ranked: MatchTypeStats = Field(
        default_factory=MatchTypeStats, description="Ranked match statistics"
    )
    casual: MatchTypeStats = Field(
        default_factory=MatchTypeStats, description="Casual match statistics"
    )

    model_config = {"populate_by_name": True}


class TotalStats(BaseModel):
    """All-time statistics container."""

    ranked: MatchTypeStats = Field(
        default_factory=MatchTypeStats, description="All-time ranked match statistics"
    )
    casual: MatchTypeStats = Field(
        default_factory=MatchTypeStats, description="All-time casual match statistics"
    )

    model_config = {"populate_by_name": True}


class UserStatistics(BaseModel):
    """User statistics for season and total."""

    season: SeasonStats = Field(
        default_factory=SeasonStats, description="Current season statistics"
    )
    total: TotalStats = Field(
        default_factory=TotalStats, description="All-time statistics"
    )

    model_config = {"populate_by_name": True}


class UserTimestamps(BaseModel):
    """User activity timestamps."""

    first_online: int = Field(
        alias="firstOnline", description="Unix timestamp of first connection"
    )
    last_online: int = Field(
        alias="lastOnline", description="Unix timestamp of last connection"
    )
    last_ranked: int | None = Field(
        default=None,
        alias="lastRanked",
        description="Unix timestamp of last ranked match",
    )
    next_decay: int | None = Field(
        default=None, alias="nextDecay", description="Unix timestamp of next elo decay"
    )

    model_config = {"populate_by_name": True}


class PhaseResult(BaseModel):
    """Phase result data."""

    phase: int = Field(description="Phase number")
    elo_rate: int = Field(alias="eloRate", description="Elo rating at phase end")
    elo_rank: int = Field(alias="eloRank", description="Elo rank at phase end")
    point: int = Field(description="Phase reward points")

    model_config = {"populate_by_name": True}


class LastSeasonState(BaseModel):
    """Last state of a season."""

    elo_rate: int | None = Field(
        default=None, alias="eloRate", description="Last elo rating of season"
    )
    elo_rank: int | None = Field(
        default=None, alias="eloRank", description="Last elo rank of season"
    )
    phase_point: int | None = Field(
        default=None, alias="phasePoint", description="Last phase points of season"
    )

    model_config = {"populate_by_name": True}


class SeasonResult(BaseModel):
    """User's season result data."""

    last: LastSeasonState = Field(description="Final season state")
    highest: int | None = Field(
        default=None, description="Highest elo rating of season"
    )
    lowest: int | None = Field(default=None, description="Lowest elo rating of season")
    phases: list[PhaseResult] = Field(
        default_factory=list, description="Phase results for the season"
    )

    model_config = {"populate_by_name": True}


class Connection(BaseModel):
    """Third-party connection data."""

    id: str = Field(description="Connection identifier")
    name: str = Field(description="Connection display name")

    model_config = {"populate_by_name": True}


class UserConnections(BaseModel):
    """User's third-party connections."""

    discord: Connection | None = Field(default=None, description="Discord connection")
    twitch: Connection | None = Field(default=None, description="Twitch connection")
    youtube: Connection | None = Field(default=None, description="YouTube connection")

    model_config = {"populate_by_name": True}


class WeeklyRaceResult(BaseModel):
    """User's weekly race result."""

    id: int = Field(description="Weekly race ID")
    time: int = Field(description="Completion time in milliseconds")
    rank: int = Field(description="Rank in the weekly race")

    model_config = {"populate_by_name": True}


class AchievementsContainer(BaseModel):
    """Container for user achievements."""

    display: list[Achievement] = Field(
        default_factory=list, description="Achievements displayed in-game"
    )
    total: list[Achievement] = Field(
        default_factory=list, description="All other achievements"
    )

    model_config = {"populate_by_name": True}


class User(BaseModel):
    """Full user profile data."""

    uuid: str = Field(description="UUID without dashes")
    nickname: str = Field(description="Player display name")
    role_type: int = Field(alias="roleType", description="User role type")
    elo_rate: int | None = Field(
        default=None,
        alias="eloRate",
        description="Elo rating for current season. None if placement matches not completed.",
    )
    elo_rank: int | None = Field(
        default=None, alias="eloRank", description="Rank for current season"
    )
    country: str | None = Field(
        default=None, description="Country code (lowercase ISO 3166-1 alpha-2)"
    )
    achievements: AchievementsContainer = Field(
        default_factory=AchievementsContainer, description="User achievements"
    )
    timestamp: UserTimestamps | None = Field(
        default=None, description="Activity timestamps"
    )
    statistics: UserStatistics = Field(
        default_factory=UserStatistics, description="Season and all-time statistics"
    )
    connections: UserConnections = Field(
        default_factory=UserConnections, description="Third-party connections"
    )
    season_result: SeasonResult | None = Field(
        default=None, alias="seasonResult", description="Current season elo data"
    )
    weekly_races: list[WeeklyRaceResult] = Field(
        default_factory=list, alias="weeklyRaces", description="Weekly race results"
    )

    model_config = {"populate_by_name": True}


class SeasonResultEntry(BaseModel):
    """Season result entry for user seasons endpoint."""

    last: LastSeasonState = Field(description="Final season state")
    highest: int = Field(description="Highest elo rating of season")
    lowest: int = Field(description="Lowest elo rating of season")
    phases: list[PhaseResult] = Field(
        default_factory=list, description="Phase results for the season"
    )

    model_config = {"populate_by_name": True}


class UserSeasons(BaseModel):
    """User's season results across all seasons."""

    uuid: str = Field(description="UUID without dashes")
    nickname: str = Field(description="Player display name")
    role_type: int = Field(alias="roleType", description="User role type")
    elo_rate: int | None = Field(
        default=None,
        alias="eloRate",
        description="Elo rating for current season. None if placement matches not completed.",
    )
    elo_rank: int | None = Field(
        default=None, alias="eloRank", description="Rank for current season"
    )
    country: str | None = Field(
        default=None, description="Country code (lowercase ISO 3166-1 alpha-2)"
    )
    season_results: dict[str, SeasonResultEntry] = Field(
        default_factory=dict,
        alias="seasonResults",
        description="Season results keyed by season number",
    )

    model_config = {"populate_by_name": True}
