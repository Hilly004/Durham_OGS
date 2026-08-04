from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController
from Utilities.Config import *

connection = MountConnection(host,port)
mount = TenMicronMount(connection)
controller = MountController(mount)

controller.get_status()