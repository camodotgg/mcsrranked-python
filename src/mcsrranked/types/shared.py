from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "UserProfile",
    "Achievement",
    "MatchSeed",
    "EloChange",
    "VodInfo",
]


class UserProfile(BaseModel):
    """Basic user profile information."""

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

    model_config = {"populate_by_name": True}


class Achievement(BaseModel):
    """User achievement data."""

    id: str = Field(description="Achievement identifier")
    date: int = Field(description="Unix timestamp when achievement was earned")
    data: list[str | int] = Field(default_factory=list, description="Achievement data")
    level: int = Field(description="Achievement level")
    value: int | None = Field(default=None, description="Current progress value")
    goal: int | None = Field(default=None, description="Target goal value")

    model_config = {"populate_by_name": True}


class MatchSeed(BaseModel):
    """Match seed information."""

    id: str | None = Field(default=None, description="Seed identifier")
    overworld: str | None = Field(default=None, description="Overworld structure type")
    nether: str | None = Field(default=None, description="Bastion type")
    end_towers: list[int] | None = Field(
        default=None, alias="endTowers", description="End tower positions"
    )
    variations: list[str] = Field(default_factory=list, description="Seed variations")

    model_config = {"populate_by_name": True}

    @property
    def bastion(self) -> str | None:
        """Alias for nether field (bastion type)."""
        return self.nether


class EloChange(BaseModel):
    """Elo change data for a player in a match."""

    uuid: str = Field(description="Player UUID without dashes")
    change: int | None = Field(default=None, description="Elo change amount")
    elo_rate: int | None = Field(
        default=None, alias="eloRate", description="Elo rating after the match"
    )

    model_config = {"populate_by_name": True}


class VodInfo(BaseModel):
    """VOD information for a match."""

    uuid: str = Field(description="Player UUID without dashes")
    url: str = Field(description="VOD URL")
    starts_at: int = Field(alias="startsAt", description="VOD start timestamp offset")

    model_config = {"populate_by_name": True}
