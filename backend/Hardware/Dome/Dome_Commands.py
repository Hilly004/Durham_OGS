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

    def format(
            self, 
            id,
            action,
            coil,
            msg
            )
        return self.connection.send(
            '00'+id+'0000'+'0006'+'01'+action+'00'+coil+msg
            )

    #####

    def open_dome(self):
        return self.coma