class AstroHavenDome:

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    #########################################################################
    #                       Connection Commands
    #########################################################################

    def connect(self):
        return self.connection.connect()

    def disconnect(self):
        return self.connection.disconnect()
    
    def is_connected(self):
        return self.connection.is_connected()

    #########################################################################
    #                       Open/Close Commands
    #########################################################################

    def open_dome(self):
        return self.connection.write_coil(
            23,
            True
        )


    def close_dome(self):
        return self.connection.write_coil(
            4,
            True
        )


    def open_left(self):
        return self.connection.write_coil(
            18,
            True
        )


    def close_left(self):
        return self.connection.write_coil(
            9,
            True
        )


    def open_right(self):
        return self.connection.write_coil(
            34,
            True
        )


    def close_right(self):
        return self.connection.write_coil(
            26,
            True
        )

    def progressive_close(self):
        self.connection.write_coil(25, True)

    #########################################################################
    #                       Jog Commands
    #########################################################################

    def left_jog_up(self):
        self.connection.write_coil(16, True)

    def left_jog_down(self):
        self.connection.write_coil(14, True)

    def right_jog_up(self):
        self.connection.write_coil(32, True)

    def right_jog_down(self):
        self.connection.write_coil(30, True)

    #########################################################################
    #                       Stop Commands
    #########################################################################

    def stop_left(self):
        self.connection.write_coil(21, True)

    def stop_right(self):
        self.connection.write_coil(37, True)

    def stop_all(self):
        self.connection.write_coil(39, True)

    #########################################################################
    #                       Reset Commands
    #########################################################################

    def fault_reset(self):
        self.connection.write_coil(8, True)

    def bg_reset(self):
        self.connection.write_coil(40, True)

    #########################################################################
    #                       Tracking Commands
    #########################################################################

    def enable_tracking(self):
        self.connection.write_coil(93, True)

    def disable_tracking(self):
        self.connection.write_coil(93, False)

    def set_target_azimuth(self, azimuth):
        self.connection.write_register(3, azimuth)

    def set_target_altitude(self, altitude):
        self.connection.write_register(2, altitude)

    #########################################################################
    #                       Angle Registers
    #########################################################################

    def get_left_angle(self):
        return self.connection.read_register(4)

    def get_right_angle(self):
        return self.connection.read_register(5)

    def get_aperture(self):
        return self.connection.read_register(6)

    def get_shutter_width(self):
        return self.connection.read_register(7)

    def get_full_travel_time(self):
        return self.connection.read_register(8)

    def get_full_travel(self):
        return self.connection.read_register(9)

    #########################################################################
    #                       Indicators
    #########################################################################

    def all_open(self):
        return self.connection.read_coil(1)

    def all_closed(self):
        return self.connection.read_coil(0)

    def close_all_indicator(self):
        return self.connection.read_coil(5)

    def open_all_indicator(self):
        return self.connection.read_coil(24)

    def left_open(self):
        return self.connection.read_coil(19)

    def right_open(self):
        return self.connection.read_coil(35)

    def left_closed(self):
        return self.connection.read_coil(10)

    def right_closed(self):
        return self.connection.read_coil(27)

    def left_up_limit(self):
        return self.connection.read_coil(22)

    def left_down_limit(self):
        return self.connection.read_coil(11)

    def right_up_limit(self):
        return self.connection.read_coil(38)

    def right_down_limit(self):
        return self.connection.read_coil(28)

    def left_forward_running(self):
        return self.connection.read_coil(12)

    def left_reverse_running(self):
        return self.connection.read_coil(20)

    def right_forward_running(self):
        return self.connection.read_coil(29)

    def right_reverse_running(self):
        return self.connection.read_coil(36)

    def left_jog_up_indicator(self):
        return self.connection.read_coil(17)

    def left_jog_down_indicator(self):
        return self.connection.read_coil(15)

    def right_jog_up_indicator(self):
        return self.connection.read_coil(33)

    def right_jog_down_indicator(self):
        return self.connection.read_coil(31)

    def either_motor_running(self):
        return self.connection.read_coil(6)

    def both_motors_running(self):
        return self.connection.read_coil(3)

    def auto_close_enabled(self):
        return self.connection.read_coil(2)

    def fault(self):
        return self.connection.read_coil(7)