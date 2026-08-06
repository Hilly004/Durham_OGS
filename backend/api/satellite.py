from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.satellite import (
    SatelliteCreate,
    SatelliteResponse,
    PassPredictionResponse,
    TrackingStatusResponse,
)
from Controllers.Satellite_Service import SatelliteService

router = APIRouter()


@router.get("/", response_model=list[SatelliteResponse])
def list_satellites(db: Session = Depends(get_db)):
    service = SatelliteService(db)
    return service.list_satellites()


@router.get("/{satellite_id}", response_model=SatelliteResponse)
def get_satellite(satellite_id: int, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    return service.get_satellite(satellite_id)


@router.post("/", response_model=SatelliteResponse)
def create_satellite(
    satellite: SatelliteCreate,
    db: Session = Depends(get_db),
):
    service = SatelliteService(db)
    return service.create_satellite(satellite)


@router.delete("/{satellite_id}")
def delete_satellite(
    satellite_id: int,
    db: Session = Depends(get_db),
):
    service = SatelliteService(db)
    service.delete_satellite(satellite_id)

    return {"message": "Satellite deleted"}