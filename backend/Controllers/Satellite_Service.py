from models.satellite import Satellite
from Utilities.TLE_Parser import TLEParser


class SatelliteService:

    def __init__(
        self,
        repository,
        mount
    ):
        self.repository = repository
        self.mount = mount
        self.tle_parser = TLEParser()


    def list_satellites(self):
        return self.repository.get_all()


    def get_satellite(
        self,
        satellite_id: int
    ):
        satellite = (
            self.repository.get_by_id(
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
            self.repository.get_by_name(
                satellite_data.name
            )
        )

        if existing is not None:
            raise ValueError(
                "Satellite with this name already exists"
            )


        existing_tle = (
            self.repository.get_by_tle(
                satellite_data.tle_line1,
                satellite_data.tle_line2
            )
        )

        if existing_tle is not None:
            raise ValueError(
                "This TLE is already stored"
            )


        self.tle_parser.validate(
            satellite_data.tle_line1,
            satellite_data.tle_line2
        )


        satellite = Satellite(
            name=satellite_data.name,
            tle_line1=satellite_data.tle_line1,
            tle_line2=satellite_data.tle_line2
        )


        return self.repository.create(
            satellite
        )


    def delete_satellite(
        self,
        satellite_id: int
    ):

        satellite = (
            self.repository.get_by_id(
                satellite_id
            )
        )

        if satellite is None:
            return False


        self.repository.delete_satellite(
            satellite
        )

        return True


    def predict_pass(
        self,
        satellite_id: int,
        jd: float,
        minutes: int
    ):

        satellite = (
            self.repository.get_by_id(
                satellite_id
            )
        )

        if satellite is None:
            return None


        tle_data = (
            satellite.tle_line1
            + "\n"
            + satellite.tle_line2
            + "\n"
        )


        load_result = (
            self.mount.write_storage(
                tle_data
            )
        )


        if load_result != "V#":
            raise RuntimeError(
                f"Mount rejected TLE: {load_result}"
            )


        result = (
            self.mount
            .precalculate_satellite_transit(
                jd,
                minutes
            )
        )


        if result == "E#":
            raise RuntimeError(
                "Mount could not calculate satellite transit"
            )


        if result == "N#":
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
            raise RuntimeError(
                (
                    "Unexpected transit response "
                    f"from mount: {result}"
                )
            )


        return {
            "found": True,
            "start_jd":
                float(parts[0]),

            "end_jd":
                float(parts[1]),

            "flags":
                parts[2]
        }


    def slew_to_satellite(self):

        result = (
            self.mount
            .slew_to_satellite_transit()
        )


        if result == "V#":
            return {
                "status": "slewing",
                "message":
                    "Slewing to satellite transit start"
            }


        if result == "S#":
            return {
                "status": "catching",
                "message":
                    "Transit already started; catching satellite"
            }


        if result == "F#":
            raise RuntimeError(
                "Mount failed to slew to satellite"
            )


        if result == "E#":
            raise RuntimeError(
                (
                    "No satellite transit "
                    "has been precalculated"
                )
            )


        if result == "Q#":
            raise RuntimeError(
                (
                    "Satellite transit "
                    "has already ended"
                )
            )


        raise RuntimeError(
            (
                "Unexpected satellite "
                f"slew response: {result}"
            )
        )


    def stop_tracking(self):

        """
        Stop all current mount motion,
        including satellite tracking.

        TenMicron command:
            :STOP#
        """

        self.mount.stop_all_motion()

        return {
            "status": "idle",
            "message":
                "Satellite tracking stopped"
        }


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
            status_map.get(result)
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