from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.satellite import (
    SatelliteCreate,
    SatelliteResponse,
    PassPredictionResponse,
    TrackingStatusResponse,
)
from Controllers.satellite_service import SatelliteService

from Repository.SatelliteRepo import SatelliteRepository

router = APIRouter()
mount = None

def set_mount(mount_driver):
    global mount
    mount = mount_driver

def get_mount():
    if mount is None:
        raise HTTPException(
            status_code=503,
            detail='Mount is not initialised'
        )

    return mount

    

@router.post("/", response_model=SatelliteResponse)
def create_satellite(
    satellite: SatelliteCreate,
    db: Session = Depends(get_db),
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    try:
        return service.create_satellite(satellite)

    except ValueError as e:
        message = str(e)

        if (
            'already exists' in message
            or 'already stored' in message
        ):
            raise HTTPException(
                status_code=409,
                detail=message
            )

        raise HTTPException(
            status_code=400,
            detail=message
        )


@router.get("/{satellite_id}", response_model=SatelliteResponse)
def get_satellite(
    satellite_id: int,
    db: Session = Depends(get_db)
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    satellite = service.get_satellite(satellite_id)

    if satellite is None:
        raise HTTPException(
            status_code=404,
            detail='Satellite not found'
        )

    return satellite


@router.post("/", response_model=SatelliteResponse)
def create_satellite(
    satellite: SatelliteCreate,
    db: Session = Depends(get_db),
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    return service.create_satellite(satellite)


@router.delete("/{satellite_id}")
def delete_satellite(
    satellite_id: int,
    db: Session = Depends(get_db),
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    deleted = service.delete_satellite(satellite_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail='Satellite not found'
        )

    return {
        "message": "Satellite deleted"
    }