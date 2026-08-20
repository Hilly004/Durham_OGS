import socket

import serial
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.Settings_Controller import SettingsController
from Repository.SettingsRepo import SettingsRepository
from database.database import SessionLocal, get_db
from schemas.settings import (
    ConnectionTestResponse,
    SerialConnectionTest,
    SettingsResponse,
    SettingsUpdate,
    TcpConnectionTest,
)

router = APIRouter(prefix="/api/settings", tags=["Settings"])

weather_controller = None
observatory_controller = None
activity_logger = None
mount_connection = None
dome_connection = None
weather_connection = None


def set_runtime(
    weather,
    observatory,
    logger,
    mount_conn=None,
    dome_conn=None,
    weather_conn=None,
):
    global weather_controller, observatory_controller, activity_logger
    global mount_connection, dome_connection, weather_connection

    weather_controller = weather
    observatory_controller = observatory
    activity_logger = logger
    mount_connection = mount_conn
    dome_connection = dome_conn
    weather_connection = weather_conn


def _controller(db: Session):
    return SettingsController(
        SettingsRepository(db),
        weather_controller,
        observatory_controller,
        activity_logger,
        mount_connection,
        dome_connection,
        weather_connection,
    )


def apply_saved_settings():
    db = SessionLocal()
    try:
        return _controller(db).apply_saved_settings()
    finally:
        db.close()


@router.get("", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)):
    return _controller(db).get_settings()


@router.put("", response_model=SettingsResponse)
def update_settings(request: SettingsUpdate, db: Session = Depends(get_db)):
    try:
        return _controller(db).update_settings(request.model_dump())
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/test/mount", response_model=ConnectionTestResponse)
def test_mount_connection(request: TcpConnectionTest):
    try:
        with socket.create_connection((request.host, request.port), timeout=3):
            pass
        return {"success": True, "message": "Mount TCP connection successful"}
    except OSError as exc:
        raise HTTPException(status_code=502, detail=f"Mount connection failed: {exc}") from exc


@router.post("/test/dome", response_model=ConnectionTestResponse)
def test_dome_connection(request: TcpConnectionTest):
    try:
        with socket.create_connection((request.host, request.port), timeout=3):
            pass
        return {"success": True, "message": "Dome TCP connection successful"}
    except OSError as exc:
        raise HTTPException(status_code=502, detail=f"Dome connection failed: {exc}") from exc


@router.post("/test/weather", response_model=ConnectionTestResponse)
def test_weather_connection(request: SerialConnectionTest):
    try:
        connection = serial.Serial(
            port=request.port,
            baudrate=request.baudrate,
            timeout=1,
        )
        connection.close()
        return {"success": True, "message": "Weather serial port opened successfully"}
    except serial.SerialException as exc:
        raise HTTPException(status_code=502, detail=f"Weather connection failed: {exc}") from exc