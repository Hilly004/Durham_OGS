from models.satellite import Satellite

class SatelliteService:

    def __init__(
            self,
            repository,
            mount
    ):
        self.repository = repository
        self.mount = mount

    
    def add_satellite(
            self,
            name,
            line1,
            line2
    ):
        satellite = Satellite(
            name=name,
            line1=line1,
            line2=line2
        )

        return self.repository.create(satellite)
    
    def list_satellites(self):
        return self.repository.get_all()
    
    def upload_to_mount(
            self,
            satellite_id
    ):
        satellite = (
            self.repository
            .get_by_id(satellite_id)
        )

        if satellite is None:
            raise Exception('Satellite not found')
        
        return self.mount.load_tle(
            satellite.line1,
            satellite.line2
        )
    
    def predict_pass(
            self,
            satellite_id,
            julian_date,
            minutes
    ):
        satellite = (
            self.repository
            .get_by_id(satellite_id)
        )

        self.mount.load_tle(
            satellite.line1,
            satellite.line2
        )

        return self.mount.predict_pass(
            julian_date,
            minutes
        )
    
    def start_tracking(
            self,
            satellite_id
    ):
        
        satellite = (
            self.repository
            .get_by_id(satellite_id)
        )

        self.mount.load_tle(
            satellite.line1,
            satellite.line2
        )

        return self.mount.start_satellite_tracking()