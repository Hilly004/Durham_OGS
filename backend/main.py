from fastapi import FastAPI
from contextlib import asynccontextmanager


# ============================================================
# API ROUTERS
# ============================================================

from api.mount import (
    router as mount_router,
    set_controller as set_mount_controller,
    set_observatory_controller as set_mount_observatory_controller,
)

from api.dome import (
    router as dome_router,
    set_controller as set_dome_controller,
    set_observatory_controller as set_dome_observatory_controller,
)

from api.weather import (
    router as weather_router,
    set_controller as set_weather_controller,
)

from api.observatory import (
    router as observatory_router,
    set_controller as set_observatory_controller,
)

from api.satellite import (
    router as satellite_router,
    set_mount as set_satellite_mount,
    set_logger as set_satellite_logger,
)

from api.activity import (
    router as activity_router,
    set_logger as set_activity_logger,
)

from api.settings import (
    router as settings_router,
    set_runtime as set_settings_runtime,
    apply_saved_settings,
)

from api.mount_alignment import (
    router as mount_alignment_router,
    set_controller as set_mount_alignment_controller,
)

from api.camera import (
    router as camera_router,
    set_controller as set_camera_controller
)

# ============================================================
# MOUNT
# ============================================================

from Controllers.Mount_Controller import MountController

from Hardware.Mount.Mount_Commands import (
    TenMicronMount,
)

from Hardware.Connections.Mount_Connection import (
    MountConnection,
)

# ============================================================
# DOME
# ============================================================

from Controllers.Dome_Controller import DomeController

from Hardware.Dome.Dome_Commands import (
    AstroHavenDome,
)

from Hardware.Connections.Dome_Connection import (
    DomeConnection,
)


# ============================================================
# WEATHER
# ============================================================

from Controllers.Weather_Controller import (
    WeatherController,
)

from Hardware.Weather.Weather_Commands import (
    WeatherMonitor,
)

from Hardware.Connections.Weather_Connection import (
    WeatherConnection
)

# ============================================================
# OBSERVATORY
# ============================================================

from Observatory import ObservatoryController


# ============================================================
# DATABASE
# ============================================================

from database.database import (
    Base,
    engine,
)

from models.satellite import Satellite

# IMPORTANT:
# This import ensures SQLAlchemy knows about the
# observatory_settings table before create_all().
from models.settings import ObservatorySettings


# ============================================================
# LOGGER
# ============================================================

from Utilities.Observatory_Logger import (
    ObservatoryLogger,
)

# ============================================================
# CAMERA
# ============================================================

from Controllers.Camera_Controller import (
    CameraController,
)

from Hardware.Camera.ZWO_Camera import ZWOCamera


# ============================================================
# LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    observatory_controller.start()

    try:

        yield

    finally:

        observatory_controller.stop()


# ============================================================
# DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)

# ============================================================
# STARTUP SETTINGS
# ============================================================

from database.database import SessionLocal
from Repository.SettingsRepo import SettingsRepository


def load_startup_settings():

    db = SessionLocal()

    try:
        repository = SettingsRepository(db)
        return repository.get_or_create()

    finally:
        db.close()

startup_settings = load_startup_settings()
# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Durham OGS API",
    lifespan=lifespan,
)


# ============================================================
# LOGGER
# ============================================================

logger = ObservatoryLogger()

set_activity_logger(
    logger
)

set_satellite_logger(
    logger
)


# ============================================================
# MOUNT
# ============================================================

mount_connection = MountConnection(
    startup_settings.mount_host,
    startup_settings.mount_port,
)

mount_driver = TenMicronMount(
    mount_connection
)

mount_controller = MountController(
    mount_driver,
    logger,
)

set_mount_controller(
    mount_controller
)

set_mount_alignment_controller(
    mount_controller
)


# ============================================================
# DOME
# ============================================================

dome_connection = DomeConnection(
    startup_settings.dome_host,
    startup_settings.dome_port,
)

dome_driver = AstroHavenDome(
    dome_connection
)

dome_controller = DomeController(
    dome_driver,
    logger,
)

set_dome_controller(
    dome_controller
)


# ============================================================
# WEATHER
# ============================================================

weather_connection = WeatherConnection(
    startup_settings.weather_port,
    startup_settings.weather_baudrate
)

weather_monitor = WeatherMonitor()

weather_controller = WeatherController(
    weather_monitor,
    logger,
)

set_weather_controller(
    weather_controller
)

# ============================================================
# CAMERA
# ============================================================

camera_driver = ZWOCamera(camera_id='0')

camera_controller = CameraController(
    camera_driver,
    logger,
)

set_camera_controller(
    camera_controller
)

# ============================================================
# SATELLITE
# ============================================================

set_satellite_mount(
    mount_driver
)


# ============================================================
# OBSERVATORY
# ============================================================

observatory_controller = ObservatoryController(
    dome_controller,
    mount_controller,
    weather_controller,
    logger,
)

set_observatory_controller(
    observatory_controller
)

set_dome_observatory_controller(
    observatory_controller
)

set_mount_observatory_controller(
    observatory_controller
)


# ============================================================
# SETTINGS RUNTIME
# ============================================================

set_settings_runtime(
    weather_controller,
    observatory_controller,
    logger,
    mount_conn=mount_connection,
    dome_conn=dome_connection,
    weather_conn=weather_connection,
    camera_driver=camera_driver,
)


#
# Load persisted settings from SQLite
# and apply them to the running system.
#
apply_saved_settings()


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    mount_router
)

app.include_router(
    dome_router
)

app.include_router(
    weather_router
)

app.include_router(
    camera_router
)

app.include_router(
    observatory_router
)

app.include_router(
    satellite_router,
    prefix="/api/satellites",
    tags=["satellites"],
)

app.include_router(
    activity_router
)

app.include_router(
    settings_router
)

app.include_router(
    mount_alignment_router
)

# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Durham OGS API",
        "status": "running",
    }