from fastapi import APIRouter, Depends
from Controllers.Mount_Controller import MountController


router = APIRouter(
    prefix='/api/mount',
    tags=['']
)


controller: MountController = None

def set_controller(mount_controller: MountController):
    global controller
    controller = mount_controller

# -------------------------------------------------------------------------------
# CONNECTION
# -------------------------------------------------------------------------------

@router.post('/connect')
def connect():
    result = controller.connect()
    return {'success': result}

@router.post('/disconnect')
def disconnect():
    result = controller.disconnect()
    return {'success': result}

# -------------------------------------------------------------------------------
# GET COMMANDS
# -------------------------------------------------------------------------------

@router.get('/status')
def status():

    print('Controller:', controller)
    return controller.get_status()

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
    result = controller.unpark()
    return {'success': result}