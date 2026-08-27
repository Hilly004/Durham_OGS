from typing import Literal

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

last_tracking_status = None

def set_logger(logger):
    global activity_logger
    activity_logger = logger
    
class SatelliteCorrectionRequest(BaseModel):
    direction: Literal[
        "north",
        "south",
        "east",
        "west",
    ]

    duration_ms: int = Field(
        ge=10,
        le=2000
    )


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
        get_mount(),
        activity_logger
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
        get_mount(),
        activity_logger
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
        get_mount(),
        activity_logger
    )

    satellite = service.get_satellite(satellite_id)

    if satellite is None:
        raise HTTPException(
            status_code=404,
            detail='Satellite not found'
        )

    return satellite

@router.delete("/")
def delete_all_satellites(
    db: Session = Depends(get_db),
):
    global active_satellite_id
    global active_satellite_name

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount(),
        activity_logger
    )

    deleted_count = (
        service.delete_all_satellites()
    )

    active_satellite_id = None
    active_satellite_name = None

    return {
        "message": (
            f"{deleted_count} satellite"
            f"{'' if deleted_count == 1 else 's'} deleted"
        ),
        "deleted": deleted_count
    }

@router.delete("/{satellite_id}")
def delete_satellite(
    satellite_id: int,
    db: Session = Depends(get_db),
):
    global active_satellite_id
    global active_satellite_name

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount(),
        activity_logger
    )

    deleted = service.delete_satellite(
        satellite_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    if (
        active_satellite_id
        == satellite_id
    ):
        active_satellite_id = None
        active_satellite_name = None

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
        get_mount(),
        activity_logger
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
        get_mount(),
        activity_logger
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
    global last_tracking_status

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount(),
        activity_logger
    )

    try:

        result = service.get_tracking_status()

    except RuntimeError as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )


    current_status = (
        result["status"]
    )


    #
    # Only log when the tracking state changes.
    #
    if (
        current_status
        != last_tracking_status
    ):

        if activity_logger:

            if current_status == "slewing":

                if active_satellite_name:

                    activity_logger.info(
                        (
                            "Satellite slew in progress: "
                            f"{active_satellite_name}"
                        ),
                        source="SATELLITE"
                    )

                else:

                    activity_logger.info(
                        "Satellite slew in progress",
                        source="SATELLITE"
                    )


            elif current_status == "waiting":

                if active_satellite_name:

                    activity_logger.info(
                        (
                            "Waiting for transit: "
                            f"{active_satellite_name}"
                        ),
                        source="SATELLITE"
                    )

                else:

                    activity_logger.info(
                        "Waiting for satellite transit",
                        source="SATELLITE"
                    )


            elif current_status == "catching":

                if active_satellite_name:

                    activity_logger.warning(
                        (
                            "Catching satellite: "
                            f"{active_satellite_name}"
                        ),
                        source="SATELLITE"
                    )

                else:

                    activity_logger.warning(
                        "Catching satellite",
                        source="SATELLITE"
                    )


            elif current_status == "tracking":

                if active_satellite_name:

                    activity_logger.success(
                        (
                            "Tracking satellite: "
                            f"{active_satellite_name}"
                        ),
                        source="SATELLITE"
                    )

                else:

                    activity_logger.success(
                        "Satellite tracking started",
                        source="SATELLITE"
                    )


            elif current_status == "ended":

                if active_satellite_name:

                    activity_logger.info(
                        (
                            "Satellite transit ended: "
                            f"{active_satellite_name}"
                        ),
                        source="SATELLITE"
                    )

                else:

                    activity_logger.info(
                        "Satellite transit ended",
                        source="SATELLITE"
                    )


            elif (
                current_status == "idle"
                and
                last_tracking_status is not None
            ):

                activity_logger.info(
                    "Satellite tracking idle",
                    source="SATELLITE"
                )


        #
        # Remember the state so the same
        # message is not logged repeatedly.
        #
        last_tracking_status = (
            current_status
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

@router.post("/tracking/correction")
def correct_satellite_trajectory(
    request: SatelliteCorrectionRequest,
    db: Session = Depends(get_db),
):

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount(),
        activity_logger
    )

    try:

        result = service.satellite_nudge(
            request.direction,
            request.duration_ms
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )


@router.post("/tracking/stop")
def stop_satellite_tracking(
    db: Session = Depends(get_db),
):
    global active_satellite_id
    global active_satellite_name
    global last_tracking_status

    repository = SatelliteRepository(db)

    service = SatelliteService(
        repository,
        get_mount(),
        activity_logger
    )

    try:

        result = service.stop_tracking()

        active_satellite_id = None
        active_satellite_name = None
        last_tracking_status = None

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )