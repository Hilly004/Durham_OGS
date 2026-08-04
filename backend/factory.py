from Hardware.Connections.Mount_Connection import MountConnection
from Hardware.Mount.Mount_Commands import TenMicronMount
from Controllers.Mount_Controller import MountController
from Controllers.Observatory import ObservatoryController

from Utilities.Config import *

def build_observatory():

    mount_connection = MountConnection(host,port)
    mount_commands = TenMicronMount(mount_connection)
    mount_controller = MountController(mount_commands)


    return ObservatoryController(mount_controller)