from PySide6.QtCore import QObject, Signal, QTimer


class MountController(QObject):
    
    status_changed = Signal(str)
    position_changed = Signal(dict)
    connection_changed = Signal(bool)

    def __init__(self,mount):
        super().__init__()

        self.mount = mount

    #### Connection ####

    def connect(self):
        success = self.mount.connect()
        self.connection_changed.emit(self.mount.is_connected())
        return success

    def disconnect(self):
        success = self.mount.disconnect()
        self.connection_changed.emit(self.mount.is_connected())
        return success
    
    def is_connected(self):

        return self.mount.is_connected()
    
    def refresh(self):
        connected = self.mount.is_connected()

        print('Refresh sees:', connected)
        self.connection_changed.emit(connected)

        if connected:
            try:
                self.position_changed.emit(self.update_position())

            except Exception as e:
                print(e)

        
    #### Movement ####

    def move_north(self):
        self.mount.move_north()

    def stop_north(self):
        self.mount.stop_north()

    def move_south(self):
        self.mount.move_south()

    def stop_south(self):
        self.mount.stop_south()

    def move_west(self):
        self.mount.move_west()

    def stop_west(self):
        self.mount.stop_west()

    def move_east(self):
        self.mount.move_east()

    def stop_east(self):
        self.mount.stop_east()



    def slew_to_target(self):
        self.mount.slew_to_target()


    def stop_motion(self):
        self.mount.stop_all_motion()

    #### Get ####

    def get_ra(self):
        return self.mount.get_telescope_ra()

    def get_dec(self):
        return self.mount.get_telescope_dec()

    def get_mount_status(self):
        return self.mount.get_mount_status()

    def get_slew_status(self):
        return self.mount.get_slew_status()
    
    def update_position(self):
        position = {
            'ra':self.mount.get_telescope_ra(),
            'dec':self.mount.get_telescope_dec()
        }
        self.position_changed.emit(position)
        return position

    #### Home & Park ####

    def slew_to_park(self):
        self.mount.slew_to_park()
        self.status_changed.emit('Slewing to target')

    def set_park_position(self):
        self.mount.set_park()
        self.status_changed.emit('Parking mount')

    def unpark(self):
        self.mount.unpark()

    #### Set ####

    def set_target_dec(self,dec):
        self.mount.set_target_declination(dec)

    def set_target_ra(self,ra):
        self.mount.set_target_ra(ra)

    def set_site_lat(self,lat):
        self.mount.set_site_latitude(lat)

    def set_site_long(self,long):
        self.mount.set_site_longitude(long)


