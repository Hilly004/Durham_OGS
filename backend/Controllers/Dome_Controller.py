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


    def get_status(self):

        connected = self.dome.is_connected()

        if not connected:
            return {
                "connected": False,
                "open": False,
                "closed": False,
                "opening": False,
                "closing": False,
            }

        return {
            "connected": True,
            "open": self.is_open,
            "closed": self.is_closed,
            "opening": self.is_opening,
            "closing": self.is_closing,
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