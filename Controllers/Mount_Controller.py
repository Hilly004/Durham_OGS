from PySide6.QtCore import QObject, Signal, QTimer
import time
from Utilities.Observatory_Logger import ObservatoryLogger

class MountController(QObject):
    
    status_changed = Signal(str)
    position_changed = Signal(dict)
    position_aa_changed = Signal(dict)
    connection_changed = Signal(bool)
    park_changed = Signal(bool)

    def __init__(self,mount):
        super().__init__()


        self.logger = ObservatoryLogger()
        self.mount = mount

        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.log_mount_state)
    #### Connection ####

    def connect(self):
        self.status_changed.emit('Connecting...')
        try:
            self.mount.connect()
            self.connection_changed.emit(True)
            self.status_changed.emit('Connected')
            self.log_timer.start(1000)

        except Exception as e:
            self.connection_changed.emit(False)
            self.status_changed.emit(f'Connection failed: {e}')

    def disconnect(self):
        self.log_timer.stop()
        self.status_changed.emit('Disconnecting...')
        self.mount.disconnect()
        self.connection_changed.emit(False)
        self.status_changed.emit('Mount not connected')
        
    
    def is_connected(self):

        return self.mount.is_connected()
     
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

    def stop_tracking(self):
        self.mount.stop_tracking()

    #### Get ####

    def get_ra(self):
        return self.mount.get_telescope_ra()

    def get_dec(self):
        return self.mount.get_telescope_dec()

    def get_mount_status(self):
        return self.mount.get_mount_status()

    def get_slew_status(self):
        return self.mount.get_slew_status()
    
    def get_tracking_status(self):
        return self.mount.get_tracking_status()
    
    def update_position(self):
        position = {
            'ra':self.mount.get_telescope_ra(),
            'dec':self.mount.get_telescope_dec()
        }
        self.position_changed.emit(position)
        return position
    
    def update_position_aa(self):
        position_aa = {
            'alt':self.mount.get_telescope_altitude(),
            'az':self.mount.get_telescope_azimuth()
        }
        self.position_aa_changed.emit(position_aa)
        return position_aa
    
    def get_info(self):
        field = self.mount.get_info().split(',')
        info = {
            'ra':field[0],
            'dec':field[1],
            'dir':field[2],
            'az':field[3],
            'alt':field[4],
            'jul':field[5],
            'stat':field[6], #Gstat status
            'slew_stat':field[7]
        }
        return info

    def log_mount_state(self):
        if not self.mount.is_connected():
            return

        self.logger.log(self.get_info()
        )
    #### Home & Park ####

    def slew_to_park(self):
        self.mount.slew_to_park()
        self.park_changed.emit(True)

    def set_park_position(self):
        self.mount.set_park()
        self.park_changed.emit(True)
        

    def unpark(self):
        self.mount.unpark()
        self.park_changed.emit(False)

    

    #### Set ####

    def set_target_dec(self,dec):
        self.mount.set_target_declination(dec)

    def set_target_ra(self,ra):
        self.mount.set_target_ra(ra)

    def set_target_azimuth(self,az):
        self.mount.set_target_azimuth(az)

    def set_target_altitude(self,alt):
        self.mount.set_target_altitude(alt)


    def set_site_lat(self,lat):
        self.mount.set_site_latitude(lat)

    def set_site_long(self,long):
        self.mount.set_site_longitude(long)


    #### Targeting ####

    def get_target_ra(self):
        return self.mount.get_target_ra()
    
    def get_target_dec(self):
        return self.mount.get_target_dec()
    
    def get_target_azimuth(self):
        return self.mount.get_target_azimuth()
    
    def get_target_altitude(self):
        return self.mount.get_target_altitude()