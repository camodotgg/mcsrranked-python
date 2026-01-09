from __future__ import annotations

from pydantic import BaseModel, Field

from mcsrranked.types.shared import UserProfile

__all__ = [
    "WeeklyRace",
    "WeeklyRaceSeed",
    "RaceLeaderboardEntry",
]


class WeeklyRaceSeed(BaseModel):
    """Weekly race seed information."""

    overworld: str | None = Field(default=None, description="Overworld seed")
    nether: str | None = Field(default=None, description="Nether seed")
    the_end: str | None = Field(default=None, alias="theEnd", description="End seed")
    rng: str | None = Field(default=None, description="RNG seed")

    model_config = {"populate_by_name": True}


class RaceLeaderboardEntry(BaseModel):
    """Entry in the weekly race leaderboard."""

    rank: int = Field(description="Leaderboard rank")
    player: UserProfile = Field(description="Player profile")
    time: int = Field(description="Completion time in milliseconds")
    replay_exist: bool = Field(
        default=False, alias="replayExist", description="Whether replay is available"
    )

    model_config = {"populate_by_name": True}


class WeeklyRace(BaseModel):
    """Weekly race data."""

    id: int = Field(description="Weekly race ID")
    seed: WeeklyRaceSeed = Field(description="Race seed information")
    ends_at: int = Field(alias="endsAt", description="Unix timestamp when race ends")
    leaderboard: list[RaceLeaderboardEntry] = Field(
        default_factory=list, description="Race leaderboard"
    )

    model_config = {"populate_by_name": True}
