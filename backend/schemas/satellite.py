from pydantic import BaseModel, ConfigDict, field_validator


class SatelliteCreate(BaseModel):
    name: str
    tle_line1: str
    tle_line2: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError('Satellite name cannot be empty')

        return value

    @field_validator('tle_line1')
    @classmethod
    def validate_line1(cls, value: str):
        value = value.strip()

        if not value.startswith('1 '):
            raise ValueError(
                'TLE line 1 must begin with "1 "'
            )

        return value

    @field_validator('tle_line2')
    @classmethod
    def validate_line2(cls, value: str):
        value = value.strip()

        if not value.startswith('2 '):
            raise ValueError(
                'TLE line 2 must begin with "2 "'
            )

        return value

class SatelliteResponse(BaseModel):
    id: int
    name: str
    tle_line1: str
    tle_line2: str

    model_config = ConfigDict(
        from_attributes=True
    )

class PassPredictionData(BaseModel):
    found: bool
    start_jd: float | None = None
    end_jd: float | None = None
    flags: str | None = None


class PassPredictionResponse(BaseModel):
    success: bool
    data: PassPredictionData | None = None


class TrackingStatusResponse(BaseModel):
    success: bool
    data: dict | None = None