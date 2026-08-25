import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController
from Utilities.Observatory_Logger import ObservatoryLogger

import numpy as np
host = '192.168.1.119'
port = 3490

connection = MountConnection(
    host,
    port
)
mount = TenMicronMount(connection)
logger = ObservatoryLogger()

control = MountController(mount,logger)

connection.connect()

print(connection.send_receive(':NUDGE+0001,-0010#'))

connection.disconnect()