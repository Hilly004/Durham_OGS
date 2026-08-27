import time
import os
import sys

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount


HOST = "192.168.1.119"
PORT = 3490


connection = MountConnection(
    HOST,
    PORT
)

mount = TenMicronMount(
    connection
)


try:

    mount.connect()

    print(
        "Mount state:",
        mount.get_mount_status()
    )

    print(
        "Starting north movement"
    )

    mount.move_north()

    time.sleep(0.5)

    print(
        "Stopping north movement"
    )

    mount.stop_north()

    print(
        "Finished"
    )


finally:

    mount.disconnect()