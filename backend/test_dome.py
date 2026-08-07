from Hardware.Dome.Dome_Commands import AstroHavenDome
from Hardware.Connections.Dome_Connection import DomeConnection
from Controllers.Dome_Controller import DomeController

from Utilities.Config import *

connection = DomeConnection(dome_host,dome_port)

connection.disconnect()