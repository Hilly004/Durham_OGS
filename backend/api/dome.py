from fastapi import APIRouter
from Controllers.Dome_Controller import DomeController

router = APIRouter(
    prefix="/api/dome",
    tags=["Dome"]
)

controller: DomeController = None


def set_controller(dome_controller: DomeController):
    global controller
    controller = dome_controller


@router.get("/status")
def status():

    result = controller.get_status()

    return {
        "success": True,
        "data": result
    }