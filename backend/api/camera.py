from fastapi import (
    APIRouter,
    HTTPException,
    Response
)

from pydantic import BaseModel

from Controllers.Camera_Controller import (
    CameraController
)


router = APIRouter(
    prefix="/api/camera",
    tags=["Camera"]
)


controller: CameraController | None = None


# =========================================================
# Controller setup
# =========================================================

def set_controller(
    camera_controller: CameraController
):

    global controller

    controller = camera_controller


def get_controller() -> CameraController:

    if controller is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "Camera controller "
                "is not initialised"
            )
        )

    return controller


# =========================================================
# Request models
# =========================================================

class ExposureRequest(BaseModel):
    exposure_us: float


class GainRequest(BaseModel):
    gain_db: float


# =========================================================
# Connection
# =========================================================

@router.post("/connect")
def connect():

    camera_controller = (
        get_controller()
    )

    result = (
        camera_controller.connect()
    )

    if not result:

        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to connect "
                "to camera"
            )
        )

    return {
        "success": True
    }


@router.post("/disconnect")
def disconnect():

    camera_controller = (
        get_controller()
    )

    result = (
        camera_controller.disconnect()
    )

    return {
        "success": result
    }


# =========================================================
# Status
# =========================================================

@router.get("/status")
def status():

    camera_controller = (
        get_controller()
    )

    return {
        "success": True,
        "data": (
            camera_controller
            .get_status()
        )
    }


# =========================================================
# Exposure
# =========================================================

@router.get("/exposure")
def get_exposure():

    camera_controller = (
        get_controller()
    )

    try:

        exposure = (
            camera_controller
            .get_exposure()
        )

    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    return {
        "success": True,
        "exposure_us": exposure
    }


@router.post("/exposure")
def set_exposure(
    request: ExposureRequest
):

    camera_controller = (
        get_controller()
    )

    try:

        exposure = (
            camera_controller
            .set_exposure(
                request.exposure_us
            )
        )

    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    return {
        "success": True,
        "exposure_us": exposure
    }


# =========================================================
# Gain
# =========================================================

@router.get("/gain")
def get_gain():

    camera_controller = (
        get_controller()
    )

    try:

        gain = (
            camera_controller
            .get_gain()
        )

    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    return {
        "success": True,
        "gain_db": gain
    }


@router.post("/gain")
def set_gain(
    request: GainRequest
):

    camera_controller = (
        get_controller()
    )

    try:

        gain = (
            camera_controller
            .set_gain(
                request.gain_db
            )
        )

    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    return {
        "success": True,
        "gain_db": gain
    }

# =========================================================
# Image acquisition
# =========================================================

@router.get("/frame")
def get_frame():

    camera_controller = (
        get_controller()
    )

    if not camera_controller.is_connected():

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    try:

        if (
            camera_controller
            .is_streaming()
        ):

            jpeg_data = (
                camera_controller
                .get_latest_jpeg()
            )

            if jpeg_data is None:

                raise HTTPException(
                    status_code=503,
                    detail=(
                        "Camera stream has not "
                        "produced a frame yet"
                    )
                )

        else:

            jpeg_data = (
                camera_controller
                .capture_jpeg()
            )

    except HTTPException:
        raise

    except ConnectionError:

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return Response(
        content=jpeg_data,
        media_type="image/jpeg",
        headers={
            "Cache-Control": (
                "no-store, "
                "no-cache, "
                "must-revalidate"
            )
        }
    )

# =========================================================
# Streaming
# =========================================================

@router.post("/stream/start")
def start_stream():

    camera_controller = (
        get_controller()
    )

    if not camera_controller.is_connected():

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    try:

        camera_controller.start_streaming()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "success": True,
        "streaming": True
    }

@router.post("/stream/stop")
def stop_stream():

    camera_controller = (
        get_controller()
    )

    if not camera_controller.is_connected():

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )

    try:

        camera_controller.stop_streaming()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "success": True,
        "streaming": False
    }

@router.get("/stream/status")
def stream_status():

    camera_controller = (
        get_controller()
    )

    return {
        "success": True,

        "connected": (
            camera_controller
            .is_connected()
        ),

        "streaming": (
            camera_controller
            .is_streaming()
        )
    }