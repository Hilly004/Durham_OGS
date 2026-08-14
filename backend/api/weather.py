from fastapi import APIRouter, HTTPException

from Controllers.Weather_Controller import WeatherController


router = APIRouter(
    prefix='/api/weather',
    tags=['weather']
)

controller: WeatherController | None = None


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
    weather_controller = get_controller()

    return {
        'success': True,
        'data': {
            'connected': weather_controller.is_connected
        }
    }


@router.post('/connect')
def connect():
    weather_controller = get_controller()

    result = weather_controller.connect()

    if not result:
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