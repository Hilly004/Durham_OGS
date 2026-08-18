from fastapi import APIRouter, HTTPException

from Controllers.Weather_Controller import WeatherController
from pydantic import BaseModel

router = APIRouter(
    prefix='/api/weather',
    tags=['weather']
)

controller: WeatherController | None = None

class WeatherOverrideRequest(BaseModel):
    mode: str

def set_controller(weather_controller: WeatherController):
    global controller
    controller = weather_controller


def get_controller() -> WeatherController:
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail='Weather controller is not initialised'
        )

    return controller


@router.get('/status')
def status():

    weather_controller = (
        get_controller()
    )

    weather_status = (
        weather_controller
        .get_status()
    )

    return {
        'success': True,
        'data': weather_status
    }


@router.post('/connect')
def connect():
    weather_controller = get_controller()

    connected = weather_controller.connect()

    if not connected:
        raise HTTPException(
            status_code=503,
            detail='Unable to connect to weather station'
        )

    return {
        'success': True
    }


@router.post('/disconnect')
def disconnect():
    weather_controller = get_controller()

    weather_controller.disconnect()

    return {
        'success': True
    }

@router.post("/override")
def set_weather_override(
    request: WeatherOverrideRequest
):

    weather_controller = get_controller()

    mode = request.mode.lower()

    if mode == "auto":
        weather_controller.set_safety_override(None)

    elif mode == "safe":
        weather_controller.set_safety_override(True)

    elif mode == "unsafe":
        weather_controller.set_safety_override(False)

    else:
        raise HTTPException(
            status_code=400,
            detail="Override mode must be auto, safe, or unsafe"
        )

    return {
        "success": True,
        "mode": mode
    }