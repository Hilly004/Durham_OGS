from fastapi import FastAPI


from api.mount import (
    router as mount_router,
    set_controller as set_mount_controller
)

from api.dome import (
    router as dome_router,
    set_controller as set_dome_controller
)

from api.weather import (
    router as weather_router,
    set_controller as set_weather_controller
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

app = FastAPI(title="Durham OGS API")


###  MOUNT  ###
connection = MountConnection(host, port)
mount_driver = TenMicronMount(connection)
mount_controller = MountController(mount_driver)
set_mount_controller(mount_controller)


### DOME ###
dome_connection = DomeConnection(dome_host, dome_port)
dome_driver = AstroHavenDome(dome_connection)
dome_controller = DomeController(dome_driver)
set_dome_controller(dome_controller)

### WEATHER ###
weather_monitor = WeatherMonitor()
weather_controller = WeatherController(weather_monitor)
set_weather_controller(weather_controller)

app.include_router(mount_router)
app.include_router(dome_router)
app.include_router(weather_router)



@app.get('/')
def root():
    return {
        'message': 'Durham OGS API',
        'status': 'running'
    }


