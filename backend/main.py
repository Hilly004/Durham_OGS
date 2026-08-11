from fastapi import FastAPI

from api.mount import (
    router as mount_router,
    set_controller as set_mount_controller
)
from api.dome import (
    router as dome_router,
    set_controller as set_dome_controller
)
from Controllers.Mount_Controller import MountController
from Hardware.Mount.Mount_Commands import TenMicronMount
from Hardware.Connections.Mount_Connection import MountConnection
from Utilities.Config import host, port

from Controllers.Dome_Controller import DomeController
from Hardware.Dome.Dome_Commands import AstroHavenDome
from Hardware.Connections.Dome_Connection import DomeConnection
from Utilities.Config import dome_host,dome_port

app = FastAPI(title="Durham OGS API")

connection = MountConnection(host, port)
mount_driver = TenMicronMount(connection)
controller = MountController(mount_driver)
set_mount_controller(controller)

dome_connection = DomeConnection(dome_host, dome_port)
dome_driver = AstroHavenDome(dome_connection)
dome_controller = DomeController(dome_driver)
set_dome_controller(controller)


app.include_router(mount_router)
app.include_router(dome_router)

@app.get('/')
def root():
    return {
        'message': 'Durham OGS API',
        'status': 'running'
    }


