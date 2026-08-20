from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class ObservatorySettings(Base):
    __tablename__ = "observatory_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)

    # Observatory
    site_name: Mapped[str] = mapped_column(String, nullable=False, default="Durham OGS")
    latitude: Mapped[float] = mapped_column(Float, nullable=False, default=54.768)
    longitude: Mapped[float] = mapped_column(Float, nullable=False, default=-1.585)
    elevation_m: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Connections
    mount_host: Mapped[str] = mapped_column(String, nullable=False, default="192.168.1.119")
    mount_port: Mapped[int] = mapped_column(Integer, nullable=False, default=3490)

    dome_host: Mapped[str] = mapped_column(String, nullable=False, default="192.168.1.120")
    dome_port: Mapped[int] = mapped_column(Integer, nullable=False, default=502)

    weather_port: Mapped[str] = mapped_column(String, nullable=False, default="/dev/cu.usbserial")
    weather_baudrate: Mapped[int] = mapped_column(Integer, nullable=False, default=19200)

    camera_id: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Safety
    max_wind_speed: Mapped[float] = mapped_column(Float, nullable=False, default=40.0)
    max_humidity: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)
    weather_timeout_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    automatic_shutdown_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Defaults
    default_nudge_arcsec: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    default_prediction_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)

    # System
    activity_log_max_entries: Mapped[int] = mapped_column(Integer, nullable=False, default=500)