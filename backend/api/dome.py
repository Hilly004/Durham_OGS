from fastapi import APIRouter, HTTPException
from Controllers.Dome_Controller import DomeController

router = APIRouter(
    prefix="/api/dome",
    tags=["Dome"]
)

controller: DomeController | None = None

observatory_controller = None


def set_observatory_controller(controller):
    global observatory_controller
    observatory_controller = controller


def get_observatory_controller():
    if observatory_controller is None:
        raise HTTPException(
            status_code=503,
            detail='Observatory controller is not initialised'
        )

    return observatory_controller
 
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
    observatory = get_observatory_controller()

    result = observatory.open_dome()

    if not result:
        raise HTTPException(
            status_code=409,
            detail='Dome opening prevented by observatory safety system'
        )

    return {
        'success': True
    }

@router.post('/close')
def close_dome():
    observatory = get_observatory_controller()

    try:
        result = observatory.close_dome()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Dome not connected'
        )

    return {
        'success': result is not False
    }

@router.post('/open_one')
def open_one():
    observatory = get_observatory_controller()

    result = observatory.open_left()

    if not result:
        raise HTTPException(
            status_code=409,
            detail='Left dome opening prevented by observatory safety system'
        )

    return {
        'success': True
    }


@router.post('/close_one')
def close_one():
    observatory = get_observatory_controller()

    try:
        result = observatory.close_left()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Dome not connected'
        )

    return {
        'success': result is not False
    }

@router.post('/open_two')
def open_two():
    observatory = get_observatory_controller()

    try:
        result = observatory.close_right()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Dome not connected'
        )

    return {
        'success': result is not False
    }

@router.post('/close_two')
def close_two():
    observatory = get_observatory_controller()

    result = observatory.close_right()

    return {
        'success': result is not False
    }

