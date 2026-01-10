from __future__ import annotations

from pydantic import BaseModel, Field

from mcsrranked.types.match import Completion, Timeline
from mcsrranked.types.shared import UserProfile

__all__ = [
    "LiveData",
    "LiveMatch",
    "LivePlayerData",
    "LivePlayerTimeline",
    "UserLiveMatch",
]


class LivePlayerTimeline(BaseModel):
    """Live player timeline data."""

    time: int = Field(description="Match time of last split update in milliseconds")
    type: str = Field(description="Timeline identifier of last split")

    model_config = {"populate_by_name": True}


class LivePlayerData(BaseModel):
    """Live player data in a match."""

    live_url: str | None = Field(
        default=None,
        alias="liveUrl",
        description="Live stream URL. None if player hasn't activated public stream.",
    )
    timeline: LivePlayerTimeline | None = Field(
        default=None, description="Last timeline update"
    )

    model_config = {"populate_by_name": True}


class LiveMatch(BaseModel):
    """Live match data."""

    current_time: int = Field(
        alias="currentTime", description="Current match time in milliseconds"
    )
    players: list[UserProfile] = Field(
        default_factory=list,
        description="Players with public stream activated",
    )
    data: dict[str, LivePlayerData] = Field(
        default_factory=dict, description="Player data keyed by UUID"
    )

    model_config = {"populate_by_name": True}


class LiveData(BaseModel):
    """Live data response."""

    players: int = Field(
        description="Concurrent players connected to MCSR Ranked server"
    )
    live_matches: list[LiveMatch] = Field(
        default_factory=list,
        alias="liveMatches",
        description="Live matches with public streams",
    )

    model_config = {"populate_by_name": True}


class UserLiveMatch(BaseModel):
    """Live match data for a specific user (from /users/{id}/live endpoint)."""

    last_id: int | None = Field(
        default=None,
        alias="lastId",
        description="Match ID of previous match. Data resets when match ends.",
    )
    type: int = Field(description="Match type")
    status: str = Field(
        description="Match status: idle, counting, generate, ready, running, or done"
    )
    time: int = Field(
        description="Current match time in milliseconds. 0 if not started."
    )
    players: list[UserProfile] = Field(
        default_factory=list, description="Match players"
    )
    spectators: list[UserProfile] = Field(
        default_factory=list, description="Match spectators"
    )
    timelines: list[Timeline] = Field(
        default_factory=list, description="Timeline events"
    )
    completions: list[Completion] = Field(
        default_factory=list, description="Match completions"
    )

    model_config = {"populate_by_name": True}
