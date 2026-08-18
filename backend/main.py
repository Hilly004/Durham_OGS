from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.mount import (
    router as mount_router,
    set_controller as set_mount_controller,
    set_observatory_controller as set_mount_observatory_controller
)

from api.dome import (
    router as dome_router,
    set_controller as set_dome_controller,
    set_observatory_controller as set_dome_observatory_controller
)

from api.weather import (
    router as weather_router,
    set_controller as set_weather_controller
)

from api.observatory import (
    router as observatory_router,
    set_controller as set_observatory_controller
)

from api.satellite import (
    router as satellite_router,
    set_mount as set_satellite_mount
)

from api.activity import (
    router as activity_router,
    set_logger as set_activity_logger
)

from Controllers.Mount_Controller import MountController
from Hardware.Mount.Mount_Commands import TenMicronMount
from Hardware.Connections.Mount_Connection import MountConnection
from Utilities.Config import host, port


from Controllers.Dome_Controller import DomeController
from Hardware.Dome.Dome_Commands import AstroHavenDome
from Hardware.Connections.Dome_Connection import DomeConnection
from Utilities.Config import dome_host,dome_port

from Controllers.Weather_Controller import WeatherController
from Hardware.Weather.Weather_Commands import WeatherMonitor

from Observatory import ObservatoryController

from database.database import Base, engine
from models.satellite import Satellite

from Utilities.Observatory_Logger import ObservatoryLogger

@asynccontextmanager
async def lifespan(app: FastAPI):
    observatory_controller.start()

    try:
        yield
    finally:
        observatory_controller.stop()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Durham OGS API", lifespan=lifespan)

### LOGGER ###
logger = ObservatoryLogger()
set_activity_logger(logger)

###  MOUNT  ###
connection = MountConnection(host, port)
mount_driver = TenMicronMount(connection)
mount_controller = MountController(mount_driver,logger)
set_mount_controller(mount_controller)


### DOME ###
dome_connection = DomeConnection(dome_host, dome_port)
dome_driver = AstroHavenDome(dome_connection)
dome_controller = DomeController(dome_driver,logger)
set_dome_controller(dome_controller)

### WEATHER ###
weather_monitor = WeatherMonitor()
weather_controller = WeatherController(weather_monitor,logger)
set_weather_controller(weather_controller)

### SATELLITE ###

set_satellite_mount(mount_driver)



observatory_controller = ObservatoryController(
    dome_controller,
    mount_controller,
    weather_controller,
    logger
)

set_observatory_controller(observatory_controller)

set_dome_observatory_controller(
    observatory_controller
)

set_mount_observatory_controller(
    observatory_controller
)

app.include_router(mount_router)
app.include_router(dome_router)
app.include_router(weather_router)
app.include_router(observatory_router)
app.include_router(
    satellite_router,
    prefix='/api/satellites',
    tags=['satellites']
)
app.include_router(activity_router)


@app.get('/')
def root():
    return {
        'message': 'Durham OGS API',
        'status': 'running'
    }


