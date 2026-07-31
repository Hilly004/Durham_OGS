class AstroHavenDome:

    def __init__(self,connection):
        super().__init__()

        self.connection = connection


    ##### Helper functions #####

    def query(self, command):
        return self.connection.send_receive(command)
    
    def send(self, command):
        return self.connection.send(command)
    
    def is_connected(self):
        return self.connection.connected
    
    def connect(self):
        return self.connection.connect()
    
    def disconnect(self):
        return self.connection.disconnect()

    #####

    def open_dome(self):
        return self.coma