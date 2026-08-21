from fastapi import APIRouter, HTTPException
from Controllers.Mount_Controller import MountController
from pydantic import BaseModel

router = APIRouter(
    prefix='/api/mount',
    tags=['Mount']
)


controller: MountController = None
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

def set_controller(mount_controller: MountController):
    global controller
    controller = mount_controller

def get_controller():
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail = 'Mount controller is not initialised'
        )

    return controller


class SlewRequest(BaseModel):
    ra: float
    dec: float

class NudgeRequest(BaseModel):
    direction: str
    step_arcsec: int

# -------------------------------------------------------------------------------
# CONNECTION
# -------------------------------------------------------------------------------

@router.post('/connect')
def connect():

    mount_controller = get_controller()

    try:

        mount_controller.connect()

        return {
            "success": True
        }

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to mount: {e}"
        ) from e

@router.post('/disconnect')
def disconnect():
    mount_controller = get_controller()

    mount_controller.disconnect()

    return {'success': True}

# -------------------------------------------------------------------------------
# GET COMMANDS
# -------------------------------------------------------------------------------

@router.get('/status')
def status():

    result = controller.get_status()

    return {
        "success": True,
        "data": result
    }

@router.get('/position_aa')
def position_aa():
    return {
        'success': True,
        'data': controller.get_alt_az()
    }

@router.get('/position_rd')
def position_rd():
    return {
        'success': True,
        'data': controller.get_ra_dec()
    }

@router.get('/get_target_aa')
def get_target_aa():
    return {
        'success': True,
        'data': controller.get_target_alt_az()
    }

@router.get('/get_target_rd')
def get_target_rd():
    return {
        'success': True,
        'data': controller.get_target_ra_dec()
    }

# -------------------------------------------------------------------------------
# SET COMMANDS
# -------------------------------------------------------------------------------

#@router.post
# -------------------------------------------------------------------------------
# PARK COMMANDS
# -------------------------------------------------------------------------------

@router.post('/set_park')
def set_park():
    result = controller.set_park_position()
    return {'success': result}

@router.post('/slew_to_park')
def slew_to_park():
    result = controller.slew_to_park()
    return {'success': result}

@router.post('/unpark')
def unpark():
    observatory = get_observatory_controller()

    try:
        result = observatory.unpark_mount()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )

    except RuntimeError as e:
        if 'Mount not connected' in str(e):
            raise HTTPException(
                status_code=503,
                detail='Mount not connected'
            )
        raise

    if not result:
        raise HTTPException(
            status_code=409,
            detail='Mount unpark prevented by observatory safety system'
        )

    return {
        'success': True
    }

@router.post('/park')
def park():
    mount_controller = get_controller()

    try:
        result = mount_controller.slew_to_park()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )

    except RuntimeError as e:
        if 'Mount not connected' in str(e):
            raise HTTPException(
                status_code=503,
                detail='Mount not connected'
            )

        raise

    return {
        'success': result is not False
    }

# -------------------------------------------------------------------------------
# OTHER COMMANDS
# -------------------------------------------------------------------------------

@router.post('/stop')
def stop():
    mount_controller = get_controller()

    try:
        result = mount_controller.stop_motion()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )

    except RuntimeError as e:
        if 'Mount not connected' in str(e):
            raise HTTPException(
                status_code=503,
                detail='Mount not connected'
            )
        raise

    return {
        'success': result is not False
    }

@router.post('/slew')
def slew(request: SlewRequest):
    observatory = get_observatory_controller()

    try:
        result = observatory.slew_mount(
            request.ra,
            request.dec
        )

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )

    except RuntimeError as e:
        if 'Mount not connected' in str(e):
            raise HTTPException(
                status_code=503,
                detail='Mount not connected'
            )
        raise

    if not result:
        raise HTTPException(
            status_code=409,
            detail='Mount slew prevented by observatory safety system'
        )

    return {
        'success': True
    }

@router.post('/start_tracking')
def start_tracking():
    observatory = get_observatory_controller()

    try:
        result = observatory.start_tracking()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )

    except RuntimeError as e:
        if 'Mount not connected' in str(e):
            raise HTTPException(
                status_code=503,
                detail='Mount not connected'
            )
        raise

    if not result:
        raise HTTPException(
            status_code=409,
            detail='Mount tracking start prevented by observatory safety system'
        )

    return {
        'success': True
    }

@router.post('/nudge')
def nudge(
    request: NudgeRequest
):

    mount_controller = get_controller()

    try:

        mount_controller.nudge(
            request.direction,
            request.step_arcsec
        )


    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail='Mount not connected'
        )


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
            status_code=500,
            detail=f'Mount nudge failed: {e}'
        )


    return {
        'success': True
    }

@router.post("/move/{direction}")
def move(direction: str):

    controller = get_controller()

    if direction == "north":
        controller.move_north()

    elif direction == "south":
        controller.move_south()

    elif direction == "east":
        controller.move_east()

    elif direction == "west":
        controller.move_west()

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid direction"
        )

    return {
        "success": True
    }

@router.post("/stop/{direction}")
def stop(direction: str):

    controller = get_controller()

    if direction == "north":
        controller.stop_north()

    elif direction == "south":
        controller.stop_south()

    elif direction == "east":
        controller.stop_east()

    elif direction == "west":
        controller.stop_west()

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid direction"
        )

    return {
        "success": True
    }