import time
from Utilities.Observatory_Logger import ObservatoryLogger

class MountController:

    def __init__(self,mount):

        self.logger = ObservatoryLogger()
        self.mount = mount

    def _parse_angle(self, value:str) -> float:
        value = value.strip().rstrip('#')

        value = value.replace('*',':')
        parts = value.split(':')

        degrees = float(parts[0])
        sign = -1 if degrees < 0 else 1

        degrees = abs(degrees)

        minutes = float(parts[1]) if len(parts) > 1 else 0
        seconds = float(parts[2]) if len(parts) > 2 else 0

        return sign * (
            degrees
            + minutes/60
            + seconds/3600
        )

    def _parse_ra(self, value: str) -> float:
        value = value.strip().rstrip('#')

        parts = value.split(':')

        hours = float(parts[0])
        minutes = float(parts[1]) if len(parts) > 1 else 0
        seconds = float(parts[2]) if len(parts) > 2 else 0

        return (
            hours
            + minutes / 60
            + seconds / 3600
        )
    
    def _format_ra(self, ra_hours: float) -> str:
        ra_hours = ra_hours % 24

        hours = int(ra_hours)
        minutes_float = (ra_hours - hours) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60

        return f"{hours:02d}:{minutes:02d}:{seconds:05.2f}"


    def _format_dec(self, dec_degrees: float) -> str:
        sign = '+' if dec_degrees >= 0 else '-'

        dec_degrees = abs(dec_degrees)

        degrees = int(dec_degrees)
        minutes_float = (dec_degrees - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60

        return f"{sign}{degrees:02d}*{minutes:02d}:{seconds:04.1f}"


    #### Connection ####

    def connect(self):
        self.mount.connect()


    def disconnect(self):
        self.mount.disconnect()
    
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

    def start_tracking(self):
        self.mount.start_tracking()

    def stop_tracking(self):
        self.mount.stop_tracking()

    def slew_to_ra_dec(self, ra: float, dec: float):
        ra_string = self._format_ra(ra)
        dec_string = self._format_dec(dec)

        ra_result = self.mount.set_target_ra(ra_string)

        if str(ra_result).strip('#') != '1':
            return False

        dec_result = self.mount.set_target_declination(dec_string)

        if str(dec_result).strip('#') != '1':
            return False

        result = self.mount.slew_to_target()

        return str(result).strip('#') == '0'
    #### Get ####

    def get_ra(self):
        value = self.mount.get_telescope_ra()
        return self._parse_ra(value)

    def get_dec(self):
        value = self.mount.get_telescope_dec()
        return self._parse_angle(value)
    
    def get_ra_dec(self):
        return {
            'ra': self.get_ra(),
            'dec': self.get_dec()
        }
    
    def get_alt(self):
        value = self.mount.get_telescope_altitude()
        return self._parse_angle(value)
    
    def get_az(self):
        value = self.mount.get_telescope_azimuth()
        return self._parse_angle(value)

    def get_alt_az(self):
        return {
            'alt': self.get_alt(),
            'az': self.get_az()
        }

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
        return position
    
    def update_position_aa(self):
        position_aa = {
            'alt':self.mount.get_telescope_altitude(),
            'az':self.mount.get_telescope_azimuth()
        }
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

    def get_status(self):

        if not self.mount.is_connected():
            return {
                'connected': False,
                'data': None
            }
        return {
            'connected': True,
            'data': None
        }
    
    #### Home & Park ####

    def slew_to_park(self):
        self.mount.slew_to_park()

    def set_park_position(self):
        self.mount.set_park()
        

    def unpark(self):
        self.mount.unpark()

    def get_home_status(self):
        return self.mount.query_home_status()
    

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
    
    def get_target_ra_dec(self):
        return {
            'ra': self.get_target_ra(),
            'dec': self.get_target_dec()
        }

    def get_target_azimuth(self):
        return self.mount.get_target_azimuth()
    
    def get_target_altitude(self):
        return self.mount.get_target_altitude()
    
    def get_target_alt_az(self):
        return {
            'alt': self.get_target_altitude(),
            'az': self.get_target_azimuth()
        }