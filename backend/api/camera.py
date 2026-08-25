import asyncio
import time

from fastapi import (
    APIRouter,
    HTTPException,
    Response
)

from fastapi.responses import (
    StreamingResponse
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
    gain: float


class FrameRateRequest(BaseModel):
    fps: float


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
        "gain": gain
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
                request.gain
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
        "gain": gain
    }
# =========================================================
# Frame rate
# =========================================================

@router.get("/frame-rate")
def get_frame_rate():

    camera_controller = (
        get_controller()
    )


    try:

        fps = (
            camera_controller
            .get_frame_rate()
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
        "fps": fps
    }


@router.post("/frame-rate")
def set_frame_rate(
    request: FrameRateRequest
):

    camera_controller = (
        get_controller()
    )


    try:

        fps = (
            camera_controller
            .set_frame_rate(
                request.fps
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
        "fps": fps
    }


# =========================================================
# Single image acquisition
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

        #
        # When streaming, return the most recent
        # live-view frame.
        #
        if camera_controller.is_streaming():

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


        #
        # When not streaming, perform a true
        # synchronous high-quality capture.
        #
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
            ),

            "Pragma": "no-cache",
        }
    )


# =========================================================
# Acquisition control
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

        result = (
            camera_controller
            .start_streaming()
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
        "success": result,
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

        result = (
            camera_controller
            .stop_streaming()
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    return {
        "success": result,
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


# =========================================================
# MJPEG live video
# =========================================================

@router.get("/stream")
async def stream_camera():

    camera_controller = (
        get_controller()
    )


    if not camera_controller.is_connected():

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )


    if not camera_controller.is_streaming():

        raise HTTPException(
            status_code=409,
            detail=(
                "Camera stream is not running"
            )
        )


    async def generate():

        try:

            while (
                camera_controller
                .is_connected()
                and
                camera_controller
                .is_streaming()
            ):

                frame = (
                    camera_controller
                    .get_latest_jpeg()
                )


                if frame is not None:

                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n"
                        b"Content-Length: "
                        + str(
                            len(frame)
                        ).encode()
                        + b"\r\n\r\n"
                        + frame
                        + b"\r\n"
                    )


                #
                # About 20 possible sends per second.
                # The actual rate is limited by camera
                # acquisition and JPEG generation.
                #
                await asyncio.sleep(
                    0.05
                )


        except asyncio.CancelledError:

            #
            # Browser closed the MJPEG connection.
            #
            return


        except Exception:

            #
            # Do not leave an MJPEG response generating
            # forever after the camera is disconnected
            # or acquisition stops.
            #
            return


    return StreamingResponse(
        generate(),

        media_type=(
            "multipart/x-mixed-replace;"
            " boundary=frame"
        ),

        headers={
            "Cache-Control": (
                "no-store, "
                "no-cache, "
                "must-revalidate"
            ),

            "Pragma": "no-cache",
        }
    )

@router.get("/live")
def camera_live():

    camera_controller = (
        get_controller()
    )

    if (
        not camera_controller
        .is_connected()
    ):

        raise HTTPException(
            status_code=503,
            detail="Camera not connected"
        )


    if (
        not camera_controller
        .is_streaming()
    ):

        raise HTTPException(
            status_code=409,
            detail="Camera stream is not running"
        )


    def generate():

        last_frame_count = -1

        while (
            camera_controller
            .is_connected()
            and
            camera_controller
            .is_streaming()
        ):

            try:

                frame_count = (
                    camera_controller
                    .get_frame_count()
                )


                #
                # Do not resend the same frame.
                #
                if (
                    frame_count
                    ==
                    last_frame_count
                ):

                    time.sleep(
                        0.01
                    )

                    continue


                frame = (
                    camera_controller
                    .get_latest_jpeg()
                )


                if frame is None:

                    time.sleep(
                        0.01
                    )

                    continue


                last_frame_count = (
                    frame_count
                )


                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n"
                    b"Cache-Control: no-cache\r\n"
                    b"\r\n"
                    +
                    frame
                    +
                    b"\r\n"
                )


            except Exception:

                break


    return StreamingResponse(
        generate(),
        media_type=(
            "multipart/x-mixed-replace;"
            " boundary=frame"
        ),
        headers={
            "Cache-Control":
                "no-store, no-cache, must-revalidate, max-age=0",

            "Pragma":
                "no-cache",

            "Expires":
                "0",
        },
    )