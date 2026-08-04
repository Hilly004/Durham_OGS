from fastapi import FastAPI

from api import mount

from Controllers.Mount_Controller import MountController
from Hardware.Mount.Mount_Commands import TenMicronMount
from Hardware.Connections.Mount_Connection import MountConnection
from Utilities.Config import host, port

app = FastAPI(title="Durham OGS API")

connection = MountConnection(host, port)
mount_driver = TenMicronMount(connection)
controller = MountController(mount_driver)

mount.set_controller(controller)

app.include_router(mount.router)

@app.get('/')
def root():
    return {
        'message': 'Durham OGS API',
        'status': 'running'
    }


