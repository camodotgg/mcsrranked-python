from __future__ import annotations

from pydantic import BaseModel, Field

from mcsrranked.types.shared import EloChange, MatchSeed, UserProfile, VodInfo

__all__ = [
    "MatchInfo",
    "MatchResult",
    "MatchRank",
    "Timeline",
    "Completion",
    "VersusStats",
    "VersusResults",
]


class MatchResult(BaseModel):
    """Match result data."""

    uuid: str | None = Field(default=None, description="Winner UUID without dashes")
    time: int = Field(description="Winning time in milliseconds")

    model_config = {"populate_by_name": True}


class MatchRank(BaseModel):
    """Match record ranking."""

    season: int | None = Field(default=None, description="Season record rank")
    all_time: int | None = Field(
        default=None, alias="allTime", description="All-time record rank"
    )

    model_config = {"populate_by_name": True}


class Timeline(BaseModel):
    """Match timeline event."""

    uuid: str = Field(description="Player UUID without dashes")
    time: int = Field(description="Event time in milliseconds")
    type: str = Field(description="Timeline event identifier")

    model_config = {"populate_by_name": True}


class Completion(BaseModel):
    """Match completion data."""

    uuid: str = Field(description="Player UUID without dashes")
    time: int = Field(description="Completion time in milliseconds")

    model_config = {"populate_by_name": True}


class MatchInfo(BaseModel):
    """Match information."""

    id: int = Field(description="Match ID")
    type: int = Field(description="Match type (1=casual, 2=ranked, 3=private, 4=event)")
    season: int = Field(description="Season number")
    category: str | None = Field(default=None, description="Completion category")
    date: int = Field(description="Unix timestamp in seconds")
    players: list[UserProfile] = Field(
        default_factory=list, description="Match players"
    )
    spectators: list[UserProfile] = Field(
        default_factory=list, description="Match spectators"
    )
    seed: MatchSeed | None = Field(default=None, description="Seed information")
    result: MatchResult | None = Field(default=None, description="Match result")
    forfeited: bool = Field(
        default=False, description="Whether match had no completions"
    )
    decayed: bool = Field(default=False, description="Whether match was decayed")
    rank: MatchRank | None = Field(default=None, description="Record ranking")
    changes: list[EloChange] = Field(default_factory=list, description="Elo changes")
    tag: str | None = Field(default=None, description="Special match tag")
    beginner: bool = Field(default=False, description="Whether beginner mode was used")
    vod: list[VodInfo] = Field(default_factory=list, description="VOD information")
    # Advanced fields (only from /matches/{id} endpoint)
    completions: list[Completion] = Field(
        default_factory=list, description="Match completions (advanced)"
    )
    timelines: list[Timeline] = Field(
        default_factory=list, description="Timeline events (advanced)"
    )
    replay_exist: bool = Field(
        default=False, alias="replayExist", description="Whether replay is available"
    )

    model_config = {"populate_by_name": True}


class VersusResultStats(BaseModel):
    """Stats for versus results."""

    total: int = Field(default=0, description="Total matches")

    model_config = {"populate_by_name": True, "extra": "allow"}


class VersusResults(BaseModel):
    """Versus match results."""

    ranked: dict[str, int] = Field(
        default_factory=dict,
        description="Ranked results. 'total' is match count, UUID keys are win counts.",
    )
    casual: dict[str, int] = Field(
        default_factory=dict,
        description="Casual results. 'total' is match count, UUID keys are win counts.",
    )

    model_config = {"populate_by_name": True}


class VersusStats(BaseModel):
    """Versus statistics between two players."""

    players: list[UserProfile] = Field(
        default_factory=list, description="The two players"
    )
    results: VersusResults = Field(
        default_factory=VersusResults, description="Match results by type"
    )
    changes: dict[str, int] = Field(
        default_factory=dict,
        description="Total elo changes between players (keyed by UUID)",
    )

    model_config = {"populate_by_name": True}
