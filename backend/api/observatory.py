from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix='/api/observatory',
    tags=['observatory']
)

controller = None


def set_controller(observatory_controller):
    global controller
    controller = observatory_controller


def get_controller():
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail='Observatory controller is not initialised'
        )

    return controller


@router.get('/safety')
def safety():
    observatory_controller = get_controller()

    return {
        'success': True,
        'data': observatory_controller.get_safety_status()
    }