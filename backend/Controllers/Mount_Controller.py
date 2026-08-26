class MountController:

    def __init__(
        self,
        mount,
        logger
    ):

        self.logger = logger
        self.mount = mount


    # ============================================================
    # Formatting / parsing helpers
    # ============================================================

    def _clean_response(
        self,
        value
    ) -> str:

        if value is None:
            return ""

        return (
            str(value)
            .strip()
            .rstrip("#")
        )


    def _parse_angle(
        self,
        value: str
    ) -> float:

        value = (
            value
            .strip()
            .rstrip("#")
        )

        value = value.replace(
            "*",
            ":"
        )

        parts = value.split(":")

        degrees = float(
            parts[0]
        )

        sign = (
            -1
            if degrees < 0
            else 1
        )

        degrees = abs(
            degrees
        )

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
            sign
            *
            (
                degrees
                +
                minutes / 60
                +
                seconds / 3600
            )
        )


    def _parse_ra(
        self,
        value: str
    ) -> float:

        value = (
            value
            .strip()
            .rstrip("#")
        )

        parts = value.split(":")

        hours = float(
            parts[0]
        )

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
            +
            minutes / 60
            +
            seconds / 3600
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
            "+"
            if dec_degrees >= 0
            else "-"
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


    def _format_longitude(
        self,
        longitude: float
    ) -> str:
        """
        Application longitude uses the normal convention:

            East  = positive
            West  = negative

        TenMicron uses the opposite sign convention
        for longitude, so invert it before sending.
        """

        mount_longitude = (
            -longitude
        )

        sign = (
            "+"
            if mount_longitude >= 0
            else "-"
        )

        value = abs(
            mount_longitude
        )

        degrees = int(
            value
        )

        minutes_float = (
            value - degrees
        ) * 60

        minutes = int(
            minutes_float
        )

        seconds = (
            minutes_float
            -
            minutes
        ) * 60


        return (
            f"{sign}"
            f"{degrees:03d}*"
            f"{minutes:02d}:"
            f"{seconds:04.1f}"
        )


    # ============================================================
    # Connection
    # ============================================================

    def connect(self):

        try:

            self.mount.connect()

            self.logger.success(
                "Mount connected",
                source="MOUNT",
            )

            return True

        except Exception as e:

            self.logger.error(
                f"Mount connection failed: {e}",
                source="MOUNT",
            )

            raise


    def disconnect(self):

        try:

            self.mount.disconnect()

            self.logger.info(
                "Mount disconnected",
                source="MOUNT",
            )

            return True


        except Exception as e:

            self.logger.error(
                (
                    "Mount disconnect failed: "
                    f"{e}"
                ),
                source="MOUNT",
            )

            return False


    def is_connected(self):

        return (
            self.mount.is_connected()
        )

    def get_health(self):

        connected = (
            self.mount.is_connected()
            if self.mount is not None
            else False
        )

        return {
            "connected": connected,
            "ready": connected,
            "fault": False,
        }

    # ============================================================
    # Manual movement
    # ============================================================

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


    # ============================================================
    # Nudge
    # ============================================================

    def nudge(
        self,
        direction: str,
        step_arcsec: int
    ):

        if not self.mount.is_connected():
            raise ConnectionError(
                "Mount not connected"
            )

        # ------------------------------------------------------------
        # Check Gstat
        # ------------------------------------------------------------

        mount_status_raw = (
            self.mount.get_mount_status()
        )

        mount_status = int(
            str(mount_status_raw)
            .strip()
            .rstrip("#")
        )

        allowed_states = {
            0,  # tracking
            1,  # stopped
            7,  # not tracking / stationary
        }

        if mount_status not in allowed_states:

            raise RuntimeError(
                f"Cannot nudge mount in state {mount_status}"
            )


        # ------------------------------------------------------------
        # Make sure any previous slew is finished
        # ------------------------------------------------------------

        slew_response = (
            self.mount.get_slew_status()
        )

        self.logger.info(
            f"Pre-nudge slew status: {slew_response}",
            source="MOUNT",
        )

        if not slew_response:

            raise RuntimeError(
                "Cannot nudge: mount movement has not completed"
            )


        # ------------------------------------------------------------
        # Calculate nudge
        # ------------------------------------------------------------

        direction = direction.lower()

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
                f"Invalid nudge direction: {direction}"
            )


        # ------------------------------------------------------------
        # Send nudge
        # ------------------------------------------------------------

        response = self.mount.nudge_offset(
            ra_offset,
            dec_offset
        )

        self.logger.info(
            (
                f"Mount nudge {direction}: "
                f"{step_arcsec} arcsec "
                f"(response: {response})"
            ),
            source="MOUNT",
        )

        return response

    # ============================================================
    # Slewing / tracking
    # ============================================================

    def slew_to_target(self):

        return (
            self.mount.slew_to_target()
        )


    def stop_motion(self):

        return (
            self.mount.stop_all_motion()
        )


    def start_tracking(self):

        result = (
            self.mount.start_tracking()
        )

        self.logger.info(
            "Mount tracking started",
            source="MOUNT",
        )

        return result


    def stop_tracking(self):

        result = (
            self.mount.stop_tracking()
        )

        self.logger.info(
            "Mount tracking stopped",
            source="MOUNT",
        )

        return result


    def slew_to_ra_dec(
        self,
        ra: float,
        dec: float
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        ra_string = (
            self._format_ra(
                ra
            )
        )

        dec_string = (
            self._format_dec(
                dec
            )
        )


        self.logger.info(
            (
                "Mount slew requested: "
                f"RA={ra_string}, "
                f"Dec={dec_string}"
            ),
            source="MOUNT"
        )


        #
        # Set RA
        #
        ra_result = (
            self.mount.set_target_ra(
                ra_string
            )
        )


        self.logger.info(
            (
                "Set target RA response: "
                f"{ra_result}"
            ),
            source="MOUNT"
        )


        if (
            str(ra_result)
            .strip()
            .strip("#")
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected target RA "
                    f"{ra_string}. "
                    f"Response: {ra_result}"
                )
            )


        #
        # Set Dec
        #
        dec_result = (
            self.mount
            .set_target_declination(
                dec_string
            )
        )


        self.logger.info(
            (
                "Set target Dec response: "
                f"{dec_result}"
            ),
            source="MOUNT"
        )


        if (
            str(dec_result)
            .strip()
            .strip("#")
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected target Dec "
                    f"{dec_string}. "
                    f"Response: {dec_result}"
                )
            )


        #
        # Start slew
        #
        result = (
            self.mount.slew_to_target()
        )


        self.logger.info(
            (
                "Mount slew response: "
                f"{result}"
            ),
            source="MOUNT"
        )


        clean_result = (
            str(result)
            .strip()
            .strip("#")
        )


        if clean_result == "0":

            self.logger.success(
                (
                    "Mount slew started: "
                    f"RA={ra_string}, "
                    f"Dec={dec_string}"
                ),
                source="MOUNT"
            )

            return True


        raise RuntimeError(
            (
                "Mount rejected slew command. "
                f"Response: {result}"
            )
        )


    # ============================================================
    # Position getters
    # ============================================================

    def get_ra(self):

        value = (
            self.mount
            .get_telescope_ra()
        )

        return (
            self._parse_ra(
                value
            )
        )


    def get_dec(self):

        value = (
            self.mount
            .get_telescope_dec()
        )

        return (
            self._parse_angle(
                value
            )
        )


    def get_ra_dec(self):

        return {
            "ra":
                self.get_ra(),

            "dec":
                self.get_dec(),
        }


    def get_alt(self):

        value = (
            self.mount
            .get_telescope_altitude()
        )

        return (
            self._parse_angle(
                value
            )
        )


    def get_az(self):

        value = (
            self.mount
            .get_telescope_azimuth()
        )

        return (
            self._parse_angle(
                value
            )
        )


    def get_alt_az(self):

        return {
            "alt":
                self.get_alt(),

            "az":
                self.get_az(),
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
            "ra":
                self.mount
                .get_telescope_ra(),

            "dec":
                self.mount
                .get_telescope_dec(),
        }


    def update_position_aa(self):

        return {
            "alt":
                self.mount
                .get_telescope_altitude(),

            "az":
                self.mount
                .get_telescope_azimuth(),
        }


    def get_info(self):

        field = (
            self.mount
            .get_info()
            .split(",")
        )


        return {
            "ra": field[0],
            "dec": field[1],
            "dir": field[2],
            "az": field[3],
            "alt": field[4],
            "jul": field[5],
            "stat": field[6],
            "slew_stat": field[7],
        }


    def log_mount_state(self):

        if not self.mount.is_connected():
            return


    def get_status(self):

        if not self.is_connected():
            return {
                "connected": False,
                "movement_status": "Disconnected",
                "tracking_status": "Off",
            }


        movement_status = "Unknown"
        tracking_status = "Unknown"


        try:

            movement_status = (
                self.get_slew_status()
            )

        except Exception as e:

            self.logger.warning(
                (
                    "Unable to read mount "
                    f"slew status: {e}"
                ),
                source="MOUNT",
            )


        try:

            tracking_status = (
                self.get_tracking_status()
            )

        except Exception as e:

            self.logger.warning(
                (
                    "Unable to read mount "
                    f"tracking status: {e}"
                ),
                source="MOUNT",
            )


        return {
            "connected": True,

            "movement_status":
                movement_status,

            "tracking_status":
                tracking_status,
        }


    # ============================================================
    # Home & park
    # ============================================================

    def slew_to_park(self):

        self.logger.info(
            "Mount parking",
            source="MOUNT",
        )

        return (
            self.mount.slew_to_park()
        )


    def set_park_position(self):

        result = (
            self.mount.set_park()
        )

        self.logger.success(
            "Mount park position set",
            source="MOUNT",
        )

        return result


    def unpark(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        self.mount.unpark()


        self.logger.success(
            "Mount unpark command sent",
            source="MOUNT",
        )


        return True


    def get_home_status(self):

        return (
            self.mount
            .query_home_status()
        )


    def seek_home_and_store(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        self.logger.info(
            "Mount home search started",
            source="MOUNT",
        )


        return (
            self.mount
            .seek_home_and_store()
        )


    def seek_home_and_align(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        self.logger.warning(
            (
                "Mount home search and "
                "alignment started"
            ),
            source="MOUNT",
        )


        return (
            self.mount
            .seek_home_and_align()
        )


    # ============================================================
    # Target setters
    # ============================================================

    def set_target_declination(self, dec):
        message = ':Sd' + str(dec) + '#'
        return self.query(
            message,
            terminator=None
        )


    def set_target_ra(self, ra):
        message = ':Sr' + str(ra) + '#'
        return self.query(
            message,
            terminator=None
        )

    def set_target_azimuth(
        self,
        az
        ):

        return (
            self.mount
            .set_target_azimuth(
                az
            )
        )


    def set_target_altitude(
        self,
        alt
    ):

        return (
            self.mount
            .set_target_altitude(
                alt
            )
        )


    # ============================================================
    # Site configuration
    # ============================================================

    def set_site_lat(
        self,
        lat
    ):

        return (
            self.mount
            .set_site_latitude(
                lat
            )
        )


    def set_site_long(
        self,
        long
    ):

        return (
            self.mount
            .set_site_longitude(
                long
            )
        )


    def get_site_configuration(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        latitude_raw = (
            self.mount
            .get_site_latitude()
        )

        longitude_raw = (
            self.mount
            .get_site_longitude()
        )

        elevation_raw = (
            self.mount
            .get_site_elevation()
        )


        latitude = (
            self._parse_angle(
                latitude_raw
            )
        )


        # TenMicron longitude uses opposite
        # sign convention to normal geographic
        # longitude.
        longitude = (
            -self._parse_angle(
                longitude_raw
            )
        )


        elevation = float(
            self._clean_response(
                elevation_raw
            )
        )


        return {
            "latitude":
                latitude,

            "longitude":
                longitude,

            "elevation_m":
                elevation,
        }


    def set_site_configuration(
        self,
        latitude: float,
        longitude: float,
        elevation_m: float
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        latitude_string = (
            self._format_dec(
                latitude
            )
        )


        longitude_string = (
            self._format_longitude(
                longitude
            )
        )


        elevation_string = (
            f"{elevation_m:+.1f}"
        )


        latitude_result = (
            self.mount
            .set_site_latitude(
                latitude_string
            )
        )


        if (
            self._clean_response(
                latitude_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected site latitude: "
                    f"{latitude_result}"
                )
            )


        longitude_result = (
            self.mount
            .set_site_longitude(
                longitude_string
            )
        )


        if (
            self._clean_response(
                longitude_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected site longitude: "
                    f"{longitude_result}"
                )
            )


        elevation_result = (
            self.mount
            .set_site_elevation(
                elevation_string
            )
        )


        if (
            self._clean_response(
                elevation_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected site elevation: "
                    f"{elevation_result}"
                )
            )


        self.logger.success(
            (
                "Mount site configured: "
                f"lat={latitude:.6f}, "
                f"lon={longitude:.6f}, "
                f"elevation={elevation_m:.1f}m"
            ),
            source="MOUNT",
        )


        return {
            "latitude":
                latitude,

            "longitude":
                longitude,

            "elevation_m":
                elevation_m,
        }


    # ============================================================
    # Time
    # ============================================================

    def get_mount_utc_datetime(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        return (
            self._clean_response(
                self.mount
                .get_utc_datetime()
            )
        )


    def set_mount_utc_datetime(
        self,
        date_string: str,
        time_string: str
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        result = (
            self.mount
            .set_utc_datetime(
                date_string,
                time_string
            )
        )


        if (
            self._clean_response(
                result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected UTC datetime: "
                    f"{result}"
                )
            )


        self.logger.success(
            (
                "Mount UTC clock synchronised: "
                f"{date_string} {time_string}"
            ),
            source="MOUNT",
        )


        return True


    # ============================================================
    # Mount information
    # ============================================================

    def get_mount_information(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        return {
            "product":
                self._clean_response(
                    self.mount
                    .get_product_name()
                ),

            "firmware":
                self._clean_response(
                    self.mount
                    .get_firmware_number()
                ),

            "firmware_date":
                self._clean_response(
                    self.mount
                    .get_firmware_date()
                ),

            "control_box":
                self._clean_response(
                    self.mount
                    .get_control_box_version()
                ),

            "connection_type":
                self._clean_response(
                    self.mount
                    .get_connection_type()
                ),

            "mount_ip":
                self._clean_response(
                    self.mount
                    .get_ip_address()
                ),
        }


    # ============================================================
    # Alignment model
    # ============================================================

    def get_alignment(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        count_response = (
            self.mount
            .get_alignment_star_count()
        )


        count_string = (
            self._clean_response(
                count_response
            )
        )


        try:

            star_count = int(
                count_string
                or
                "0"
            )

        except ValueError:

            raise RuntimeError(
                (
                    "Unexpected alignment star "
                    f"count: {count_response}"
                )
            )


        stars = []


        for index in range(
            1,
            star_count + 1
        ):

            response = (
                self.mount
                .get_alignment_star_info_polar(
                    index
                )
            )


            clean = (
                self._clean_response(
                    response
                )
            )


            if clean == "E":
                continue


            parts = clean.split(",")


            if len(parts) < 3:
                continue


            try:

                error_arcsec = float(
                    parts[2]
                )

            except ValueError:

                error_arcsec = 0.0


            polar_angle = None


            if len(parts) >= 4:

                try:

                    polar_angle = float(
                        parts[3]
                    )

                except ValueError:

                    polar_angle = None


            stars.append(
                {
                    "index":
                        index,

                    "hour_angle":
                        parts[0],

                    "declination":
                        parts[1],

                    "error_arcsec":
                        error_arcsec,

                    "polar_angle":
                        polar_angle,
                }
            )


        model = None


        if star_count >= 2:

            model_response = (
                self.mount
                .get_alignment_model_info()
            )


            clean_model = (
                self._clean_response(
                    model_response
                )
            )


            if (
                clean_model
                and
                clean_model != "E"
            ):

                parts = (
                    clean_model.split(",")
                )


                if len(parts) >= 9:

                    def number(
                        value
                    ):

                        try:
                            return float(value)

                        except ValueError:
                            return None


                    model = {
                        "azimuth":
                            number(parts[0]),

                        "altitude":
                            number(parts[1]),

                        "polar_error":
                            number(parts[2]),

                        "position_angle":
                            number(parts[3]),

                        "orthogonality_error":
                            number(parts[4]),

                        "azimuth_adjustment_turns":
                            number(parts[5]),

                        "altitude_adjustment_turns":
                            number(parts[6]),

                        "terms":
                            (
                                int(parts[7])
                                if parts[7]
                                    .lstrip("+-")
                                    .isdigit()
                                else None
                            ),

                        "expected_rms_arcsec":
                            number(parts[8]),
                    }


        return {
            "star_count":
                star_count,

            "model":
                model,

            "stars":
                stars,
        }


    def add_alignment_point(
        self,
        ra_hours: float,
        dec_degrees: float,
        name: str = "Alignment star"
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        ra_string = (
            self._format_ra(
                ra_hours
            )
        )

        dec_string = (
            self._format_dec(
                dec_degrees
            )
        )


        # Ensure the mount's selected target
        # contains the known coordinates.
        ra_result = (
            self.mount
            .set_target_ra(
                ra_string
            )
        )


        if (
            self._clean_response(
                ra_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected alignment "
                    f"RA: {ra_result}"
                )
            )


        dec_result = (
            self.mount
            .set_target_declination(
                dec_string
            )
        )


        if (
            self._clean_response(
                dec_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Mount rejected alignment "
                    f"Dec: {dec_result}"
                )
            )


        # Mode 1 tells TenMicron that syncs
        # are used to refine the alignment
        # model.
        sync_mode_result = (
            self.mount
            .set_sync_config(
                1
            )
        )


        if (
            self._clean_response(
                sync_mode_result
            )
            != "1"
        ):

            raise RuntimeError(
                (
                    "Unable to enable alignment "
                    f"sync mode: {sync_mode_result}"
                )
            )


        result = (
            self.mount
            .sync_add_alignment_point()
        )


        if (
            self._clean_response(
                result
            )
            != "V"
        ):

            raise RuntimeError(
                (
                    "Mount could not add "
                    "alignment point: "
                    f"{result}"
                )
            )


        self.logger.success(
            (
                "Alignment point added: "
                f"{name} "
                f"(RA {ra_string}, "
                f"Dec {dec_string})"
            ),
            source="MOUNT",
        )


        return {
            "name":
                name,

            "ra":
                ra_string,

            "dec":
                dec_string,

            "response":
                result,
        }


    def delete_alignment_point(
        self,
        index: int
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        result = (
            self.mount
            .delete_alignment_star(
                index
            )
        )


        success = (
            self._clean_response(
                result
            )
            == "1"
        )


        if success:

            self.logger.warning(
                (
                    "Alignment point deleted: "
                    f"{index}"
                ),
                source="MOUNT",
            )


        return success


    def delete_alignment_model(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        result = (
            self.mount
            .delete_alignment_model()
        )


        self.logger.warning(
            (
                "Active mount alignment "
                "model deleted"
            ),
            source="MOUNT",
        )


        return result


    # ============================================================
    # Saved TenMicron models
    # ============================================================

    def get_saved_models(self):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        response = (
            self.mount
            .get_model_count()
        )


        try:

            count = int(
                self._clean_response(
                    response
                )
                or
                "0"
            )

        except ValueError:

            raise RuntimeError(
                (
                    "Unexpected saved model "
                    f"count: {response}"
                )
            )


        models = []


        for index in range(
            1,
            count + 1
        ):

            name = (
                self._clean_response(
                    self.mount
                    .get_model_name(
                        index
                    )
                )
            )


            if name:

                models.append(
                    name
                )


        return models


    def save_alignment_model(
        self,
        name: str
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        name = name.strip()


        if not name:

            raise ValueError(
                "Model name cannot be empty"
            )


        if len(name) > 15:

            raise ValueError(
                (
                    "TenMicron model names "
                    "are limited to 15 characters"
                )
            )


        result = (
            self.mount.save_model(
                name
            )
        )


        success = (
            self._clean_response(
                result
            )
            == "1"
        )


        if success:

            self.logger.success(
                (
                    "Alignment model saved: "
                    f"{name}"
                ),
                source="MOUNT",
            )


        return success


    def load_alignment_model(
        self,
        name: str
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        result = (
            self.mount.load_model(
                name
            )
        )


        success = (
            self._clean_response(
                result
            )
            == "1"
        )


        if success:

            self.logger.success(
                (
                    "Alignment model loaded: "
                    f"{name}"
                ),
                source="MOUNT",
            )


        return success


    def delete_saved_model(
        self,
        name: str
    ):

        if not self.mount.is_connected():

            raise ConnectionError(
                "Mount not connected"
            )


        result = (
            self.mount.delete_model(
                name
            )
        )


        success = (
            self._clean_response(
                result
            )
            == "1"
        )


        if success:

            self.logger.warning(
                (
                    "Saved alignment model "
                    f"deleted: {name}"
                ),
                source="MOUNT",
            )


        return success


    # ============================================================
    # Target getters
    # ============================================================

    def get_target_ra(self):

        return (
            self.mount.get_target_ra()
        )


    def get_target_dec(self):

        return (
            self.mount.get_target_dec()
        )


    def get_target_ra_dec(self):

        return {
            "ra":
                self.get_target_ra(),

            "dec":
                self.get_target_dec(),
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
            "alt":
                self.get_target_altitude(),

            "az":
                self.get_target_azimuth(),
        }