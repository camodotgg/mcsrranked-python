from __future__ import annotations

from pydantic import BaseModel, Field

from mcsrranked.types.shared import MatchSeed, UserProfile

__all__ = [
    "SeasonInfo",
    "LeaderboardUser",
    "EloLeaderboard",
    "PhaseInfo",
    "PhaseLeaderboardUser",
    "PhaseLeaderboard",
    "RecordEntry",
]


class SeasonInfo(BaseModel):
    """Season information."""

    number: int = Field(description="Season number")
    starts_at: int = Field(
        alias="startsAt", description="Unix timestamp of season start"
    )
    ends_at: int = Field(alias="endsAt", description="Unix timestamp of season end")

    model_config = {"populate_by_name": True}


class LeaderboardSeasonResult(BaseModel):
    """Season result for leaderboard user."""

    elo_rate: int = Field(alias="eloRate", description="Final elo rating in season")
    elo_rank: int = Field(alias="eloRank", description="Final elo rank in season")
    phase_point: int = Field(
        alias="phasePoint", description="Final phase points in season"
    )

    model_config = {"populate_by_name": True}


class LeaderboardUser(UserProfile):
    """User entry in the elo leaderboard."""

    season_result: LeaderboardSeasonResult = Field(
        alias="seasonResult", description="Season result data"
    )

    model_config = {"populate_by_name": True}


class EloLeaderboard(BaseModel):
    """Elo leaderboard data."""

    season: SeasonInfo = Field(description="Season information")
    users: list[LeaderboardUser] = Field(
        default_factory=list, description="Top 150 users by elo"
    )

    model_config = {"populate_by_name": True}


class PhaseInfo(BaseModel):
    """Phase information."""

    season: int = Field(description="Season number")
    number: int | None = Field(
        default=None, description="Current phase number. None for past seasons."
    )
    ends_at: int | None = Field(
        default=None,
        alias="endsAt",
        description="Unix timestamp of phase end. None for past seasons.",
    )

    model_config = {"populate_by_name": True}


class PhaseLeaderboardUser(UserProfile):
    """User entry in the phase points leaderboard."""

    season_result: LeaderboardSeasonResult = Field(
        alias="seasonResult", description="Season result data"
    )
    pred_phase_point: int = Field(
        default=0,
        alias="predPhasePoint",
        description="Predicted phase points for next phase",
    )

    model_config = {"populate_by_name": True}


class PhaseLeaderboard(BaseModel):
    """Phase points leaderboard data."""

    phase: PhaseInfo = Field(description="Phase information")
    users: list[PhaseLeaderboardUser] = Field(
        default_factory=list, description="Top 100 users by phase points"
    )

    model_config = {"populate_by_name": True}


class RecordEntry(BaseModel):
    """Record leaderboard entry."""

    rank: int = Field(description="Record rank")
    season: int = Field(description="Season number")
    date: int = Field(description="Unix timestamp of the record")
    id: int = Field(description="Match ID")
    time: int = Field(description="Completion time in milliseconds")
    user: UserProfile = Field(description="Player who set the record")
    seed: MatchSeed | None = Field(default=None, description="Seed information")

    model_config = {"populate_by_name": True}
