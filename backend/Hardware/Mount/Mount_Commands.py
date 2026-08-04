class TenMicronMount:

    def __init__(self, connection):
        self.connection = connection


    ###### Helper Functions ######

    def query(self, command):
        # Send a command and wait for a response

        return self.connection.send_receive(command)


    def command(self, command):
        # Send a command without waiting for a response
        
        return self.connection.send(command)

    def is_connected(self):
        return self.connection.connected
    
    def connect(self):
        return self.connection.connect()
    
    def disconnect(self):
        return self.connection.disconnect()
    



    #########################################################################
    #                       Movement Commands
    #########################################################################

    def move_north(self):
        # Start manual movement north
        message = ':Mn#'
        return self.command(message)


    def stop_north(self):
        # Stop manual movement north
        message = ':Qn#'
        return self.command(message)


    def move_south(self):
        # Start manual movement south
        message = ':Ms#'
        return self.command(message)


    def stop_south(self):
        # Stop manual movement south
        message = ':Qs#'
        return self.command(message)


    def move_east(self):
        # Start manual movement east
        message = ':Me#'
        return self.command(message)


    def stop_east(self):
        # Stop manual movement east
        message = ':Qe#'
        return self.command(message)


    def move_west(self):
        # Start manual movement west
        message = ':Mw#'
        return self.command(message)


    def stop_west(self):
        # Stop manual movement west
        message = ':Qw#'
        return self.command(message)



    #########################################################################
    #                       Tracking Mode
    #########################################################################

    def stop_tracking(self):
        # Stop sidereal tracking
        message = ':AL#'
        return self.command(message)


    def start_tracking(self):
        # Start sidereal tracking
        message = ':AP#'
        return self.command(message)



    #########################################################################
    #                         GPS Commands
    #########################################################################

    def update_from_gps(self):
        # Update mount time and location information from GPS receiver
        message = ':gT#'
        return self.query(message)


    def check_mount_clock(self):
        # Check mount clock synchronisation status
        message = ':gtg#'
        return self.query(message)


    def get_last_gps_string(self):
        # Retrieve last GPS received string
        message = ':gps#'
        return self.query(message)



    #########################################################################
    #                         Get Commands
    #########################################################################

    def get_telescope_altitude(self):
        # Get current telescope altitude
        message = ':GA#'
        return self.query(message)


    def get_date(self):
        # Get current mount date
        message = ':GC#'
        return self.query(message)


    def get_telescope_dec(self):
        # Get current telescope declination
        message = ':GD#'
        return self.query(message)


    def get_site_elevation(self):
        # Get observatory elevation
        message = ':Gev#'
        return self.query(message)


    def get_utc_offset(self):
        # Get UTC offset
        message = ':GG#'
        return self.query(message)


    def get_site_longitude(self):
        # Get observatory longitude
        message = ':Gg#'
        return self.query(message)


    def get_site_latitude(self):
        # Get observatory latitude
        message = ':Gt#'
        return self.query(message)


    def get_high_limit_altitude(self):
        # Get maximum altitude limit
        message = ':Gh#'
        return self.query(message)


    def get_info(self):
        # Get general mount information
        message = ':Ginfo#'
        return self.query(message)


    def get_connection_type(self):
        # Get connection interface information
        message = ':GINQ#'
        return self.query(message)


    def get_ip_address(self):
        # Get mount IP address
        message = ':GIP#'
        return self.query(message)


    def get_mac_address(self):
        # Get mount MAC address
        message = ':GMAC#'
        return self.query(message)


    def get_julian_day(self):
        # Get Julian date
        message = ':GJD1#'
        return self.query(message)


    def get_local_time(self):
        # Get local time
        message = ':GL#'
        return self.query(message)


    def get_local_datetime(self):
        # Get local date and time
        message = ':GLDT#'
        return self.query(message)


    def get_utc_datetime(self):
        # Get UTC date and time
        message = ':GUDT#'
        return self.query(message)
    

    def get_delta_t_gps(self):
        # Get GPS delta time correction
        message = ':GDGPS#'
        return self.query(message)


    def get_meridian_behaviour(self):
        # Get meridian flip behaviour setting
        message = ':GMF#'
        return self.query(message)


    def get_low_limit_altitude(self):
        # Get minimum altitude limit
        message = ':Go#'
        return self.query(message)


    def get_telescope_ra(self):
        # Get current telescope right ascension
        message = ':GR#'
        return self.query(message)


    def get_atmospheric_pressure(self):
        # Get atmospheric pressure used for refraction correction
        message = ':GRPRS#'
        return self.query(message)


    def get_temperature(self):
        # Get mount temperature
        message = ':GRTMP#'
        return self.query(message)


    def get_sidereal_time(self):
        # Get current sidereal time
        message = ':GS#'
        return self.query(message)


    def get_refraction_status(self):
        # Get atmospheric refraction correction status
        message = ':GREF#'
        return self.query(message)


    def get_mount_status(self):
        # Get mount operating status
        message = ':Gstat#'
        return self.query(message)


    def get_meridian_flip_time(self):
        # Get calculated meridian flip time
        message = ':Gmte#'
        return self.query(message)


    def get_tracking_status(self):
        # Get whether tracking is active
        message = ':GTRK#'
        return self.query(message)


    def get_destination_side(self):
        # Get telescope side of pier/destination side
        message = ':GTsid#'
        return self.query(message)


    def get_firmware_date(self):
        # Get firmware release date
        message = ':GVD#'
        return self.query(message)


    def get_firmware_number(self):
        # Get firmware version number
        message = ':GVN#'
        return self.query(message)


    def get_wake_on_lan_status(self):
        # Get Wake-on-LAN status
        message = ':GWOL#'
        return self.query(message)


    def get_telescope_azimuth(self):
        # Get current telescope azimuth
        message = ':GZ#'
        return self.query(message)


    def get_point_state(self):
        # Get pointing state
        message = ':pS#'
        return self.query(message)



    #########################################################################
    #                         Home and Park Commands
    #########################################################################

    def slew_to_park(self):
        # Slew the mount to the stored park position
        message = ':KA#'
        return self.command(message)


    def unpark(self):
        # Unpark the mount and enable movement
        message = ':PO#'
        return self.command(message)


    def set_park(self):
        # Set the current position as the park position
        message = ':PiP#'
        return self.query(message)


    def query_home_status(self):
        # Query home status of the mount
        message = ':h?#'
        return self.query(message)

    #########################################################################
    #                         Get Targeting
    #########################################################################

    def get_target_azimuth(self):
        # Get target azimuth
        message = ':Gz#'
        return self.query(message)

    def get_target_ra(self):
        # Get target right ascension
        message = ':Gr#'
        return self.query(message)
    
    def get_target_dec(self):
        # Get target declination
        message = ':Gd#'
        return self.query(message)
    

    def get_target_altitude(self):
        # Get target altitude
        message = ':Ga#'
        return self.query(message)
    
    #########################################################################
    #                         Movement Commands
    #########################################################################

    def slew_to_altaz(self):
        # Start slew to previously defined Alt-Az target
        message = ':MA#'
        return self.query(message)


    def slew_to_target(self):
        # Start slew to previously defined RA-Dec target
        message = ':MS#'
        return self.query(message)


    def halt_slew(self):
        # Immediately stop all mount slewing
        message = ':Q#'
        return self.command(message)


    def get_slew_status(self):
        # Get current slew status
        message = ':D#'
        return self.query(message)


    def nudge(self, direction):
        # Perform a small manual movement in specified direction
        message = ':NUDGE' + direction + '#'
        return self.query(message)
    
    #########################################################################
    #                         Set Commands
    #########################################################################

    def set_target_altitude(self, altitude):
        # Set target altitude for a future slew
        message = ':Sa' + altitude + '#'
        return self.query(message)


    def set_target_declination(self, dec):
        # Set target declination for a future slew
        message = ':Sd' + dec + '#'
        return self.query(message)


    def set_site_elevation(self, elevation):
        # Set observatory elevation
        message = ':Sev' + elevation + '#'
        return self.query(message)


    def set_site_longitude(self, longitude):
        # Set observatory longitude
        message = ':Sg' + longitude + '#'
        return self.query(message)


    def set_max_altitude_limit(self, altitude):
        # Set maximum altitude slew limit
        message = ':Sh+' + str(altitude) + '#'
        return self.query(message)


    def set_min_altitude_limit(self, altitude):
        # Set minimum altitude slew limit
        message = ':So+' + str(altitude) + '#'
        return self.query(message)


    def set_target_ra(self, ra):
        # Set target right ascension for a future slew
        message = ':Sr' + ra + '#'
        return self.query(message)


    def set_site_latitude(self, latitude):
        # Set observatory latitude
        message = ':St' + latitude + '#'
        return self.query(message)


    def stop_all_motion(self):
        # Emergency stop of all mount movement
        message = ':STOP#'
        return self.command(message)


    def set_wake_on_lan(self, state):
        # Enable or disable Wake-on-LAN
        message = ':SWOL' + str(state) + '#'
        return self.query(message)


    def set_target_azimuth(self, azimuth):
        # Set target azimuth for a future Alt-Az slew
        message = ':Sz' + str(azimuth) + '#'
        return self.query(message)


    def set_sidereal_tracking_rate(self):
        # Set tracking rate to sidereal
        message = ':RT2#'
        return self.command(message)


    def stop_tracking_rate(self):
        # Stop tracking rate
        message = ':RT9#'
        return self.command(message)



    #########################################################################
    #                         Precision Commands
    #########################################################################

    def set_low_precision(self):
        # Set low precision coordinate format
        message = ':U0#'
        return self.command(message)


    def set_high_precision(self):
        # Set high precision coordinate format
        message = ':U1#'
        return self.command(message)


    def set_ultra_precision(self):
        # Set ultra precision coordinate format
        message = ':U2#'
        return self.command(message)



    #########################################################################
    #                         Storage Commands
    #########################################################################

    def write_storage(self, data):
        # Write data string to mount internal storage
        message = ':TLEL0' + data + '#'
        return self.query(message)


    def read_storage(self):
        # Read stored data from mount internal storage
        message = ':TLEG#'
        return self.query(message)



    #########################################################################
    #                         System Commands
    #########################################################################

    def shutdown(self):
        # Shutdown mount electronics
        message = ':shutdown#'
        return self.query(message)