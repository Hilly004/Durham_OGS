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

active_satellite_id = None
active_satellite_name = None

from pydantic import BaseModel, Field


activity_logger = None


def set_logger(logger):
    global activity_logger
    activity_logger = logger
    
class PassPredictionRequest(BaseModel):
    jd: float
    minutes: int = Field(
        ge=1,
        le=1440
    )

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
    
@router.get("/", response_model=list[SatelliteResponse])
def list_satellites(
    db: Session = Depends(get_db)
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    return service.list_satellites()


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

@router.post(
    "/{satellite_id}/predict",
    response_model=PassPredictionResponse
)
def predict_pass(
    satellite_id: int,
    request: PassPredictionRequest,
    db: Session = Depends(get_db),
):
    global active_satellite_id
    global active_satellite_name

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    satellite = service.get_satellite(
        satellite_id
    )

    if satellite is None:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    try:
        result = service.predict_pass(
            satellite_id,
            request.jd,
            request.minutes
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

    active_satellite_id = satellite.id
    active_satellite_name = satellite.name

    return {
        "success": True,
        "data": result
    }

@router.post("/{satellite_id}/slew")
def slew_to_satellite(
    satellite_id: int,
    db: Session = Depends(get_db),
):
    global active_satellite_id
    global active_satellite_name

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    satellite = service.get_satellite(
        satellite_id
    )

    if satellite is None:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    active_satellite_id = satellite.id
    active_satellite_name = satellite.name

    try:
        result = service.slew_to_satellite()

    except RuntimeError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

    return {
        "success": True,
        "data": result
    }

@router.get(
    "/tracking/status",
    response_model=TrackingStatusResponse
)
def get_tracking_status(
    db: Session = Depends(get_db),
):
    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount()
    )

    try:
        result = service.get_tracking_status()

    except RuntimeError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

    result["satellite_id"] = (
        active_satellite_id
    )

    result["satellite_name"] = (
        active_satellite_name
    )

    return {
        "success": True,
        "data": result
    }