from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController
host = '192.168.1.119'
port = 3490

connection = MountConnection(
    host,
    port
)
mount = TenMicronMount(connection)

control = MountController(mount)

print(connection.connect())