from sqlalchemy.orm import Session
from models.satellite import Satellite

class SatelliteRepository:

    def __init__(self,db: Session):
        self.db=db

    def create(self, satellite: Satellite):

        self.db.add(satellite)
        self.db.commit()
        self.db.refresh(satellite)

        return satellite
    
    def get_by_id(self,satellite_id:int):
        
        return(
            self.db.query(Satellite)
            .filter(Satellite.id == satellite_id)
            .first()
        )
    
    def get_by_tle(self, tle_line1: str, tle_line2: str):
        return (
            self.db.query(Satellite)
            .filter(
                Satellite.tle_line1 == tle_line1,
                Satellite.tle_line2 == tle_line2
            )
            .first()
        )

    def get_all(self):
        
        return(
            self.db.query(Satellite)
            .all()
        )
    
    def get_by_name(self, name:str):

        return(
            self.db.query(Satellite)
            .filter(Satellite.name == name)
            .first()
        )
    
    def update(self, satellite):
        self.db.commit()
        self.db.refresh(satellite)

        return satellite
    
    def delete_satellite(self,satellite):
        self.db.delete(satellite)
        self.db.commit()
    