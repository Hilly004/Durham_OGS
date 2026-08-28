class DomeController:

    def __init__(
        self,
        dome,
        logger
    ):

        self.dome = dome
        self.logger = logger


    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        try:

            connected = (
                self.dome.connect()
            )


            if not connected:

                self.logger.error(
                    "Dome connection failed",
                    source="DOME"
                )

                return False


            if not self.dome.is_connected():

                self.logger.error(
                    (
                        "Dome connection failed: "
                        "hardware did not report connected"
                    ),
                    source="DOME"
                )

                return False


            self.logger.success(
                "Dome connected",
                source="DOME"
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Dome connection failed: "
                    f"{e}"
                ),
                source="DOME"
            )

            return False


    def disconnect(self):

        try:

            self.dome.disconnect()

            self.logger.info(
                "Dome disconnected",
                source="DOME"
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Dome disconnect failed: "
                    f"{e}"
                ),
                source="DOME"
            )

            return False


    # =========================================================
    # Status
    #
    # These are deliberately not logged because get_status()
    # is likely to be polled by the frontend.
    # =========================================================

    @property
    def is_connected(self):

        return (
            self.dome.is_connected()
        )


    @property
    def is_open(self):

        return (
            self.dome.all_open()
        )


    @property
    def is_moving(self):

        return (
            self.dome
            .either_motor_running()
        )


    @property
    def has_fault(self):

        return (
            self.dome.fault()
        )

    @property
    def is_closed(self):

        return (
            self.dome.all_closed()
        )
    
    @property
    def is_opening(self):

        return (
            self.dome.left_forward_running()
            or self.dome.right_forward_running()
        )

    @property
    def is_closing(self):

        return (
            self.dome.left_reverse_running()
            or self.dome.right_reverse_running()
        )

    
    def get_status(self):

        connected = self.dome.is_connected()

        if not connected:
            return {
                "connected": False,
                "open": False,
                "closed": False,
                "opening": False,
                "closing": False,
                "moving": False,
                "fault": False,
            }

        return {
            "connected": True,
            "open": self.is_open,
            "closed": self.is_closed,
            "opening": self.is_opening,
            "closing": self.is_closing,
            "moving": self.is_moving,
            "fault": self.has_fault,
        }


    # =========================================================
    # Full dome movement
    # =========================================================

    def open_dome(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.open_dome()
            )

            self.logger.info(
                "Dome opening",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Dome open failed: "
                    f"{e}"
                ),
                source="DOME"
            )

            raise


    def close_dome(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.close_dome()
            )

            self.logger.info(
                "Dome closing",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Dome close failed: "
                    f"{e}"
                ),
                source="DOME"
            )

            raise


    # =========================================================
    # Left shutter
    # =========================================================

    def open_left(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.open_left()
            )

            self.logger.info(
                "Left dome shutter opening",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Left dome shutter "
                    f"open failed: {e}"
                ),
                source="DOME"
            )

            raise


    def close_left(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.close_left()
            )

            self.logger.info(
                "Left dome shutter closing",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Left dome shutter "
                    f"close failed: {e}"
                ),
                source="DOME"
            )

            raise


    # =========================================================
    # Right shutter
    # =========================================================

    def open_right(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.open_right()
            )

            self.logger.info(
                "Right dome shutter opening",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Right dome shutter "
                    f"open failed: {e}"
                ),
                source="DOME"
            )

            raise


    def close_right(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.close_right()
            )

            self.logger.info(
                "Right dome shutter closing",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Right dome shutter "
                    f"close failed: {e}"
                ),
                source="DOME"
            )

            raise

    # =========================================================
    # Jog commands
    # =========================================================

    def start_jog_left_up(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.left_jog_up(True)
            )

            self.logger.info(
                "Started left dome shutter jog up",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to start left dome shutter jog up: {e}"
                ),
                source="DOME"
            )

            raise

    def stop_jog_left_up(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.left_jog_up(False)
            )

            self.logger.info(
                "Stopped left dome shutter jog up",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to stop left dome shutter jog up: {e}"
                ),
                source="DOME"
            )

            raise


    def start_jog_right_up(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.right_jog_up(True)
            )

            self.logger.info(
                "Started right dome shutter jog up",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to start right dome shutter jog up: {e}"
                ),
                source="DOME"
            )

            raise

    def stop_jog_right_up(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.right_jog_up(False)
            )

            self.logger.info(
                "Stopped right dome shutter jog up",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to stop right dome shutter jog up: {e}"
                ),
                source="DOME"
            )

            raise

    def start_jog_left_down(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.left_jog_down(True)
            )

            self.logger.info(
                "Started left dome shutter jog down",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to start left dome shutter jog down: {e}"
                ),
                source="DOME"
            )

            raise

    def stop_jog_left_down(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.left_jog_down(False)
            )

            self.logger.info(
                "Stopped left dome shutter jog down",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to stop left dome shutter jog down: {e}"
                ),
                source="DOME"
            )

            raise

    def start_jog_right_down(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.right_jog_down(True)
            )

            self.logger.info(
                "Started right dome shutter jog down",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to start right dome shutter jog down: {e}"
                ),
                source="DOME"
            )

            raise

    def stop_jog_right_down(self):

        if not self.is_connected:

            raise ConnectionError(
                "Dome not connected"
            )


        try:

            result = (
                self.dome.right_jog_down(False)
            )

            self.logger.info(
                "Stopped right dome shutter jog down",
                source="DOME"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    f"Failed to stop right dome shutter jog down: {e}"
                ),
                source="DOME"
            )

            raise

    def stop_all(self):

        if not self.is_connected:
            raise ConnectionError(
                "Dome not connected"
            )

        try:

            result = self.dome.stop_all()

            self.logger.warning(
                "Dome movement stopped",
                source="DOME"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Dome stop failed: {e}",
                source="DOME"
            )

            raise


    def stop_left(self):

        if not self.is_connected:
            raise ConnectionError(
                "Dome not connected"
            )

        try:

            result = self.dome.stop_left()

            self.logger.info(
                "Left dome shutter stopped",
                source="DOME"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Left dome stop failed: {e}",
                source="DOME"
            )

            raise


    def stop_right(self):

        if not self.is_connected:
            raise ConnectionError(
                "Dome not connected"
            )

        try:

            result = self.dome.stop_right()

            self.logger.info(
                "Right dome shutter stopped",
                source="DOME"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Right dome stop failed: {e}",
                source="DOME"
            )

            raise


    def reset_fault(self):

        if not self.is_connected:
            raise ConnectionError(
                "Dome not connected"
            )

        try:

            result = self.dome.fault_reset()

            self.logger.info(
                "Dome fault reset requested",
                source="DOME"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Dome fault reset failed: {e}",
                source="DOME"
            )

            raise