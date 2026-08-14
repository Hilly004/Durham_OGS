from fastapi import APIRouter, HTTPException
from Controllers.Dome_Controller import DomeController

router = APIRouter(
    prefix="/api/dome",
    tags=["Dome"]
)

controller: DomeController | None = None


def set_controller(dome_controller: DomeController):
    global controller
    controller = dome_controller

def get_controller() -> DomeController:
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail='Dome controller not initialised'
        )
    return controller

@router.post('/connect')
def connect():
    dome_controller = get_controller()

    result = dome_controller.connect()

    if not result:
        raise HTTPException(
            status_code=503,
            detail='Unable to connect to dome'
        )

    return {
        'success': True
    }

@router.post('/disconnect')
def disconnect():
    dome_controller = get_controller()

    dome_controller.disconnect()

    return {
        'success': True
    }

@router.get("/status")
def status():
    dome_controller = get_controller()
    return dome_controller.get_status()

@router.post('/open')
def open_dome():
    dome_controller = get_controller()

    result = dome_controller.open_dome()

    return {
        'success': result is not False
    }

@router.post('/close')
def close_dome():
    dome_controller = get_controller()

    result = dome_controller.close_dome()

    return {
        'success': result is not False
    }

@router.post('/open_one')
def open_one():
    dome_controller = get_controller()

    result = dome_controller.open_left()

    return {
        'success': result is not False
    }


@router.post('/close_one')
def close_one():
    dome_controller = get_controller()

    result = dome_controller.close_left()

    return {
        'success': result is not False
    }

@router.post('/open_two')
def open_two():
    dome_controller = get_controller()

    result = dome_controller.open_right()

    return {
        'success': result is not False
    }


@router.post('/close_two')
def close_two():
    dome_controller = get_controller()

    result = dome_controller.close_right()

    return {
        'success': result is not False
    }

