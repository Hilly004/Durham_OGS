class MountController:

    def __init__(self, mount, logger):

        self.logger = logger
        self.mount = mount


    def _parse_angle(
        self,
        value: str
    ) -> float:

        value = value.strip().rstrip('#')

        value = value.replace('*', ':')

        parts = value.split(':')

        degrees = float(parts[0])

        sign = (
            -1
            if degrees < 0
            else 1
        )

        degrees = abs(degrees)

        minutes = (
            float(parts[1])
            if len(parts) > 1
            else 0
        )

        seconds = (
            float(parts[2])
            if len(parts) > 2
            else 0
        )

        return sign * (
            degrees
            + minutes / 60
            + seconds / 3600
        )


    def _parse_ra(
        self,
        value: str
    ) -> float:

        value = (
            value
            .strip()
            .rstrip('#')
        )

        parts = value.split(':')

        hours = float(parts[0])

        minutes = (
            float(parts[1])
            if len(parts) > 1
            else 0
        )

        seconds = (
            float(parts[2])
            if len(parts) > 2
            else 0
        )

        return (
            hours
            + minutes / 60
            + seconds / 3600
        )


    def _format_ra(
        self,
        ra_hours: float
    ) -> str:

        ra_hours = (
            ra_hours % 24
        )

        hours = int(
            ra_hours
        )

        minutes_float = (
            ra_hours - hours
        ) * 60

        minutes = int(
            minutes_float
        )

        seconds = (
            minutes_float - minutes
        ) * 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:05.2f}"
        )


    def _format_dec(
        self,
        dec_degrees: float
    ) -> str:

        sign = (
            '+'
            if dec_degrees >= 0
            else '-'
        )

        dec_degrees = abs(
            dec_degrees
        )

        degrees = int(
            dec_degrees
        )

        minutes_float = (
            dec_degrees - degrees
        ) * 60

        minutes = int(
            minutes_float
        )

        seconds = (
            minutes_float - minutes
        ) * 60

        return (
            f"{sign}"
            f"{degrees:02d}*"
            f"{minutes:02d}:"
            f"{seconds:04.1f}"
        )


    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        try:

            self.mount.connect()

            self.logger.success(
                "Mount connected",
                source="MOUNT"
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Mount connection failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            return False


    def disconnect(self):

        try:

            self.mount.disconnect()

            self.logger.info(
                "Mount disconnected",
                source="MOUNT"
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Mount disconnect failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            return False


    def is_connected(self):

        return (
            self.mount.is_connected()
        )


    # =========================================================
    # Manual movement
    # =========================================================

    def move_north(self):

        try:

            self.mount.move_north()

            self.logger.info(
                "Mount moving north",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to move mount north: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_north(self):

        try:

            self.mount.stop_north()

            self.logger.info(
                "Mount north movement stopped",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop north movement: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def move_south(self):

        try:

            self.mount.move_south()

            self.logger.info(
                "Mount moving south",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to move mount south: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_south(self):

        try:

            self.mount.stop_south()

            self.logger.info(
                "Mount south movement stopped",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop south movement: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def move_west(self):

        try:

            self.mount.move_west()

            self.logger.info(
                "Mount moving west",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to move mount west: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_west(self):

        try:

            self.mount.stop_west()

            self.logger.info(
                "Mount west movement stopped",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop west movement: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def move_east(self):

        try:

            self.mount.move_east()

            self.logger.info(
                "Mount moving east",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to move mount east: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_east(self):

        try:

            self.mount.stop_east()

            self.logger.info(
                "Mount east movement stopped",
                source="MOUNT"
            )


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop east movement: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    # =========================================================
    # Nudge
    # =========================================================

    def nudge(
        self,
        direction: str,
        step_arcsec: int
    ):
        """
        Nudge the mount by a fixed angular offset.

        step_arcsec:
            Offset in arcseconds.
        """

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        if (
            step_arcsec < 1
            or
            step_arcsec > 3600
        ):

            raise ValueError(
                (
                    "Nudge step must be between "
                    "1 and 3600 arcseconds"
                )
            )


        direction = (
            direction.lower()
        )


        if direction == "north":

            ra_offset = 0
            dec_offset = step_arcsec


        elif direction == "south":

            ra_offset = 0
            dec_offset = -step_arcsec


        elif direction == "east":

            ra_offset = step_arcsec
            dec_offset = 0


        elif direction == "west":

            ra_offset = -step_arcsec
            dec_offset = 0


        else:

            raise ValueError(
                (
                    "Invalid nudge direction: "
                    f"{direction}"
                )
            )


        try:

            response = (
                self.mount.nudge_offset(
                    ra_offset,
                    dec_offset
                )
            )


            if response not in (
                "0",
                "0#",
            ):

                self.logger.error(
                    (
                        f"Mount nudge {direction} "
                        f"rejected: {response}"
                    ),
                    source="MOUNT"
                )

                raise RuntimeError(
                    (
                        "Mount rejected nudge: "
                        f"{response}"
                    )
                )


            self.logger.success(
                (
                    f"Mount nudged {direction}: "
                    f"{step_arcsec} arcsec"
                ),
                source="MOUNT"
            )


            return True


        except RuntimeError:

            raise


        except Exception as e:

            self.logger.error(
                (
                    f"Mount nudge {direction} "
                    f"failed: {e}"
                ),
                source="MOUNT"
            )

            raise


    # =========================================================
    # Slewing / tracking
    # =========================================================

    def slew_to_target(self):

        try:

            result = (
                self.mount.slew_to_target()
            )

            self.logger.success(
                "Mount slew command sent",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Mount slew failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_motion(self):

        try:

            result = (
                self.mount.stop_all_motion()
            )

            self.logger.warning(
                "Mount motion stopped",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop mount motion: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def start_tracking(self):

        try:

            result = (
                self.mount.start_tracking()
            )

            self.logger.success(
                "Mount tracking started",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to start mount tracking: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def stop_tracking(self):

        try:

            result = (
                self.mount.stop_tracking()
            )

            self.logger.info(
                "Mount tracking stopped",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to stop mount tracking: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def slew_to_ra_dec(
        self,
        ra: float,
        dec: float
    ):

        ra_string = (
            self._format_ra(ra)
        )

        dec_string = (
            self._format_dec(dec)
        )


        self.logger.info(
            (
                "RA/Dec slew requested: "
                f"RA={ra_string}, "
                f"Dec={dec_string}"
            ),
            source="MOUNT"
        )


        try:

            ra_result = (
                self.mount.set_target_ra(
                    ra_string
                )
            )


            if (
                str(ra_result)
                .strip('#')
                != '1'
            ):

                self.logger.error(
                    (
                        "Mount rejected target RA "
                        f"{ra_string}: "
                        f"{ra_result}"
                    ),
                    source="MOUNT"
                )

                return False


            dec_result = (
                self.mount
                .set_target_declination(
                    dec_string
                )
            )


            if (
                str(dec_result)
                .strip('#')
                != '1'
            ):

                self.logger.error(
                    (
                        "Mount rejected target Dec "
                        f"{dec_string}: "
                        f"{dec_result}"
                    ),
                    source="MOUNT"
                )

                return False


            result = (
                self.mount.slew_to_target()
            )


            success = (
                str(result)
                .strip('#')
                == '0'
            )


            if success:

                self.logger.success(
                    (
                        "Mount slew started: "
                        f"RA={ra_string}, "
                        f"Dec={dec_string}"
                    ),
                    source="MOUNT"
                )


            else:

                self.logger.error(
                    (
                        "Mount rejected slew command: "
                        f"{result}"
                    ),
                    source="MOUNT"
                )


            return success


        except Exception as e:

            self.logger.error(
                (
                    "RA/Dec slew failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    # =========================================================
    # Getters
    #
    # Deliberately not logged because these may be polled
    # continuously by the frontend.
    # =========================================================

    def get_ra(self):

        value = (
            self.mount
            .get_telescope_ra()
        )

        return self._parse_ra(
            value
        )


    def get_dec(self):

        value = (
            self.mount
            .get_telescope_dec()
        )

        return self._parse_angle(
            value
        )


    def get_ra_dec(self):

        return {
            'ra': self.get_ra(),
            'dec': self.get_dec()
        }


    def get_alt(self):

        value = (
            self.mount
            .get_telescope_altitude()
        )

        return self._parse_angle(
            value
        )


    def get_az(self):

        value = (
            self.mount
            .get_telescope_azimuth()
        )

        return self._parse_angle(
            value
        )


    def get_alt_az(self):

        return {
            'alt': self.get_alt(),
            'az': self.get_az()
        }


    def get_mount_status(self):

        return (
            self.mount
            .get_mount_status()
        )


    def get_slew_status(self):

        return (
            self.mount
            .get_slew_status()
        )


    def get_tracking_status(self):

        return (
            self.mount
            .get_tracking_status()
        )


    def update_position(self):

        return {
            'ra':
                self.mount
                .get_telescope_ra(),

            'dec':
                self.mount
                .get_telescope_dec()
        }


    def update_position_aa(self):

        return {
            'alt':
                self.mount
                .get_telescope_altitude(),

            'az':
                self.mount
                .get_telescope_azimuth()
        }


    def get_info(self):

        field = (
            self.mount
            .get_info()
            .split(',')
        )

        return {
            'ra': field[0],
            'dec': field[1],
            'dir': field[2],
            'az': field[3],
            'alt': field[4],
            'jul': field[5],
            'stat': field[6],
            'slew_stat': field[7]
        }


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


    # =========================================================
    # Home / Park
    # =========================================================

    def slew_to_park(self):

        try:

            result = (
                self.mount.slew_to_park()
            )

            self.logger.info(
                "Mount parking",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Mount park failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def set_park_position(self):

        try:

            result = (
                self.mount.set_park()
            )

            self.logger.success(
                "Mount park position set",
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set park position: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def unpark(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        try:

            self.mount.unpark()

            self.logger.success(
                "Mount unpark command sent",
                source="MOUNT"
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Mount unpark failed: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def get_home_status(self):

        return (
            self.mount
            .query_home_status()
        )


    # =========================================================
    # Set target
    # =========================================================

    def set_target_dec(
        self,
        dec
    ):

        try:

            result = (
                self.mount
                .set_target_declination(
                    dec
                )
            )

            self.logger.info(
                (
                    "Mount target Dec set: "
                    f"{dec}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set target Dec: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def set_target_ra(
        self,
        ra
    ):

        try:

            result = (
                self.mount
                .set_target_ra(
                    ra
                )
            )

            self.logger.info(
                (
                    "Mount target RA set: "
                    f"{ra}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set target RA: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def set_target_azimuth(
        self,
        az
    ):

        try:

            result = (
                self.mount
                .set_target_azimuth(
                    az
                )
            )

            self.logger.info(
                (
                    "Mount target azimuth set: "
                    f"{az}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set target azimuth: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def set_target_altitude(
        self,
        alt
    ):

        try:

            result = (
                self.mount
                .set_target_altitude(
                    alt
                )
            )

            self.logger.info(
                (
                    "Mount target altitude set: "
                    f"{alt}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set target altitude: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    # =========================================================
    # Site coordinates
    # =========================================================

    def set_site_lat(
        self,
        lat
    ):

        try:

            result = (
                self.mount
                .set_site_latitude(
                    lat
                )
            )

            self.logger.info(
                (
                    "Mount site latitude set: "
                    f"{lat}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set site latitude: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    def set_site_long(
        self,
        long
    ):

        try:

            result = (
                self.mount
                .set_site_longitude(
                    long
                )
            )

            self.logger.info(
                (
                    "Mount site longitude set: "
                    f"{long}"
                ),
                source="MOUNT"
            )

            return result


        except Exception as e:

            self.logger.error(
                (
                    "Failed to set site longitude: "
                    f"{e}"
                ),
                source="MOUNT"
            )

            raise


    # =========================================================
    # Target getters
    #
    # Not logged because these may also be polled.
    # =========================================================

    def get_target_ra(self):

        return (
            self.mount
            .get_target_ra()
        )


    def get_target_dec(self):

        return (
            self.mount
            .get_target_dec()
        )


    def get_target_ra_dec(self):

        return {
            'ra': self.get_target_ra(),
            'dec': self.get_target_dec()
        }


    def get_target_azimuth(self):

        return (
            self.mount
            .get_target_azimuth()
        )


    def get_target_altitude(self):

        return (
            self.mount
            .get_target_altitude()
        )


    def get_target_alt_az(self):

        return {
            'alt':
                self.get_target_altitude(),

            'az':
                self.get_target_azimuth()
        }