from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
host = '192.168.1.119'
port = 3490

connection = MountConnection(
    host,
    port
)
mount = TenMicronMount(connection)

try:
    connection.connect()
    print('RA:')
    print(mount.get_info())
    connection.disconnect()

except Exception as e:
    print(e)