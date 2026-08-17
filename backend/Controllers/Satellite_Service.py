from models.satellite import Satellite
from Utilities.TLE_Parser import TLEParser

class SatelliteService:

    def __init__(self, repository, mount):
        self.repository = repository
        self.mount = mount
        self.tle_parser = TLEParser()


    def list_satellites(self):
        return self.repository.get_all()


    def get_satellite(self, satellite_id: int):
        satellite = self.repository.get_by_id(satellite_id)

        if satellite is None:
            return None

        return satellite


    def create_satellite(self, satellite_data):
        existing = self.repository.get_by_name(
            satellite_data.name
        )

        if existing is not None:
            raise ValueError(
                'Satellite with this name already exists'
            )
        
        existing_tle = self.repository.get_by_tle(
            satellite_data.tle_line1,
            satellite_data.tle_line2
        )

        if existing_tle is not None:
            raise ValueError(
                'This TLE is already stored'
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

        return self.repository.create(satellite)


    def delete_satellite(self, satellite_id: int):
        satellite = self.repository.get_by_id(satellite_id)

        if satellite is None:
            return False

        self.repository.delete_satellite(satellite)

        return True