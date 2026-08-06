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
    #                       Alignment Commands
    #########################################################################

    def get_alignment_mode(self):
        """Query the alignment/tracking mounting mode.
        Format: no input (command string is the single byte 0x06, the <ACK> character).
        Returns: 'L' if tracking is off, 'P' if tracking is on.
        """
        message = '\x06'
        return self.query(message)

    def stop_tracking(self):
        """Stop tracking.
        """
        message = ':AL#'
        return self.command(message)

    def start_tracking(self):
        """Start tracking.
        """
        message = ':AP#'
        return self.command(message)



    #########################################################################
    #                         GPS Commands
    #########################################################################

    def update_from_gps(self):
        """Update mount clock, latitude, longitude and elevation from GPS (async from fw 2.12.6).
        Returns: '0' if GPS unconnected/error (or not yet synced from fw 2.12.6), '1' if successful/synced.
        """
        message = ':gT#'
        return self.query(message)

    def get_last_gps_string(self):
        """Retrieve the last string received from the GPS.
        Returns: last NMEA string from the GPS, if available, terminated by '#'.
        """
        message = ':gps#'
        return self.query(message)

    def check_mount_clock(self):
        """Check if the mount clock is being kept synchronised to the GPS clock.
        Returns: '0#' if not synchronised to GPS clock, '1#' if synchronised.
        """
        message = ':gtg#'
        return self.query(message)



    #########################################################################
    #                 Sync Control and Model Building
    #########################################################################

    def sync_add_alignment_point(self):
        """Add an alignment point to the current model at the current target coordinates.
        Format: no input (target must be set beforehand with set_target_ra/set_target_declination).
        Returns: 'V#' if successful, 'E#' if the model can't be refined. Available from v2.8.15.
        """
        message = ':CMS#'
        return self.query(message)

    def sync_position(self):
        """Synchronise mount position with the currently selected target (offset or refine, per CMCFG).
        Returns: "Coordinates matched #" if synced, "Match fail: dist. too large#" otherwise
        (or offsets the axis angles directly, depending on the last :CMCFGn# setting).
        """
        message = ':CM#'
        return self.query(message)

    def sync_position_r(self):
        """Identical to sync_position(); the same as :CM#.
        Returns: same as sync_position().
        """
        message = ':CMR#'
        return self.query(message)

    def set_sync_config(self, n):
        """Configure the behaviour of :CM#/:CMR#.
        Format: n = 0 (offset axis angles, default) or 1 (use as additional alignment star).
        Returns: '0#' or '1#' echoing the value passed. Available from v2.8.15.
        """
        message = ':CMCFG' + str(n) + '#'
        return self.query(message)

    def get_alignment_star_count(self):
        """Get the number of alignment stars used in the current alignment model.
        Returns: number of alignment stars, terminated by '#'. Available from v2.8.15.
        """
        message = ':getalst#'
        return self.query(message)

    def delete_alignment_model(self):
        """Delete the current alignment model and all its stars.
        Returns: an empty string terminated by '#'. Available from v2.8.15.
        """
        message = ':delalig#'
        return self.query(message)

    def get_alignment_star_info(self, n):
        """Get alignment information for star number n.
        Format: n = star index, 1 to value returned by get_alignment_star_count().
        Returns: 'E#' if n out of range, otherwise "HH:MM:SS.SS,+dd*mm:ss.s,eeee.e#"
        (hour angle, declination, error in arcseconds). Available from v2.8.15.
        """
        message = ':getali' + str(n) + '#'
        return self.query(message)

    def get_alignment_model_info(self):
        """Get alignment information about the current alignment model.
        Returns: 'E#' if fewer than two stars, otherwise
        "ZZZ.ZZZZ,+AA.AAAA,EE.EEEE,PPP.PP,+OO.OOOO,+aa.aa,+bb.bb,NN,RRRRR.R#"
        (azimuth, altitude, polar align error, position angle, orthogonality error,
        azimuth/altitude knob turns, number of terms, expected RMS error). Available from v2.14.20.
        """
        message = ':getain#'
        return self.query(message)

    def get_alignment_star_info_polar(self, n):
        """Get alignment information for star n, including polar angle of measured vs modeled star.
        Format: n = star index, 1 to value returned by get_alignment_star_count().
        Returns: 'E#' if n out of range, otherwise "HH:MM:SS.SS,+dd*mm:ss.s,eeee.e,ppp#"
        (hour angle, declination, error in arcseconds, polar angle 0-359). Available from v2.8.15.
        """
        message = ':getalp' + str(n) + '#'
        return self.query(message)

    def delete_alignment_star(self, n):
        """Delete alignment star n and recalculate the alignment model.
        Format: n = star index, 1 to value returned by get_alignment_star_count().
        Returns: '0#' if the procedure failed, '1#' if it succeeded. Available from v2.8.15.
        """
        message = ':delalst' + str(n) + '#'
        return self.query(message)

    def new_alignment_spec(self):
        """Start creating a new alignment specification (does not clear the active model).
        Returns: 'V#' (always successful). Available from v2.8.15.
        """
        message = ':newalig#'
        return self.query(message)

    def new_alignment_point(self, mra, mdec, mside, pra, pdec, sidtime):
        """Add a new point to the alignment specification started with new_alignment_spec().
        Format: mra='HH:MM:SS.S', mdec='sDD:MM:SS', mside='E' or 'W', pra='HH:MM:SS.S',
        pdec='sDD:MM:SS', sidtime='HH:MM:SS.S'.
        Returns: "nnn#" (current number of points) if valid, 'E#' if not valid. Available from v2.8.15.
        """
        message = ':newalpt' + mra + ',' + mdec + ',' + mside + ',' + pra + ',' + pdec + ',' + sidtime + '#'
        return self.query(message)

    def end_alignment_spec(self):
        """Complete the alignment specification and compute a new alignment model from it.
        Returns: 'V#' if computed successfully, 'E#' if it couldn't be computed (previous model kept).
        Available from v2.8.15.
        """
        message = ':endalig#'
        return self.query(message)

    def get_model_count(self):
        """Get the number of user alignment models saved in the mount.
        Returns: "nnn#" number of saved models. Available from v2.13.3.
        """
        message = ':modelcnt#'
        return self.query(message)

    def get_model_name(self, n):
        """Get the name of saved model number n.
        Format: n = model index, 1 to value returned by get_model_count().
        Returns: '#' if n not valid, otherwise the (escaped) model name terminated by '#'.
        Available from v2.13.3.
        """
        message = ':modelnam' + str(n) + '#'
        return self.query(message)

    def load_model(self, name):
        """Load the alignment model with the given name.
        Format: name = model name string (escaped), case-sensitive, max 15 characters.
        Returns: '1#' if loaded correctly, '0#' if there was an error. Available from v2.13.3.
        """
        message = ':modelld0' + name + '#'
        return self.query(message)

    def save_model(self, name):
        """Save the current alignment model under the given name.
        Format: name = model name string (escaped), case-sensitive, max 15 characters.
        Returns: '1#' if saved correctly, '0#' if there was an error. Available from v2.13.3.
        """
        message = ':modelsv0' + name + '#'
        return self.query(message)

    def delete_model(self, name):
        """Delete the saved alignment model with the given name.
        Format: name = model name string (escaped), case-sensitive, max 15 characters.
        Returns: '1#' if deleted, '0#' if there was an error. Available from v2.13.3.
        """
        message = ':modeldel0' + name + '#'
        return self.query(message)



    #########################################################################
    #                         Get Information
    #########################################################################

    def get_telescope_altitude(self):
        """Get the current telescope altitude above the horizon.
        Returns: sDD*MM# / sDD*MM:SS# / sDD:MM:SS.S# depending on precision mode.
        """
        message = ':GA#'
        return self.query(message)

    def get_target_altitude(self):
        """Get the current target altitude above the horizon.
        Returns: sDD*MM# / sDD*MM:SS# / sDD:MM:SS.S# depending on precision mode.
        """
        message = ':Ga#'
        return self.query(message)

    def get_date(self):
        """Get the current mount date.
        Returns: MM/DD/YY# (LX200), MM:DD:YY# (extended), or YYYY-MM-DD# (ultra precision).
        """
        message = ':GC#'
        return self.query(message)

    def get_telescope_dec(self):
        """Get the current telescope declination.
        Returns: sDD*MM# / sDD*MM:SS# / sDD:MM:SS.S# depending on emulation/precision.
        """
        message = ':GD#'
        return self.query(message)

    def get_target_dec(self):
        """Get the current target declination.
        Returns: sDD*MM# / sDD*MM:SS# / sDD:MM:SS.S# depending on emulation/precision.
        """
        message = ':Gd#'
        return self.query(message)

    def get_site_elevation(self):
        """Get the current site elevation.
        Returns: sXXXX.X# elevation in metres.
        """
        message = ':Gev#'
        return self.query(message)

    def get_utc_offset(self):
        """Get the number of hours added to local time to yield UTC.
        Returns: sHH.H# / sHH:MM.M# / sHH:MM:SS.S# depending on emulation/precision.
        """
        message = ':GG#'
        return self.query(message)

    def get_site_longitude(self):
        """Get the current site longitude (East longitudes returned as negative).
        Returns: sDDD*MM# / sDDD*MM:SS# / sDDD:MM:SS.S# depending on emulation/precision.
        """
        message = ':Gg#'
        return self.query(message)

    def get_high_limit_altitude(self):
        """Get the highest altitude the mount may slew to.
        Returns: sDD*# (low/high precision) or sDD# (ultra precision).
        """
        message = ':Gh#'
        return self.query(message)

    def get_info(self):
        """Get multiple pieces of mount information in a single query.
        Returns: comma-separated string terminated by '#': RA, Dec (JNow), pier side ('E'/'W'),
        azimuth, altitude, Julian date w/ leap flag, mount status code, slew status (0/1).
        Available from v2.14.9.
        """
        message = ':Ginfo#'
        return self.query(message)

    def get_connection_type(self):
        """Get the type of connection currently in use.
        Returns: '0#' serial RS-232, '1#' GPS/RS-232, '2#' cabled LAN, '3#' wireless LAN.
        Available from v2.10.
        """
        message = ':GINQ#'
        return self.query(message)

    def get_ip_address(self):
        """Get the wired IP address configuration of the mount.
        Returns: "nnn.nnn.nnn.nnn,mmm.mmm.mmm.mmm,ggg.ggg.ggg.ggg,c#"
        (IP, subnet mask, gateway, 'D'=DHCP or 'M'=manual).
        """
        message = ':GIP#'
        return self.query(message)

    def get_wireless_ip_address(self):
        """Get the wireless IP address configuration of the mount.
        Returns: "nnn.nnn.nnn.nnn,mmm.mmm.mmm.mmm,ggg.ggg.ggg.ggg,c#"
        (IP, subnet mask, gateway, 'D'=DHCP or 'M'=manual). Available from v2.9.8.
        """
        message = ':GIPW#'
        return self.query(message)

    def get_mac_address(self):
        """Get the MAC address of the Ethernet interface.
        Returns: "NN:NN:NN:NN:NN:NN#" or '#' if no Ethernet interface. Available from v2.14.11.
        """
        message = ':GMAC#'
        return self.query(message)

    def get_wireless_mac_address(self):
        """Get the MAC address of the wireless interface.
        Returns: "NN:NN:NN:NN:NN:NN#" or '#' if no wireless interface. Available from v2.14.11.
        """
        message = ':GMACW#'
        return self.query(message)

    def get_julian_date(self):
        """Get the current Julian Date.
        Returns: JJJJJJJ.JJJJJ# (invalid during leap seconds).
        """
        message = ':GJD#'
        return self.query(message)

    def get_julian_day(self):
        """Get the current Julian Date with extended (8 decimal place) precision.
        Returns: JJJJJJJ.JJJJJJJJ# (invalid during leap seconds). Available from v2.10.
        """
        message = ':GJD1#'
        return self.query(message)

    def get_julian_date_leap(self):
        """Get the current Julian Date with extended precision and leap second flag.
        Returns: JJJJJJJ.JJJJJJJJ# or JJJJJJJ.JJJJJJJJL# ('L' during a leap second).
        Available from v2.13.2.
        """
        message = ':GJD2#'
        return self.query(message)

    def get_local_time(self):
        """Get the local time in 24-hour format.
        Returns: HH:MM:SS# / HH:MM.T# / HH:MM:SS.S# / HH:MM:SS.SS# depending on emulation/precision.
        """
        message = ':GL#'
        return self.query(message)

    def get_local_datetime(self):
        """Get the local date and time together.
        Returns: "<date>,<time>#" using the formats of get_date()/get_local_time(). Available from v2.12.26.
        """
        message = ':GLDT#'
        return self.query(message)

    def get_utc_datetime(self):
        """Get the UTC date and time together.
        Returns: "<date>,<time>#" using the formats of get_date()/get_local_time(). Available from v2.12.26.
        """
        message = ':GUDT#'
        return self.query(message)

    def get_utc_ut1_difference(self):
        """Get the current UTC - UT1 difference.
        Returns: XXX.XX# seconds and decimals, with sign. Available from v2.13.1.
        """
        message = ':GDUT#'
        return self.query(message)

    def get_delta_t_status(self):
        """Get the status of the deltaT flag and expiration date of the deltaT-UTC data.
        Returns: "F,XXXX-XX-XX#" where F is 'V' (valid) or 'E' (expired). Available from v2.15.
        """
        message = ':GDUTV#'
        return self.query(message)

    def get_delta_t_gps(self):
        """Get the current GPS - UTC difference.
        Returns: XX# seconds. Available from v2.13.1.
        """
        message = ':GDGPS#'
        return self.query(message)

    def get_next_leap_second(self):
        """Get the date of the next leap second accounted for by the mount.
        Returns: XXXX-XX-XX# date (UTC) of next leap second, or 'E#' if none due. Available from v2.13.1.
        """
        message = ':GULEAP#'
        return self.query(message)

    def get_meridian_behaviour(self):
        """Get the meridian side behaviour for slewing.
        Returns: '1#' both sides allowed, '2#' only west, '3#' only east. Available from v2.7.7.
        """
        message = ':GMF#'
        return self.query(message)

    def get_low_limit_altitude(self):
        """Get the lowest altitude the mount may slew to.
        Returns: sDD*# (low/high precision) or sDD# (ultra precision).
        """
        message = ':Go#'
        return self.query(message)

    def get_guiding_status(self):
        """Get the current guiding status.
        Returns: '0' not guiding, '1' guiding RA/azimuth, '2' guiding Dec/altitude, '3' guiding both axes.
        Available from v2.9.9 (only reliable from v2.9.21).
        """
        message = ':Gpgc#'
        return self.query(message)

    def get_telescope_ra(self):
        """Get the current telescope right ascension.
        Returns: HH:MM.M# / HH:MM:SS# / HH:MM:SS.S# / HH:MM:SS.SS# depending on emulation/precision.
        """
        message = ':GR#'
        return self.query(message)

    def get_target_ra(self):
        """Get the current target right ascension.
        Returns: HH:MM.M# / HH:MM:SS# / HH:MM:SS.S# / HH:MM:SS.SS# depending on emulation/precision.
        """
        message = ':Gr#'
        return self.query(message)

    def get_relay_status(self, n):
        """Get the status of relay n.
        Format: n = ASCII digit 1-8 (1-6 user relays, 7 RA/Az heater, 8 Dec/Alt heater).
        Returns: '0' (open) or '1' (closed). Special-purpose mounts with external relay control only.
        """
        message = ':GRLY' + str(n) + '#'
        return self.query(message)

    def get_atmospheric_pressure(self):
        """Get the atmospheric pressure used in the refraction model.
        Returns: PPPP.P# pressure in hPa. Available from v2.3.0.
        """
        message = ':GRPRS#'
        return self.query(message)

    def get_temperature(self):
        """Get the temperature used in the refraction model.
        Returns: +TTT.T# degrees Celsius. Available from v2.3.0.
        """
        message = ':GRTMP#'
        return self.query(message)

    def get_sidereal_time(self):
        """Get the local sidereal time.
        Returns: HH:MM.M# / HH:MM:SS# / HH:MM:SS.S# / HH:MM:SS.SS# depending on emulation/precision.
        """
        message = ':GS#'
        return self.query(message)

    def get_refraction_status(self):
        """Get the current status of the refraction correction.
        Returns: '0' inactive, '1' active. Available from v2.10.
        """
        message = ':GREF#'
        return self.query(message)

    def get_speed_correction_status(self):
        """Get the current status of the speed correction flag.
        Returns: '0' inactive, '1' active.
        """
        message = ':GSC#'
        return self.query(message)

    def get_mount_status_deprecated(self):
        """Deprecated status query (no '#' terminator) - use get_mount_status() instead.
        Returns: a number, see get_mount_status() for codes.
        """
        message = ':GSTAT#'
        return self.query(message)

    def get_mount_status(self):
        """Get the current status of the mount.
        Returns: number 0-11/98/99 terminated by '#'. 0=tracking,1=stopped,2=slewing to park,
        3=unparking,4=slewing to home,5=parked,6=slewing,7=tracking off/not moving,
        8=motors inhibited (low temp),9=tracking on but outside limits,
        10=following satellite trajectory,11=needs user intervention (see USEROK),
        98=unknown,99=error. Available from v2.8.8.
        """
        message = ':Gstat#'
        return self.query(message)

    def get_slew_settle_time(self):
        """Get the slew settle time.
        Returns: NNNNN.NNN# seconds. Available from v2.9.14.
        """
        message = ':Gstm#'
        return self.query(message)

    def get_dome_settle_time(self):
        """Get the dome settle time.
        Returns: NNNNN.NNN# seconds. Available from v2.9.14.
        """
        message = ':GDstm#'
        return self.query(message)

    def get_meridian_limit_tracking(self):
        """Get the meridian limit for tracking, in degrees.
        Returns: NN#. Available from v2.11.
        """
        message = ':Glmt#'
        return self.query(message)

    def get_meridian_limit_slews(self):
        """Get the meridian limit for slews, in degrees.
        Returns: NN#. Available from v2.11.
        """
        message = ':Glms#'
        return self.query(message)

    def get_meridian_flip_time(self):
        """Get the estimated time to tracking end due to horizon/flip limits.
        Returns: NNNN# minutes of time. Available from v2.11.
        """
        message = ':Gmte#'
        return self.query(message)

    def get_unattended_flip_setting(self):
        """Get the unattended meridian flip setting.
        Returns: '0' disabled, '1' enabled. Available from v2.11.
        """
        message = ':Guaf#'
        return self.query(message)

    def get_tracking_rate(self):
        """Get the tracking rate (LX200-compatible frequency emulation).
        Returns: TT.T# - divide by four to obtain arcseconds per second of time.
        """
        message = ':GT#'
        return self.query(message)

    def get_site_latitude(self):
        """Get the current site latitude (positive implies north).
        Returns: sDD*MM# / sDD*MM:SS# / sDD:MM:SS.S# depending on emulation/precision.
        """
        message = ':Gt#'
        return self.query(message)

    def get_element_temperature(self, n):
        """Get the temperature of element n.
        Format: n = ASCII digit: 1 RA/Az motor driver, 2 Dec/Alt motor driver, 7 RA/Az motor,
        8 Dec/Alt motor, 9 electronics box sensor, 11-13 keypad v2 sensors.
        Returns: +TTT.T# degrees Celsius, or "Unavailable#". Available from v2.3.0.
        """
        message = ':GTMP' + str(n) + '#'
        return self.query(message)

    def get_low_temperature_status(self):
        """Get the status of low temperature detection limiting slew performance.
        Returns: '0' no low temperature condition, '1' condition detected. Available from v2.14.8.
        """
        message = ':GTMPLT#'
        return self.query(message)

    def get_motor_overheat_threshold(self, n):
        """Get the overheat temperature threshold for a motor.
        Format: n = ASCII digit, 7 (RA/Az motor) or 8 (Dec/Alt motor).
        Returns: sTTT.T# degrees Celsius, or '1' if n invalid. Special-purpose mounts only. Available from v2.7.8.
        """
        message = ':GTMPOH' + str(n) + '#'
        return self.query(message)

    def get_motor_temperature_thresholds(self, n):
        """Get the three temperature thresholds (T0, T1, T2) for a motor.
        Format: n = ASCII digit, 7 (RA/Az motor) or 8 (Dec/Alt motor).
        Returns: "sTTT.T,sTTT.T,sTTT.T#", or '1' if n invalid. Special-purpose mounts only. Available from v2.3.0.
        """
        message = ':GTMPTH' + str(n) + '#'
        return self.query(message)

    def get_tracking_status(self):
        """Get the current tracking status of the mount.
        Returns: '0' not tracking, '1' tracking. Available from v2.3.0.
        """
        message = ':GTRK#'
        return self.query(message)

    def get_target_tracking_status(self):
        """Get whether the target object is at a position where tracking is allowed.
        Returns: '0' not allowed, '1' allowed. Available from v2.3.0.
        """
        message = ':GTTRK#'
        return self.query(message)

    def get_destination_side(self):
        """Get the destination side of the pier for the current target.
        Returns: '0' no target/not possible, '2' would slew to west side, '3' would slew to east side.
        Available from v2.9.9.
        """
        message = ':GTsid#'
        return self.query(message)

    def get_firmware_date(self):
        """Get the firmware release date.
        Returns: "mmm dd yyyy#" (three-letter month, day, year).
        """
        message = ':GVD#'
        return self.query(message)

    def get_firmware_number(self):
        """Get the firmware version string.
        Returns: "<string>#" firmware revision.
        """
        message = ':GVN#'
        return self.query(message)

    def get_product_name(self):
        """Get the mount product name.
        Returns: "<string>#", e.g. "10micron GM2000HPS#".
        """
        message = ':GVP#'
        return self.query(message)

    def get_firmware_time(self):
        """Get the firmware build time.
        Returns: HH:MM:SS#.
        """
        message = ':GVT#'
        return self.query(message)

    def get_control_box_version(self):
        """Get the control box hardware version.
        Returns: "Q-TYPE2012#", "PRE2012#", or "UNKNOWN#". Available from v2.9.9.
        """
        message = ':GVZ#'
        return self.query(message)

    def get_wireless_available(self):
        """Query whether a wireless adapter is available (not whether it is active).
        Returns: '0#' not available, '1#' available. Available from v2.10.
        """
        message = ':GWAV#'
        return self.query(message)

    def start_wireless_scan(self):
        """Start scanning for wireless access points.
        Returns: '0#' no wireless available, '1#' wireless adapter available. Available from v2.10.
        """
        message = ':GWRSC#'
        return self.query(message)

    def get_wireless_access_points(self):
        """Get the wireless access points found by the last scan.
        Returns: '0#' if unavailable, otherwise "1" + comma-separated (escaped) AP names + '#'.
        Available from v2.9.8.
        """
        message = ':GWRAP#'
        return self.query(message)

    def get_wireless_ssid(self):
        """Get the ESSID of the currently connected wireless network.
        Returns: '#' if not connected, otherwise "<ESSID>#" (escaped). Available from v2.10.
        """
        message = ':GWID#'
        return self.query(message)

    def get_wireless_network_status(self):
        """Get the wireless network configuration status.
        Returns: 'E#' not configured, '0#' client mode, '1#' hotspot mode, '2#' configuring.
        Available from v2.12.25.
        """
        message = ':GWUP#'
        return self.query(message)

    def get_wireless_access_points_ex(self):
        """Get wireless access points found, including encryption information.
        Returns: '0#' if unavailable; otherwise a status digit ('1' scan underway, '2' scan finished)
        followed by a comma-separated list of encryption-flag-prefixed (escaped) AP names,
        terminated by '#'. Flags: 'o' open, 'w' WEP, '1' WPA-PSK, '2' WPA2-PSK, 'x' unsupported.
        Available from v2.10.
        """
        message = ':GWRAP2#'
        return self.query(message)

    def get_wake_on_lan_status(self):
        """Get Wake-on-LAN status.
        NOTE: ':GWOL#' does not appear in the official Mount Command Protocol v2.15.1 document;
        this method is carried over unchanged from the original module and may be mount/firmware-specific.
        Returns: mount-dependent; not documented in the v2.15.1 protocol reference.
        """
        message = ':GWOL#'
        return self.query(message)

    def get_telescope_azimuth(self):
        """Get the current telescope azimuth.
        Returns: DDD*MM# / DDD*MM:SS# / DDD:MM:SS.S# depending on precision.
        """
        message = ':GZ#'
        return self.query(message)

    def get_target_azimuth(self):
        """Get the current target azimuth.
        Returns: DDD*MM# / DDD*MM:SS# / DDD:MM:SS.S# depending on precision.
        """
        message = ':Gz#'
        return self.query(message)

    def get_point_state(self):
        """Get the side of the pier on which the telescope is currently positioned.
        Returns: "East#" or "West#".
        """
        message = ':pS#'
        return self.query(message)

    def get_emulated_firmware_revision(self):
        """Get the emulated firmware revision (for compatibility with software requiring it).
        Returns: "G#".
        """
        message = ':V#'
        return self.query(message)



    #########################################################################
    #                         Home and Park Commands
    #########################################################################

    def seek_home_and_store(self):
        """Seek the home position and store alignment/encoder data there (GM4000QCI/AZ2000QCI only).
        """
        message = ':hS#'
        return self.command(message)

    def seek_home_and_align(self):
        """Seek the home position and set/align the scope from stored data (GM4000QCI/AZ2000QCI only).
        """
        message = ':hF#'
        return self.command(message)

    def slew_to_park_h(self):
        """Slew to the stored park position (alternate command to :KA#).
        """
        message = ':hP#'
        return self.command(message)

    def slew_to_park(self):
        """Slew the mount to the stored park position.
        """
        message = ':KA#'
        return self.command(message)

    def unpark(self):
        """Unpark the mount and enable movement.
        """
        message = ':PO#'
        return self.command(message)

    def query_home_status(self):
        """Query the home search status of the mount.
        Returns: '0' home search failed, '1' home search found, '2' home search in progress.
        """
        message = ':h?#'
        return self.query(message)



    #########################################################################
    #                       Movement Commands
    #########################################################################

    def move_north(self):
        """Start manual movement north (or up, for altazimuth mounts) at the current rate.
        """
        message = ':Mn#'
        return self.command(message)

    def stop_north(self):
        """Halt northward (or upward) movement.
        """
        message = ':Qn#'
        return self.command(message)

    def move_south(self):
        """Start manual movement south (or down) at the current rate.
        """
        message = ':Ms#'
        return self.command(message)

    def stop_south(self):
        """Halt southward (or downward) movement.
        """
        message = ':Qs#'
        return self.command(message)

    def move_east(self):
        """Start manual movement east (or left) at the current rate.
        """
        message = ':Me#'
        return self.command(message)

    def stop_east(self):
        """Halt eastward (or leftward) movement.
        """
        message = ':Qe#'
        return self.command(message)

    def move_west(self):
        """Start manual movement west (or right) at the current rate.
        """
        message = ':Mw#'
        return self.command(message)

    def stop_west(self):
        """Halt westward (or rightward) movement.
        """
        message = ':Qw#'
        return self.command(message)

    def guide_correction_north(self, xxxx):
        """Correct position north (or up) by a given duration at the current autoguide speed.
        Format: xxxx = milliseconds, integer string, up to 4 digits (max length 9999ms from fw 2.10).
        """
        message = ':Mgn' + str(xxxx) + '#'
        return self.command(message)

    def guide_correction_south(self, xxxx):
        """Correct position south (or down) by a given duration at the current autoguide speed.
        Format: xxxx = milliseconds, integer string, up to 4 digits (max length 9999ms from fw 2.10).
        """
        message = ':Mgs' + str(xxxx) + '#'
        return self.command(message)

    def guide_correction_east(self, xxxx):
        """Correct position east (or left) by a given duration at the current autoguide speed.
        Format: xxxx = milliseconds, integer string, up to 4 digits (max length 9999ms from fw 2.10).
        """
        message = ':Mge' + str(xxxx) + '#'
        return self.command(message)

    def guide_correction_west(self, xxxx):
        """Correct position west (or right) by a given duration at the current autoguide speed.
        Format: xxxx = milliseconds, integer string, up to 4 digits (max length 9999ms from fw 2.10).
        """
        message = ':Mgw' + str(xxxx) + '#'
        return self.command(message)

    def slew_to_altaz(self):
        """Start a slew to the previously defined target altitude/azimuth (no tracking afterwards).
        Format: no input (set target first with set_target_altitude()/set_target_azimuth()).
        Returns: '0' no error; or an error string: "1Object Below Horizon #", "2Object Below Higher #",
        "3Cannot Perform Slew #", "4Mount Parked #", "5Object on the other side #".
        """
        message = ':MA#'
        return self.query(message)

    def slew_to_target(self):
        """Start a slew to the previously defined target RA/Dec (tracking starts afterwards).
        Format: no input (set target first with set_target_ra()/set_target_declination()).
        Returns: '0' no error; or an error string: "1Object Below Horizon #", "2Object Below Higher #",
        "3Cannot Perform Slew #", "4Mount Parked #", "5Object on the other side #".
        """
        message = ':MS#'
        return self.query(message)

    def slew_to_target_side(self, n):
        """Slew to the previously defined target RA/Dec, forcing a specific pier side.
        Format: n = 2 (west) or 3 (east).
        Returns: same error codes as slew_to_target(). Available from v2.9.9.
        """
        message = ':MSfs' + str(n) + '#'
        return self.query(message)

    def slew_to_target_no_fine_limit(self):
        """Slew to the previously defined target RA/Dec, ignoring the fine movement same-side limit.
        Returns: same error codes as slew_to_target(). Available from v2.11.
        """
        message = ':MSnf#'
        return self.query(message)

    def swap_east_west(self):
        """Swap the east and west movement directions.
        """
        message = ':EW#'
        return self.command(message)

    def swap_north_south(self):
        """Swap the north and south movement directions.
        """
        message = ':NS#'
        return self.command(message)

    def halt_slew(self):
        """Immediately halt all current slewing.
        """
        message = ':Q#'
        return self.command(message)

    def meridian_flip(self):
        """Force a meridian flip (equatorial mounts) or a 360-degree azimuth turn near lowest culmination (AZ2000).
        Returns: '1' if successful, '0' if the movement cannot be done.
        """
        message = ':FLIP#'
        return self.query(message)

    def get_slew_status(self):
        """Get the progress of the current slew operation.
        Returns: string with a single block character (0x7F) if a slew is in progress/settling,
        or '#' alone if no slew is underway/it has completed.
        """
        message = ':D#'
        return self.query(message)

    def compat_high_precision_toggle(self):
        """LX200-compatibility no-op included for LX200 high-precision toggle compatibility.
        Returns: nothing (this command does nothing on 10micron mounts).
        """
        message = ':P#'
        return self.command(message)

    def nudge(self, direction):
        """Perform a small manual movement (as a raw NUDGE payload string) in the specified direction.
        Format: direction = the raw payload appended after ':NUDGE' and before the trailing '#'
        (per protocol this should be 'sXXXX,sYYYY' - signed arcsecond offsets for the
        RA/azimuth axis and declination/altitude axis; see nudge_offset() for a version that
        builds this string for you).
        Returns: '0' no error, "1Object Below Horizon #", "2Object Below Higher #",
        "3Cannot Perform Nudge #". Available from v2.7.4.
        """
        message = ':NUDGE' + direction + '#'
        return self.query(message)

    def nudge_offset(self, ra_offset, dec_offset):
        """Move to a point offset from the current coordinates (for centering objects after a slew).
        Format: ra_offset, dec_offset = signed arcseconds, e.g. '+120', '-45' (RA/Az axis, Dec/Alt axis).
        Returns: '0' no error, "1Object Below Horizon #", "2Object Below Higher #",
        "3Cannot Perform Nudge #". Available from v2.7.4.
        """
        message = ':NUDGE' + str(ra_offset) + ',' + str(dec_offset) + '#'
        return self.query(message)



    #########################################################################
    #                         Rate Commands
    #########################################################################

    def set_centering_rate(self):
        """Set slew rate to the centering rate (2nd slowest).
        """
        message = ':RC#'
        return self.command(message)

    def set_centering_rate_n(self, n):
        """Set the centering rate to a predefined value.
        Format: n = 0 (16x/0.067 deg/s), 1 (64x/0.27 deg/s), 2 (600x/2.5 deg/s), 3 (1200x/5 deg/s).
        """
        message = ':RC' + str(n) + '#'
        return self.command(message)

    def set_guiding_rate(self):
        """Set slew rate to the guiding rate (slowest).
        """
        message = ':RG#'
        return self.command(message)

    def set_guiding_rate_n(self, n):
        """Set the guiding rate to a predefined value.
        Format: n = 0 (0.25x/3.75"/s), 1 (0.5x/7.5"/s), 2 (1.0x/15"/s).
        """
        message = ':RG' + str(n) + '#'
        return self.command(message)

    def set_find_rate(self):
        """Set slew rate to the find rate (2nd fastest).
        """
        message = ':RM#'
        return self.command(message)

    def set_max_slew_rate(self):
        """Set slew rate to the maximum (fastest).
        """
        message = ':RS#'
        return self.command(message)

    def set_slew_rate_n(self, n):
        """Set the slew rate to a predefined value.
        Format: n = 0 (1200x/5 deg/s), 1 (900x/3.75 deg/s), 2 (600x/2.5 deg/s).
        """
        message = ':RS' + str(n) + '#'
        return self.command(message)

    def set_ra_slew_rate(self, dd_d):
        """Set RA/azimuth slew rate directly.
        Format: dd_d = degrees per second, decimal string, up to 7 decimal places, e.g. '2.5000000'.
        """
        message = ':RA' + str(dd_d) + '#'
        return self.command(message)

    def set_dec_slew_rate(self, dd_d):
        """Set declination/altitude slew rate directly.
        Format: dd_d = degrees per second, decimal string, up to 7 decimal places.
        """
        message = ':RE' + str(dd_d) + '#'
        return self.command(message)

    def set_guiding_rate_value(self, ss_s):
        """Set the guiding rate directly.
        Format: ss_s = signed arcseconds per second, e.g. '+3.75', '-7.50' (max sidereal, ~15.0417"/s).
        """
        message = ':Rg' + str(ss_s) + '#'
        return self.command(message)

    def set_centering_rate_multiple(self, xxx):
        """Set the centering rate as a multiple of sidereal speed.
        Format: xxx = integer 1-255.
        Returns: nothing. Available from v2.7.8.
        """
        message = ':Rc' + str(xxx) + '#'
        return self.command(message)

    def set_slew_rate_multiple(self, xxxx):
        """Set the slew rate as a multiple of sidereal speed.
        Format: xxxx = integer 1-1200.
        Returns: nothing. Available from v2.7.8.
        """
        message = ':Rs' + str(xxxx) + '#'
        return self.command(message)

    def set_automated_slew_rate(self, xx):
        """Set the slew rate used for automated moves (does not affect manual axis movement rate).
        Format: xx = degrees per second, within the mount's allowed range.
        Returns: '0' valid, '1' invalid. Available from v2.9.9.
        """
        message = ':RMs' + str(xx) + '#'
        return self.query(message)

    def get_current_slew_rate(self):
        """Get the current slew rate.
        Returns: XX# degrees/s. Available from v2.9.9.
        """
        message = ':GMs#'
        return self.query(message)

    def get_min_slew_rate(self):
        """Get the minimum slew rate that can be set on this mount.
        Returns: XX# degrees/s. Available from v2.9.9.
        """
        message = ':GMsa#'
        return self.query(message)

    def get_max_slew_rate(self):
        """Get the maximum slew rate that can be set on this mount.
        Returns: XX# degrees/s. Available from v2.9.9.
        """
        message = ':GMsb#'
        return self.query(message)

    def get_current_guide_rate(self):
        """Get the current guide rate.
        Returns: S.SS# arcseconds/s. Available from v2.9.11.
        """
        message = ':Ggui#'
        return self.query(message)



    #########################################################################
    #                         Set Commands
    #########################################################################

    def set_dec_backlash(self, value):
        """Set declination/altitude backlash.
        Format: value = 'DD*MM:SS' (deg/arcmin/arcsec) or 'HH:MM:SS(.S)' (hours/min/sec, optional tenths).
        Returns: '1' valid.
        """
        message = ':Bd' + str(value) + '#'
        return self.query(message)

    def set_ra_backlash(self, value):
        """Set RA/azimuth backlash.
        Format: value = 'DD*MM:SS' (deg/arcmin/arcsec) or 'HH:MM:SS(.S)' (hours/min/sec, optional tenths).
        Returns: '1' valid.
        """
        message = ':Br' + str(value) + '#'
        return self.query(message)

    def set_target_altitude(self, altitude):
        """Set the target altitude for a future slew.
        Format: altitude = 'sDD*MM', 'sDD*MM:SS', or 'sDD*MM:SS.S' (sign, degrees, arcmin[, arcsec[.t]]).
        Returns: '0' object out of slew range, '1' object within slew range.
        """
        message = ':Sa' + str(altitude) + '#'
        return self.query(message)

    def set_baud_rate(self, n):
        """Set the serial baud rate (RS-232 link only).
        Format: n = ASCII digit: 0=115.2K,1=57.6K,2=38.4K,4=19.2K,6=9600,7=4800,8=2400,9=1200.
        Returns: '0' invalid rate, '1' accepted (response sent at old rate, then switches).
        """
        message = ':SB' + str(n) + '#'
        return self.query(message)

    def set_date(self, date_str):
        """Set the mount date (local time).
        Format: date_str = 'MM/DD/YY', 'MM/DD/YYYY', or 'YYYY-MM-DD'.
        Returns: '0' invalid date; otherwise a success string (format varies by emulation/precision mode).
        """
        message = ':SC' + str(date_str) + '#'
        return self.query(message)

    def set_target_declination(self, dec):
        """Set the target declination for a future slew.
        Format: dec = 'sDD*MM', 'sDD*MM:SS', or 'sDD*MM:SS.S'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sd' + str(dec) + '#'
        return self.query(message)

    def set_site_elevation(self, elevation):
        """Set the current site elevation.
        Format: elevation = 'sXXXX.X' metres, range -1000.0 to 9999.9. Available from v2.9.9.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sev' + str(elevation) + '#'
        return self.query(message)

    def set_site_longitude(self, longitude):
        """Set the current site longitude (East longitudes must be given as negative).
        Format: longitude = 'sDDD*MM', 'sDDD*MM:SS', or 'sDDD*MM:SS.S'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sg' + str(longitude) + '#'
        return self.query(message)

    def set_utc_offset(self, offset):
        """Set the number of hours added to local time to yield UTC.
        Format: offset = 'sHH.H', 'sHH:MM.M', or 'sHH:MM:SS'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':SG' + str(offset) + '#'
        return self.query(message)

    def set_max_altitude_limit(self, altitude):
        """Set the highest altitude to which the telescope will slew (always sent with a '+' prefix).
        Format: altitude = unsigned degrees value, e.g. 85 (a '+' is prepended automatically;
        use set_max_altitude_limit_signed() if you need to pass a negative value).
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sh+' + str(altitude) + '#'
        return self.query(message)

    def set_max_altitude_limit_signed(self, altitude):
        """Set the highest altitude to which the telescope will slew, with an explicit sign.
        Format: altitude = 'sDD' signed degrees, e.g. '+85'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sh' + str(altitude) + '#'
        return self.query(message)

    def set_julian_date(self, jd):
        """Set the Julian Date.
        Format: jd = 'JJJJJJJ.JJJJJJJJ', up to 8 decimal places. Not usable during a leap second.
        Returns: '0' invalid, '1' valid.
        """
        message = ':SJD' + str(jd) + '#'
        return self.query(message)

    def set_local_time(self, time_str):
        """Set the local time.
        Format: time_str = 'HH:MM:SS', 'HH:MM:SS.S', or 'HH:MM:SS.SS' (seconds may reach 60.00-60.59 on leap seconds).
        Returns: '0' invalid, '1' valid.
        """
        message = ':SL' + str(time_str) + '#'
        return self.query(message)

    def set_local_datetime(self, date_str, time_str):
        """Set the local date and time together.
        Format: date_str = 'YYYY-MM-DD' (or 'MM/DD/YY'/'MM/DD/YYYY'), time_str = 'HH:MM:SS' (or with decimals).
        Returns: '0' invalid, '1' valid. Available from v2.12.26.
        """
        message = ':SLDT' + str(date_str) + ',' + str(time_str) + '#'
        return self.query(message)

    def set_utc_datetime(self, date_str, time_str):
        """Set the UTC date and time together.
        Format: date_str = 'YYYY-MM-DD' (or 'MM/DD/YY'/'MM/DD/YYYY'), time_str = 'HH:MM:SS' (or with decimals).
        Returns: '0' invalid, '1' valid. Available from v2.12.26.
        """
        message = ':SUDT' + str(date_str) + ',' + str(time_str) + '#'
        return self.query(message)

    def set_meridian_behaviour(self, n):
        """Set the meridian side behaviour for slewing.
        Format: n = 1 (both sides), 2 (west only), 3 (east only).
        Returns: '0' invalid, '1' valid. Available from v2.7.7.
        """
        message = ':SMF' + str(n) + '#'
        return self.query(message)

    def set_min_altitude_limit(self, altitude):
        """Set the minimum altitude above the horizon to which the telescope will slew (always sent with a '+' prefix).
        Format: altitude = unsigned degrees value, range -5 to +45, e.g. 0
        (a '+' is prepended automatically; use set_min_altitude_limit_signed() for negative values).
        Returns: '0' invalid, '1' valid.
        """
        message = ':So+' + str(altitude) + '#'
        return self.query(message)

    def set_min_altitude_limit_signed(self, altitude):
        """Set the minimum altitude above the horizon to which the telescope will slew, with an explicit sign.
        Format: altitude = 'sDD' signed degrees, range -5 to +45, e.g. '-5'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':So' + str(altitude) + '#'
        return self.query(message)

    def set_target_ra(self, ra):
        """Set the target right ascension for a future slew.
        Format: ra = 'HH:MM.T', 'HH:MM:SS', 'HH:MM:SS.S', or 'HH:MM:SS.SS'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sr' + str(ra) + '#'
        return self.query(message)

    def set_relay_status(self, n, m):
        """Set the status of a user relay.
        Format: n = ASCII digit 1-6 (relay number), m = 0 (open) or 1 (closed).
        Returns: '0' invalid, '1' valid. Special-purpose mounts with external relay control only.
        """
        message = ':SRLY' + str(n) + ',' + str(m) + '#'
        return self.query(message)

    def set_refraction_status(self, n):
        """Set the status of the refraction correction.
        Format: n = 0 (deactivate) or 1 (activate).
        Returns: '0' invalid, '1' valid. Available from v2.10.
        """
        message = ':SREF' + str(n) + '#'
        return self.query(message)

    def set_atmospheric_pressure(self, pppp_p):
        """Set the atmospheric pressure used in the refraction model.
        Format: pppp_p = pressure in hPa at telescope location (not sea level), e.g. '1013.0'.
        Returns: '0' invalid, '1' valid. Available from v2.3.0.
        """
        message = ':SRPRS' + str(pppp_p) + '#'
        return self.query(message)

    def set_temperature(self, sttt_t):
        """Set the temperature used in the refraction model.
        Format: sttt_t = signed degrees Celsius, e.g. '+15.0'.
        Returns: '0' invalid, '1' valid. Available from v2.3.0.
        """
        message = ':SRTMP' + str(sttt_t) + '#'
        return self.query(message)

    def set_speed_correction_status(self, n):
        """Set the status of the speed correction flag.
        Format: n = 0 (deactivate) or 1 (activate).
        Returns: '0' invalid, '1' valid.
        """
        message = ':SSC' + str(n) + '#'
        return self.query(message)

    def set_slew_settle_time(self, seconds):
        """Set the slew settle time.
        Format: seconds = 'NNNNN.NNN', range 0-99999.
        Returns: '0' invalid, '1' valid. Available from v2.9.14.
        """
        message = ':Sstm' + str(seconds) + '#'
        return self.query(message)

    def set_dome_settle_time(self, seconds):
        """Set the dome settle time.
        Format: seconds = 'NNNNN.NNN', range 0-99999.
        Returns: '0' invalid, '1' valid. Available from v2.9.14.
        """
        message = ':SDstm' + str(seconds) + '#'
        return self.query(message)

    def set_meridian_limit_tracking(self, nn):
        """Set the meridian limit for tracking, in degrees.
        Format: nn = degrees; minimum value is the meridian limit for slews.
        Returns: '0' invalid, '1' valid. Available from v2.11.
        """
        message = ':Slmt' + str(nn) + '#'
        return self.query(message)

    def set_meridian_limit_slews(self, nn):
        """Set the meridian limit for slews, in degrees.
        Format: nn = degrees; raises the tracking limit too if set higher than it.
        Returns: '0' invalid, '1' valid. Available from v2.11.
        """
        message = ':Slms' + str(nn) + '#'
        return self.query(message)

    def set_unattended_flip(self, n):
        """Enable or disable the unattended meridian flip. Always reset to disabled after power-up.
        Format: n = 1 (enable) or 0 (disable).
        Returns: nothing. Available from v2.11.
        """
        message = ':Suaf' + str(n) + '#'
        return self.command(message)

    def set_site_latitude(self, latitude):
        """Set the current site latitude.
        Format: latitude = 'sDD*MM', 'sDD*MM:SS', or 'sDD*MM:SS.S'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':St' + str(latitude) + '#'
        return self.query(message)

    def set_motor_temperature_thresholds(self, n, t0, t1, t2):
        """Set the three temperature thresholds for a motor.
        Format: n = ASCII digit 7 (RA/Az) or 8 (Dec/Alt); t0,t1,t2 = 'sTTT.T' degrees Celsius,
        must satisfy t0 < t1 < t2, range -100 to +40.
        Returns: '0' invalid, '1' valid. Special-purpose mounts only. Available from v2.3.
        """
        message = ':STMPTH' + str(n) + ',' + str(t0) + ',' + str(t1) + ',' + str(t2) + '#'
        return self.query(message)

    def set_motor_overheat_threshold(self, n, th):
        """Set the temperature overheat threshold for a motor.
        Format: n = ASCII digit 7 (RA/Az) or 8 (Dec/Alt); th = 'sTTT.T' degrees Celsius, range 0 to +80.
        Returns: '0' invalid, '1' valid. Special-purpose mounts only. Available from v2.7.8.
        """
        message = ':STMPOH' + str(n) + ',' + str(th) + '#'
        return self.query(message)

    def stop_all_motion(self):
        """Halt all current movement, including tracking (park state preserved if parked/parking).
        Returns: nothing. Available from v2.3.
        """
        message = ':STOP#'
        return self.command(message)

    def set_wake_on_lan(self, state):
        """Enable or disable Wake-on-LAN.
        NOTE: ':SWOL#' does not appear in the official Mount Command Protocol v2.15.1 document;
        this method is carried over unchanged from the original module and may be mount/firmware-specific.
        Format: state = mount-dependent value (as passed in the original module).
        Returns: mount-dependent; not documented in the v2.15.1 protocol reference.
        """
        message = ':SWOL' + str(state) + '#'
        return self.query(message)

    def set_max_slew_rate_value(self, n):
        """Set the maximum slew rate.
        Format: n = degrees per second.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sw' + str(n) + '#'
        return self.query(message)

    def set_wireless_config(self, config_str):
        """Configure the wireless interface (hotspot or client mode).
        Format: config_str = '1,ssid,encryption,key,ip,mask' (hotspot) or
        '0,ssid,encryption,key,DHCP' or '0,ssid,encryption,key,ip,mask,gateway' (client);
        encryption is 'WEP' or 'WPA'; ssid/key are escaped strings.
        Returns: '1#' configuration succeeded, '0#' configuration failed.
        Available from v2.9.8, wireless-equipped mounts only.
        """
        message = ':SWRL' + str(config_str) + '#'
        return self.query(message)

    def shutdown_wireless(self):
        """Shut down the wireless interface.
        Returns: '1#'. Available from v2.12.3, wireless-equipped mounts only.
        """
        message = ':SWRLC#'
        return self.query(message)

    def set_lan_config(self, config_str):
        """Configure the LAN interface.
        Format: config_str = '1' (DHCP) or '0,ip address,network mask,gateway' (fixed IP).
        Returns: '1#' configuration succeeded, '0#' configuration failed. Available from v2.10.
        """
        message = ':SIP' + str(config_str) + '#'
        return self.query(message)

    def set_target_azimuth(self, azimuth):
        """Set the target azimuth for a future Alt-Az slew.
        Format: azimuth = 'DDD*MM', 'DDD*MM:SS', or 'DDD*MM:SS.S'.
        Returns: '0' invalid, '1' valid.
        """
        message = ':Sz' + str(azimuth) + '#'
        return self.query(message)



    #########################################################################
    #                         Tracking Commands
    #########################################################################

    def toggle_pec(self):
        """Toggle periodic error correction on and off (no effect if PEC training is active or unsupported).
        """
        message = ':$Q#'
        return self.command(message)

    def stop_pec(self):
        """Stop periodic error correction.
        """
        message = ':p#'
        return self.command(message)

    def activate_pec(self):
        """Activate periodic error correction.
        """
        message = ':pP#'
        return self.command(message)

    def start_pec_training(self):
        """Start periodic error correction training (default duration).
        """
        message = ':pR#'
        return self.command(message)

    def start_pec_training_ra(self, x):
        """Start periodic error correction training for the RA axis (equatorial) with a chosen duration.
        Format: x = 0 (short, ~15 min), 1 (medium, ~30 min), 2 (long, ~60 min), all at sidereal speed.
        """
        message = ':pR' + str(x) + '#'
        return self.command(message)

    def start_pec_training_altitude(self, x):
        """Start periodic error correction training for the altitude axis (altazimuth mounts).
        Format: x = 0 (short, ~15 min), 1 (medium, ~30 min), 2 (long, ~60 min), at sidereal speed.
        """
        message = ':pRa' + str(x) + '#'
        return self.command(message)

    def start_pec_training_azimuth(self, x):
        """Start periodic error correction training for the azimuth axis (altazimuth mounts).
        Format: x = 0 (short, ~15 min), 1 (medium, ~30 min), 2 (long, ~60 min), at sidereal speed.
        """
        message = ':pRz' + str(x) + '#'
        return self.command(message)

    def increment_custom_tracking_rate(self):
        """Increment the custom tracking rate by 0.025 arcseconds per second of time.
        """
        message = ':T+#'
        return self.command(message)

    def decrement_custom_tracking_rate(self):
        """Decrement the custom tracking rate by 0.025 arcseconds per second of time.
        """
        message = ':T-#'
        return self.command(message)

    def set_lunar_tracking_rate(self):
        """Set the lunar tracking rate.
        """
        message = ':TL#'
        return self.command(message)

    def set_solar_tracking_rate(self):
        """Set the solar tracking rate.
        """
        message = ':TSOLAR#'
        return self.command(message)

    def set_custom_tracking_rate_mode(self):
        """Switch to custom tracking rate mode (issue set_custom_tracking_rate_value() first).
        """
        message = ':TM#'
        return self.command(message)

    def set_default_tracking_rate(self):
        """Set the default (sidereal) tracking rate.
        """
        message = ':TQ#'
        return self.command(message)

    def set_custom_tracking_rate_value(self, ddd_ddd):
        """Set the custom tracking rate value (issue before set_custom_tracking_rate_mode()).
        Format: ddd_ddd = decimal number equal to 4x the tracking rate in arcsec/s (see get_tracking_rate()).
        """
        message = ':T' + str(ddd_ddd) + '#'
        return self.command(message)

    def set_tracking_rate_value(self, ddd_ddd):
        """Set the tracking rate directly.
        Format: ddd_ddd = decimal number equal to 4x the tracking rate in arcsec/s.
        Returns: '0' invalid, '1' valid.
        """
        message = ':ST' + str(ddd_ddd) + '#'
        return self.query(message)

    def set_lunar_tracking_rate_rt(self):
        """Set the lunar tracking rate (alternate form).
        """
        message = ':RT0#'
        return self.command(message)

    def set_solar_tracking_rate_rt(self):
        """Set the solar tracking rate (alternate form).
        """
        message = ':RT1#'
        return self.command(message)

    def set_sidereal_tracking_rate(self):
        """Set the default (sidereal) tracking rate.
        """
        message = ':RT2#'
        return self.command(message)

    def stop_tracking_rate(self):
        """Stop tracking.
        """
        message = ':RT9#'
        return self.command(message)

    def set_custom_ra_tracking_rate(self, sxxx_xxxx):
        """Set a custom tracking rate offset in right ascension, added to standard sidereal tracking.
        Format: sxxx_xxxx = signed multiple of sidereal speed, e.g. '+0.0250'.
        Returns: '1' valid. Available from v2.7.8.
        """
        message = ':RR' + str(sxxx_xxxx) + '#'
        return self.command(message)

    def set_custom_dec_tracking_rate(self, sxxx_xxxx):
        """Set a custom tracking rate in declination.
        Format: sxxx_xxxx = signed multiple of sidereal speed, e.g. '+0.0250'.
        Returns: '1' valid. Available from v2.7.8.
        """
        message = ':RD' + str(sxxx_xxxx) + '#'
        return self.command(message)

    def set_dual_axis_tracking(self, n):
        """Configure dual axis tracking. Does not start or stop tracking itself.
        Format: n = 1 (enable) or 0 (disable, equatorial mounts only).
        Returns: '1' valid, '0' invalid. Available from v2.13.9.
        """
        message = ':Sdat' + str(n) + '#'
        return self.query(message)

    def get_dual_axis_tracking(self):
        """Get the status of the dual axis tracking setting.
        Returns: '0' disabled (equatorial only), '1' enabled. Available from v2.13.9.
        """
        message = ':Gdat#'
        return self.query(message)



    #########################################################################
    #                         Precision Commands
    #########################################################################

    def toggle_precision(self):
        """Toggle between low and high precision modes (always switches to high in extended LX200 emulation).
        """
        message = ':U#'
        return self.command(message)

    def set_low_precision(self):
        """Set low precision coordinate format.
        """
        message = ':U0#'
        return self.command(message)

    def set_high_precision(self):
        """Set high precision coordinate format.
        """
        message = ':U1#'
        return self.command(message)

    def set_ultra_precision(self):
        """Set ultra precision coordinate format (removes emulation-mode differences). Available from v2.10.
        """
        message = ':U2#'
        return self.command(message)



    #########################################################################
    #                         Drive Configuration
    #########################################################################

    def set_final_approach_time_constant(self, t_tt):
        """Set the final approach time constant used when final approach mode is custom (GM3000HPS/GM4000HPS only).
        Format: t_tt = seconds, range 0.25-5.00, e.g. '1.50'.
        Returns: 'E#' not supported, '0#' failed (out of range), '1#' successful. Available from v2.14.21.
        """
        message = ':SFAtc' + str(t_tt) + '#'
        return self.query(message)

    def get_final_approach_time_constant(self):
        """Get the user-defined final approach time constant (GM3000HPS/GM4000HPS only).
        Returns: 'E#' not supported, otherwise 't.tt#' seconds. Available from v2.14.21.
        """
        message = ':GFAtc#'
        return self.query(message)

    def set_final_approach_distance_limit(self, l_ll):
        """Set the final approach distance limit used when final approach mode is custom (GM3000HPS/GM4000HPS only).
        Format: l_ll = arcminutes, range 0-9.99 (0 = always make final approach), e.g. '2.00'.
        Returns: 'E#' not supported, '0#' failed (out of range), '1#' successful. Available from v2.15.
        """
        message = ':SFAlm' + str(l_ll) + '#'
        return self.query(message)

    def get_final_approach_distance_limit(self):
        """Get the user-defined final approach distance limit (GM3000HPS/GM4000HPS only).
        Returns: 'l.ll#' arcminutes. Available from v2.15.
        """
        message = ':GFAlm#'
        return self.query(message)

    def set_final_approach_mode(self, n):
        """Set the final approach mode (GM3000HPS/GM4000HPS only).
        Format: n = 0 (standard configuration) or 1 (use user-defined time constant/distance limit).
        Returns: 'E#' not supported, '0#' failed (out of range), '1#' successful. Available from v2.14.21.
        """
        message = ':SFAmd' + str(n) + '#'
        return self.query(message)

    def get_final_approach_mode(self):
        """Get the final approach mode (GM3000HPS/GM4000HPS only).
        Returns: 'E#' not supported, '0#' standard mode, '1#' custom mode. Available from v2.14.21.
        """
        message = ':GFAmd#'
        return self.query(message)



    #########################################################################
    #                         Dome Control
    #########################################################################

    def get_dome_azimuth(self):
        """Get the current dome azimuth, if a dome is connected.
        Returns: 'XXXX#' tenths of a degree, 0-3599; '9999#' on error. Available from v1.6.4.
        """
        message = ':GDA#'
        return self.query(message)

    def get_dome_flap_status(self):
        """Get the flap status of the dome, if connected.
        Returns: '0#' no dome, '1#' closed, '2#' open, '3#' moving, '4#' not detected. Available from v2.14.17.
        """
        message = ':GDF#'
        return self.query(message)

    def get_dome_homing_status(self):
        """Get the homing operation status on the dome.
        Returns: '0#' no homing operation, '1#' in progress, '2#' completed. Available from v2.7.4.
        """
        message = ':GDH#'
        return self.query(message)

    def get_dome_shutter_status(self):
        """Get the shutter status of the dome, if connected.
        Returns: '0#' no dome, '1#' closed, '2#' open, '3#' moving, '4#' not detected. Available from v1.6.4.
        """
        message = ':GDS#'
        return self.query(message)

    def get_dome_slew_status_internal(self):
        """Get the status of the dome slew when under internal mount logic control.
        Returns: '0#' no slew in progress (dome at target), '1#' slew in progress. Available from v2.7.4.
        """
        message = ':GDW#'
        return self.query(message)

    def get_dome_slew_status_external(self):
        """Get the status of the dome slew when under external control via :SDA commands.
        Returns: '0#' no slew in progress (dome at manually set target), '1#' slew in progress.
        Available from v2.9.11.
        """
        message = ':GDw#'
        return self.query(message)

    def command_dome_flap(self, n):
        """Command the dome flap.
        Format: n = 1 (close flap) or 2 (open flap).
        Returns: '0' failure, '1' success (command received; check get_dome_flap_status() for completion).
        Available from v2.14.17.
        """
        message = ':SDF' + str(n) + '#'
        return self.query(message)

    def start_dome_homing(self):
        """Start homing on the dome (succeeds even if no dome is connected).
        Returns: '1' success (does not confirm a dome is connected). Available from v2.7.4.
        """
        message = ':SDH#'
        return self.query(message)

    def set_dome_control(self, n):
        """Set the dome control connection.
        Format: n = 0 (disconnect), 1 (dome on RS-232 port), 2 (dome on GPS port).
        Returns: '0' failure, '1' success. Available from v1.6.4.
        """
        message = ':SDM' + str(n) + '#'
        return self.query(message)

    def command_dome_shutter(self, n):
        """Command the dome shutter.
        Format: n = 1 (close shutter) or 2 (open shutter).
        Returns: '0' failure, '1' success (command received; check get_dome_flap_status() for completion).
        Available from v1.6.4.
        """
        message = ':SDS' + str(n) + '#'
        return self.query(message)

    def set_dome_radius(self, xxxx):
        """Set the dome radius.
        Format: xxxx = millimetres.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDR' + str(xxxx) + '#'
        return self.command(message)

    def set_dome_mount_type(self, n):
        """Set the mount type for dome control (GM4000 only).
        Format: n = 1 (shoulders front) or 2 (shoulders back).
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDT' + str(n) + '#'
        return self.command(message)

    def set_dome_update_interval(self, ss):
        """Set the dome position update interval.
        Format: ss = seconds between updates.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDU' + str(ss) + '#'
        return self.command(message)

    def set_dome_mount_offset_north(self, sxxxx):
        """Set the mount offset from dome centre towards North.
        Format: sxxxx = signed millimetres.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDXM' + str(sxxxx) + '#'
        return self.command(message)

    def set_dome_mount_offset_east(self, sxxxx):
        """Set the mount offset from dome centre towards East.
        Format: sxxxx = signed millimetres.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDYM' + str(sxxxx) + '#'
        return self.command(message)

    def set_dome_mount_offset_zenith(self, sxxxx):
        """Set the mount offset from dome centre towards the Zenith.
        Format: sxxxx = signed millimetres.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDZM' + str(sxxxx) + '#'
        return self.command(message)

    def set_optical_axis_distance(self, sxxxx):
        """Set the distance from the declination mounting flange to the optical axis (usually the OTA radius).
        Format: sxxxx = signed millimetres.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDX' + str(sxxxx) + '#'
        return self.command(message)

    def set_optical_axis_lateral_offset(self, sxxxx):
        """Set the lateral displacement of the optical axis from the centre of the mounting flange.
        Format: sxxxx = signed millimetres, positive towards right when viewed from the back of the OTA.
        Returns: nothing. Available from v1.6.4.
        """
        message = ':SDY' + str(sxxxx) + '#'
        return self.command(message)

    def slew_dome_to_azimuth(self, xxxx):
        """Slew the dome to a given azimuth, taking direct control from the internal mount logic.
        Format: xxxx = tenths of a degree, 0-3600.
        Returns: '0' invalid (out of range), '1' valid. Available from v2.9.11.
        """
        message = ':SDA' + str(xxxx) + '#'
        return self.query(message)

    def release_dome_control(self):
        """Release dome control back to the internal logic of the mount.
        Returns: nothing. Available from v2.9.11.
        """
        message = ':SDAr#'
        return self.command(message)



    #########################################################################
    #                 Axis Angular Position Commands
    #########################################################################

    def get_ra_axis_position(self):
        """Get the angular position of the RA axis (equatorial) or azimuth axis (altazimuth).
        Returns: 'sXXX.XXXX#' signed degrees. Available from v2.9.9.
        """
        message = ':GaXa#'
        return self.query(message)

    def get_dec_axis_position(self):
        """Get the angular position of the Dec axis (equatorial) or altitude axis (altazimuth).
        Returns: 'sXXX.XXXX#' signed degrees. Available from v2.9.9.
        """
        message = ':GaXb#'
        return self.query(message)

    def set_target_ra_axis_position(self, sxxx_xxxx):
        """Set the target angular position on the RA/azimuth axis.
        Format: sxxx_xxxx = signed degrees, e.g. '+045.1234'.
        Returns: '0' invalid (out of range), '1' valid. Available from v2.9.9.
        """
        message = ':SaXa' + str(sxxx_xxxx) + '#'
        return self.query(message)

    def set_target_dec_axis_position(self, sxxx_xxxx):
        """Set the target angular position on the Dec/altitude axis.
        Format: sxxx_xxxx = signed degrees, e.g. '+045.1234'.
        Returns: '0' invalid (out of range), '1' valid. Available from v2.9.9.
        """
        message = ':SaXb' + str(sxxx_xxxx) + '#'
        return self.query(message)

    def get_target_ra_axis_position(self):
        """Get the target angular position previously set on the RA/azimuth axis.
        Returns: 'sXXX.XXXX#' signed degrees, or 'E#' if no target has been set. Available from v2.9.9.
        """
        message = ':QaXa#'
        return self.query(message)

    def get_target_dec_axis_position(self):
        """Get the target angular position previously set on the Dec/altitude axis.
        Returns: 'sXXX.XXXX#' signed degrees, or 'E#' if no target has been set. Available from v2.9.9.
        """
        message = ':QaXb#'
        return self.query(message)

    def slew_to_axis_target(self):
        """Slew to the target angular positions set via set_target_ra_axis_position()/set_target_dec_axis_position(), then stop.
        Returns: '0' no error, "1Object Below Horizon #", "2Object Below Higher #",
        "3Cannot Perform Slew #", "4Mount Parked #". Available from v2.9.9.
        """
        message = ':MaX#'
        return self.query(message)

    def slew_to_axis_target_and_park(self):
        """Slew to the target angular positions and then park.
        Returns: '0#' no error, '1#' below lower limit, '2#' above high limit,
        '3#' cannot perform slew, '4#' already parked. Available from v2.9.9.
        """
        message = ':PaX#'
        return self.query(message)

    def set_park(self):
        """Park the mount at its current position.
        Returns: '0#' error, '1#' mount parked. Available from v2.9.9.
        """
        message = ':PiP#'
        return self.query(message)

    def slew_to_saved_park_and_park(self):
        """Slew to the previously saved park angular position and park there.
        Returns: '0#' no error, '1#' below lower limit, '2#' above high limit,
        '3#' cannot perform slew, '4#' already parked. Available from v2.9.9.
        """
        message = ':PsX#'
        return self.query(message)

    def save_current_position_as_park(self):
        """Save the current angular position as the parking position used by slew_to_saved_park_and_park().
        Returns: '0' no error / '0' error (protocol documents both as '0'; check hardware response).
        Available from v2.9.9.
        """
        message = ':PyX#'
        return self.query(message)



    #########################################################################
    #                         Dithering Commands
    #########################################################################

    def set_dithering_amount(self, ra_arcsec, dec_arcsec):
        """Set the dithering amount in right ascension and declination.
        Format: ra_arcsec, dec_arcsec = arcseconds, integer strings, range 0-30 each.
        Returns: '0#' failed, '1#' succeeded. Available from v2.14.
        """
        message = ':SditM' + str(ra_arcsec) + ',' + str(dec_arcsec) + '#'
        return self.query(message)

    def set_dithering_timer(self, delay, exposure, interval):
        """Set the dithering timer.
        Format: delay, exposure = seconds, range 0-356400; interval = seconds, range 5-356400.
        Returns: '0#' failed, '1#' succeeded. Available from v2.14.
        """
        message = ':SditT' + str(delay) + ',' + str(exposure) + ',' + str(interval) + '#'
        return self.query(message)

    def start_dithering(self):
        """Start dithering.
        Returns: '0#' failed (mount state doesn't allow dithering), '1#' succeeded. Available from v2.14.
        """
        message = ':SditS#'
        return self.query(message)

    def stop_dithering(self):
        """Stop dithering.
        Returns: '0#' failed, '1#' succeeded. Available from v2.14.
        """
        message = ':SditQ#'
        return self.query(message)

    def dither_now(self):
        """Execute a dithering step immediately. Dithering must already be active.
        Returns: '0#' failed (dithering not active), '1#' succeeded. Available from v2.14.
        """
        message = ':SditN#'
        return self.query(message)

    def get_dithering_parameters(self):
        """Get the current dithering parameters.
        Returns: "R,D,L,E,I#" - RA dither (arcsec), Dec dither (arcsec), delay (s), exposure (s), interval (s).
        Available from v2.14.
        """
        message = ':GditP#'
        return self.query(message)

    def get_dithering_status(self):
        """Get whether dithering is currently active.
        Returns: '0#' inactive, '1#' active. Available from v2.14.
        """
        message = ':GditS#'
        return self.query(message)



    #########################################################################
    #                 Satellite Orbital Elements Commands
    #########################################################################

    def load_tle_from_database(self, n):
        """Load a satellite's orbital elements from the mount's onboard TLE database.
        Format: n = index into the database, 1 to value returned by get_tle_database_count().
        Returns: 'E#' if index doesn't exist, otherwise the (escaped) two-line-element string that was loaded.
        Available from v2.13.20.
        """
        message = ':TLEDL' + str(n) + '#'
        return self.query(message)

    def get_tle_database_count(self):
        """Get the number of TLEs stored in the mount's onboard database.
        Returns: 'n#' number of TLEs. Available from v2.13.20.
        """
        message = ':TLEDN#'
        return self.query(message)

    def read_storage(self):
        """Get the currently-loaded two-line orbital elements.
        Returns: escaped string of the two-line elements (lines separated by ASCII newline),
        or 'E#' if none loaded. Available from v2.13.20.
        """
        message = ':TLEG#'
        return self.query(message)

    def write_storage(self, data):
        """Load satellite orbital elements directly, in two-line format (writes to the mount's active TLE slot).
        Format: data = escaped two-line-element string; optional satellite name line, then the two TLE lines,
        each terminated by escaped newline (\\n) and/or carriage return (\\r).
        Returns: 'E#' invalid format, 'V#' valid format. Available from v2.13.20.
        """
        message = ':TLEL0' + data + '#'
        return self.query(message)

    def get_satellite_altaz(self, jd):
        """Get the apparent altazimuth coordinates of the loaded satellite at a given Julian Date.
        Format: jd = Julian Date (UTC).
        Returns: 'E#' no TLE loaded, otherwise "+AA.AAAA,ZZZ.ZZZZ#" (altitude with refraction, azimuth).
        Available from v2.14.5.
        """
        message = ':TLEGAZ' + str(jd) + '#'
        return self.query(message)

    def get_satellite_equatorial(self, jd):
        """Get the apparent equatorial coordinates of the loaded satellite at a given Julian Date.
        Format: jd = Julian Date (UTC).
        Returns: 'E#' no TLE loaded, otherwise "RR.RRRRR,+DD.DDDD#" (RA in hours, Dec in degrees).
        Available from v2.14.5.
        """
        message = ':TLEGEQ' + str(jd) + '#'
        return self.query(message)

    def precalculate_satellite_transit(self, jd, minutes):
        """Precalculate the first satellite transit within a given time window (requires a TLE loaded via load_tle()).
        Format: jd = starting Julian Date (UTC); minutes = window length, integer 1-1440.
        Returns: 'E#' no TLE/invalid, 'N#' no passes in window, or "JDstart,JDend,flags#"
        ('flags' may contain 'F' if the mount will flip during the transit). Available from v2.13.20.
        """
        message = ':TLEP' + str(jd) + ',' + str(minutes) + '#'
        return self.query(message)

    def slew_to_satellite_transit(self):
        """Slew to the start of the satellite transit precalculated with precalculate_satellite_transit().
        Returns: 'E#' no transit precalculated, 'F#' slew failed, 'V#' slewing to start (will auto-track),
        'S#' transit already started (catching up), 'Q#' transit already ended. Available from v2.13.20.
        """
        message = ':TLES#'
        return self.query(message)

    def get_satellite_slew_status(self):
        """Get the status of a slew to a precalculated satellite transit.
        Returns: 'V#' slewing to start, 'P#' waiting at start, 'S#' catching satellite,
        'T#' tracking satellite, 'Q#' transit ended, 'E#' no slew requested. Available from v2.14.22.
        """
        message = ':TLESCK#'
        return self.query(message)



    #########################################################################
    #                         Other Commands
    #########################################################################

    def set_astro_physics_emulation(self):
        """Set Astro-Physics compatible emulation mode (no effect in ultra-precision mode).
        """
        message = ':EMUAP#'
        return self.command(message)

    def set_lx200_emulation(self):
        """Set LX200 emulation mode (no effect in ultra-precision mode).
        """
        message = ':EMULX#'
        return self.command(message)

    def start_log(self):
        """Start logging the commands received by the mount.
        """
        message = ':startlog#'
        return self.command(message)

    def stop_log(self):
        """Stop the communication log.
        """
        message = ':stoplog#'
        return self.command(message)

    def shutdown(self):
        """Shut down the mount electronics (2012-model electronics or above only). Do not cut power until '1' is returned.
        Returns: '0' failure, '1' success. Available from v2.9.2.
        """
        message = ':shutdown#'
        return self.query(message)

    def get_command_log(self):
        """Get the recorded communication log.
        Returns: text of the communication log, up to 256Kbytes.
        """
        message = ':getlog#'
        return self.query(message)

    def get_event_log(self):
        """Get the mount's event log.
        Returns: text of the event log, up to 3Kbytes. Available from v2.7.8.
        """
        message = ':evlog#'
        return self.query(message)

    def allow_movement(self):
        """Allow the mount to move again after an inconsistency has been signalled (see get_mount_status()).
        Returns: nothing. Available from v2.8.13.
        """
        message = ':USEROK#'
        return self.command(message)

    def wait_for_user_confirmation(self):
        """Stop the mount and require user confirmation (via allow_movement() or the keypad) before further movement.
        Returns: nothing. Available from v2.8.13.
        """
        message = ':USERWAIT#'
        return self.command(message)

    def get_hardware_id(self):
        """Get a unique hardware identifier for the mount (stable unless the mount is serviced).
        Returns: a 20-digit (64-bit) number terminated by '#'. Available from v2.9.11.
        """
        message = ':GETID#'
        return self.query(message)

    def adjust_mount_time(self, xxx):
        """Adjust the mount's internal time by a small amount.
        Format: xxx = signed milliseconds, range +999 to -999.
        Returns: '0#' failed, '1#' succeeded. Available from v2.10.
        """
        message = ':NUtims' + str(xxx) + '#'
        return self.query(message)