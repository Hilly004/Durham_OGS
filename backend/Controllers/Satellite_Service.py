import time

from models.satellite import Satellite
from Utilities.TLE_Parser import TLEParser


class SatelliteService:

    def __init__(
        self,
        repository,
        mount,
        logger=None
    ):

        self.repository = repository
        self.mount = mount
        self.logger = logger

        self.tle_parser = (
            TLEParser()
        )
        self._last_tracking_status = None


    # =========================================================
    # Logging helpers
    # =========================================================

    def _info(
        self,
        message: str
    ):

        if self.logger:

            self.logger.info(
                message,
                source="SATELLITE"
            )


    def _success(
        self,
        message: str
    ):

        if self.logger:

            self.logger.success(
                message,
                source="SATELLITE"
            )


    def _warning(
        self,
        message: str
    ):

        if self.logger:

            self.logger.warning(
                message,
                source="SATELLITE"
            )


    def _error(
        self,
        message: str
    ):

        if self.logger:

            self.logger.error(
                message,
                source="SATELLITE"
            )


    # =========================================================
    # Satellite database
    #
    # list/get are deliberately not logged because they may be
    # called frequently by the frontend.
    # =========================================================

    def list_satellites(self):

        return (
            self.repository
            .get_all()
        )


    def get_satellite(
        self,
        satellite_id: int
    ):

        satellite = (
            self.repository
            .get_by_id(
                satellite_id
            )
        )


        if satellite is None:

            return None


        return satellite


    def create_satellite(
        self,
        satellite_data
    ):

        existing = (
            self.repository
            .get_by_name(
                satellite_data.name
            )
        )


        if existing is not None:

            self._warning(
                (
                    "Satellite upload rejected: "
                    f"{satellite_data.name} "
                    "already exists"
                )
            )

            raise ValueError(
                (
                    "Satellite with this name "
                    "already exists"
                )
            )


        existing_tle = (
            self.repository
            .get_by_tle(
                satellite_data.tle_line1,
                satellite_data.tle_line2
            )
        )


        if existing_tle is not None:

            self._warning(
                (
                    "Satellite upload rejected: "
                    "TLE already stored"
                )
            )

            raise ValueError(
                "This TLE is already stored"
            )


        try:

            self.tle_parser.validate(
                satellite_data.tle_line1,
                satellite_data.tle_line2
            )


        except Exception as e:

            self._error(
                (
                    "TLE validation failed for "
                    f"{satellite_data.name}: "
                    f"{e}"
                )
            )

            raise


        satellite = Satellite(
            name=satellite_data.name,
            tle_line1=
                satellite_data.tle_line1,
            tle_line2=
                satellite_data.tle_line2
        )


        try:

            created = (
                self.repository
                .create(
                    satellite
                )
            )


            self._success(
                (
                    "Satellite stored: "
                    f"{created.name}"
                )
            )


            return created


        except Exception as e:

            self._error(
                (
                    "Failed to store satellite "
                    f"{satellite_data.name}: "
                    f"{e}"
                )
            )

            raise


    def delete_satellite(
        self,
        satellite_id: int
    ):

        satellite = (
            self.repository
            .get_by_id(
                satellite_id
            )
        )


        if satellite is None:

            return False


        satellite_name = (
            satellite.name
        )


        try:

            self.repository.delete_satellite(
                satellite
            )


            self._info(
                (
                    "Satellite deleted: "
                    f"{satellite_name}"
                )
            )


            return True


        except Exception as e:

            self._error(
                (
                    "Failed to delete satellite "
                    f"{satellite_name}: "
                    f"{e}"
                )
            )

            raise


    def delete_all_satellites(self):

        try:

            deleted_count = (
                self.repository
                .delete_all_satellites()
            )


            if deleted_count == 0:

                self._info(
                    (
                        "Delete all requested but "
                        "no satellites were stored"
                    )
                )


            else:

                self._warning(
                    (
                        f"Deleted {deleted_count} "
                        "stored satellite"
                        f"{'' if deleted_count == 1 else 's'}"
                    )
                )


            return deleted_count


        except Exception as e:

            self._error(
                (
                    "Failed to delete all "
                    f"satellites: {e}"
                )
            )

            raise


    # =========================================================
    # Pass prediction
    # =========================================================

    def predict_pass(
        self,
        satellite_id: int,
        jd: float,
        minutes: int
    ):

        satellite = (
            self.repository
            .get_by_id(
                satellite_id
            )
        )


        if satellite is None:

            return None


        satellite_name = (
            satellite.name
        )


        self._info(
            (
                "Predicting pass for "
                f"{satellite_name} "
                f"over {minutes} minutes"
            )
        )


        tle_data = (
            satellite.tle_line1
            + "\n"
            + satellite.tle_line2
            + "\n"
        )


        try:

            load_result = (
                self.mount
                .write_storage(
                    tle_data
                )
            )


            if load_result != "V#":

                self._error(
                    (
                        "Mount rejected TLE for "
                        f"{satellite_name}: "
                        f"{load_result}"
                    )
                )

                raise RuntimeError(
                    (
                        "Mount rejected TLE: "
                        f"{load_result}"
                    )
                )


            result = (
                self.mount
                .precalculate_satellite_transit(
                    jd,
                    minutes
                )
            )


            if result == "E#":

                self._error(
                    (
                        "Mount could not calculate "
                        "satellite transit for "
                        f"{satellite_name}"
                    )
                )

                raise RuntimeError(
                    (
                        "Mount could not calculate "
                        "satellite transit"
                    )
                )


            if result == "N#":

                self._info(
                    (
                        "No pass found for "
                        f"{satellite_name} "
                        f"within {minutes} minutes"
                    )
                )

                return {
                    "found": False,
                    "start_jd": None,
                    "end_jd": None,
                    "flags": None
                }


            clean_result = (
                result.rstrip("#")
            )


            parts = (
                clean_result.split(",")
            )


            if len(parts) != 3:

                self._error(
                    (
                        "Unexpected transit response "
                        f"for {satellite_name}: "
                        f"{result}"
                    )
                )

                raise RuntimeError(
                    (
                        "Unexpected transit response "
                        f"from mount: {result}"
                    )
                )


            prediction = {
                "found": True,

                "start_jd":
                    float(parts[0]),

                "end_jd":
                    float(parts[1]),

                "flags":
                    parts[2]
            }


            self._success(
                (
                    "Pass found for "
                    f"{satellite_name}"
                )
            )


            return prediction


        except RuntimeError:

            raise


        except Exception as e:

            self._error(
                (
                    "Pass prediction failed for "
                    f"{satellite_name}: "
                    f"{e}"
                )
            )

            raise


    # =========================================================
    # Satellite slew / tracking
    # =========================================================

    def slew_to_satellite(self):

        try:

            result = (
                self.mount
                .slew_to_satellite_transit()
            )


            if result == "V#":

                self._success(
                    (
                        "Satellite slew started; "
                        "moving to transit start"
                    )
                )

                return {
                    "status": "slewing",
                    "message":
                        (
                            "Slewing to satellite "
                            "transit start"
                        )
                }


            if result == "S#":

                self._warning(
                    (
                        "Satellite transit already "
                        "started; attempting catch-up"
                    )
                )

                return {
                    "status": "catching",
                    "message":
                        (
                            "Transit already started; "
                            "catching satellite"
                        )
                }


            if result == "F#":

                self._error(
                    (
                        "Mount failed to slew "
                        "to satellite"
                    )
                )

                raise RuntimeError(
                    (
                        "Mount failed to slew "
                        "to satellite"
                    )
                )


            if result == "E#":

                self._error(
                    (
                        "Satellite slew requested "
                        "without a precalculated transit"
                    )
                )

                raise RuntimeError(
                    (
                        "No satellite transit "
                        "has been precalculated"
                    )
                )


            if result == "Q#":

                self._warning(
                    (
                        "Satellite slew rejected: "
                        "transit has already ended"
                    )
                )

                raise RuntimeError(
                    (
                        "Satellite transit "
                        "has already ended"
                    )
                )


            self._error(
                (
                    "Unexpected satellite slew "
                    f"response: {result}"
                )
            )


            raise RuntimeError(
                (
                    "Unexpected satellite "
                    f"slew response: {result}"
                )
            )


        except RuntimeError:

            raise


        except Exception as e:

            self._error(
                (
                    "Satellite slew failed: "
                    f"{e}"
                )
            )

            raise


    def satellite_nudge(
        self,
        direction: str,
        duration_ms: int
    ):

        """
        Apply a short manual movement correction while the
        TenMicron mount is following a satellite trajectory.

        Satellite trajectory mode is Gstat state 10. The
        correction uses the same directional movement commands
        that were verified to move the mount during trajectory
        tracking, then stops that axis after a short duration.
        """

        direction = (
            direction
            .strip()
            .lower()
        )


        if direction not in {
            "north",
            "south",
            "east",
            "west",
        }:

            raise ValueError(
                f"Invalid satellite correction direction: {direction}"
            )


        if (
            duration_ms < 10
            or
            duration_ms > 2000
        ):

            raise ValueError(
                (
                    "Satellite correction duration "
                    "must be between 10 and 2000 ms"
                )
            )


        status_response = (
            self.mount
            .get_mount_status()
        )


        status_text = (
            str(status_response)
            .strip()
            .rstrip("#")
        )


        try:

            mount_status = int(
                status_text
            )

        except ValueError:

            raise RuntimeError(
                (
                    "Unexpected mount status response: "
                    f"{status_response!r}"
                )
            )


        if mount_status != 10:

            raise RuntimeError(
                (
                    "Satellite correction is only available "
                    "while the mount is following a satellite "
                    "trajectory (mount state 10)"
                )
            )


        if direction == "north":

            start = self.mount.move_north
            stop = self.mount.stop_north

        elif direction == "south":

            start = self.mount.move_south
            stop = self.mount.stop_south

        elif direction == "east":

            start = self.mount.move_east
            stop = self.mount.stop_east

        else:

            start = self.mount.move_west
            stop = self.mount.stop_west


        self._info(
            (
                "Satellite correction requested: "
                f"{direction}, {duration_ms} ms"
            )
        )


        try:

            start()

            time.sleep(
                duration_ms / 1000.0
            )

        finally:

            stop()


        self._success(
            (
                "Satellite correction complete: "
                f"{direction}, {duration_ms} ms"
            )
        )


        return {
            "direction": direction,
            "duration_ms": duration_ms,
            "message": (
                f"Trajectory adjusted {direction} "
                f"for {duration_ms} ms"
            ),
        }


    def stop_tracking(self):

        """
        Stop all current mount motion,
        including satellite tracking.

        TenMicron command:
            :STOP#
        """

        try:

            self.mount.stop_all_motion()


            self._info(
                "Satellite tracking stopped"
            )


            return {
                "status": "idle",
                "message":
                    "Satellite tracking stopped"
            }


        except Exception as e:

            self._error(
                (
                    "Failed to stop satellite "
                    f"tracking: {e}"
                )
            )

            raise


    # =========================================================
    # Tracking status
    #
    # IMPORTANT:
    # Do not log this method. It is polled by the frontend and
    # would otherwise flood the Activity Log.
    # =========================================================

    def get_tracking_status(self):

        result = (
            self.mount
            .get_satellite_slew_status()
        )


        status_map = {
            "V#": "slewing",
            "P#": "waiting",
            "S#": "catching",
            "T#": "tracking",
            "Q#": "ended",
            "E#": "idle",
        }


        status = (
            status_map.get(
                result
            )
        )


        if status is None:

            raise RuntimeError(
                (
                    "Unexpected satellite "
                    f"tracking status: {result}"
                )
            )


        return {
            "status": status,

            "tracking":
                result == "T#"
        }