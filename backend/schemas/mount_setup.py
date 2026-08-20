from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class MountSiteUpdate(BaseModel):

    latitude: float = Field(
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ge=-180,
        le=180
    )

    elevation_m: float = Field(
        ge=-500,
        le=10000
    )


class AlignmentPointRequest(BaseModel):

    name: str = "Alignment star"

    ra_hours: float = Field(
        ge=0,
        lt=24
    )

    dec_degrees: float = Field(
        ge=-90,
        le=90
    )


    @field_validator("name")
    @classmethod
    def clean_name(
        cls,
        value: str
    ):

        value = value.strip()

        return (
            value
            or
            "Alignment star"
        )


class AlignmentNudgeRequest(BaseModel):

    direction: str

    step_arcsec: int = Field(
        ge=1,
        le=3600
    )


    @field_validator("direction")
    @classmethod
    def validate_direction(
        cls,
        value: str
    ):

        value = (
            value
            .strip()
            .lower()
        )


        if value not in {
            "north",
            "south",
            "east",
            "west",
        }:

            raise ValueError(
                (
                    "Direction must be north, "
                    "south, east or west"
                )
            )


        return value


class ModelNameRequest(BaseModel):

    name: str


    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str
    ):

        value = value.strip()


        if not value:

            raise ValueError(
                "Model name cannot be empty"
            )


        if len(value) > 15:

            raise ValueError(
                (
                    "TenMicron model names "
                    "are limited to 15 characters"
                )
            )


        return value