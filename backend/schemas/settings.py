from pydantic import BaseModel, ConfigDict, Field, field_validator


class SettingsUpdate(BaseModel):
    site_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    elevation_m: float = Field(ge=-500, le=10000)

    mount_host: str
    mount_port: int = Field(ge=1, le=65535)
    dome_host: str
    dome_port: int = Field(ge=1, le=65535)
    weather_port: str
    weather_baudrate: int = Field(ge=300, le=1_000_000)
    camera_id: str = ""

    max_wind_speed: float = Field(gt=0, le=200)
    max_humidity: float = Field(ge=0, le=100)
    weather_timeout_seconds: int = Field(ge=2, le=300)
    automatic_shutdown_enabled: bool

    default_nudge_arcsec: int = Field(ge=1, le=3600)
    default_prediction_minutes: int = Field(ge=1, le=1440)
    activity_log_max_entries: int = Field(ge=50, le=5000)

    @field_validator("site_name", "mount_host", "dome_host", "weather_port")
    @classmethod
    def non_empty(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value


class SettingsResponse(SettingsUpdate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TcpConnectionTest(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)


class SerialConnectionTest(BaseModel):
    port: str
    baudrate: int = Field(ge=300, le=1_000_000)


class ConnectionTestResponse(BaseModel):
    success: bool
    message: str
