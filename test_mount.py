from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController

import numpy as np
host = '192.168.1.119'
port = 3490

connection = MountConnection(
    host,
    port
)
mount = TenMicronMount(connection)

control = MountController(mount)

control.connect()

print(control.get_info())

control.disconnect()