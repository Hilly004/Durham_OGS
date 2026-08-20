from datetime import (
    datetime,
    timezone,
)

from fastapi import (
    APIRouter,
    HTTPException,
)

from Controllers.Mount_Controller import (
    MountController,
)

from schemas.mount_setup import (
    AlignmentNudgeRequest,
    AlignmentPointRequest,
    ModelNameRequest,
    MountSiteUpdate,
)


router = APIRouter(
    prefix="/api/mount",
    tags=["Mount Setup"],
)


controller: MountController | None = None


# ============================================================
# Controller registration
# ============================================================

def set_controller(
    mount_controller: MountController
):

    global controller

    controller = mount_controller


def get_controller() -> MountController:

    if controller is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "Mount controller is "
                "not initialised"
            ),
        )


    return controller


# ============================================================
# Mount information
# ============================================================

@router.get("/info")
def mount_info():

    try:

        return {
            "success": True,
            "data":
                get_controller()
                .get_mount_information(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Site setup
# ============================================================

@router.get("/setup/site")
def get_site():

    try:

        return {
            "success": True,
            "data":
                get_controller()
                .get_site_configuration(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.put("/setup/site")
def set_site(
    request: MountSiteUpdate
):

    try:

        data = (
            get_controller()
            .set_site_configuration(
                request.latitude,
                request.longitude,
                request.elevation_m,
            )
        )


        return {
            "success": True,
            "data": data,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Mount clock
# ============================================================

@router.get("/setup/time")
def mount_time():

    try:

        mount_utc = (
            get_controller()
            .get_mount_utc_datetime()
        )


        return {
            "success": True,

            "data": {
                "mount_utc":
                    mount_utc,

                "computer_utc":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
            },
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/setup/time/sync"
)
def sync_mount_time():

    try:

        now = datetime.now(
            timezone.utc
        )


        get_controller().set_mount_utc_datetime(
            now.strftime(
                "%Y-%m-%d"
            ),
            now.strftime(
                "%H:%M:%S"
            ),
        )


        return {
            "success": True,
            "message":
                (
                    "Mount UTC clock "
                    "synchronised"
                ),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Home
# ============================================================

@router.post("/setup/home")
def seek_home():

    try:

        return {
            "success": True,

            "data":
                get_controller()
                .seek_home_and_store(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/setup/home-align"
)
def seek_home_align():

    try:

        return {
            "success": True,

            "data":
                get_controller()
                .seek_home_and_align(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.get(
    "/setup/home/status"
)
def home_status():

    try:

        return {
            "success": True,

            "data":
                get_controller()
                .get_home_status(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Alignment model
# ============================================================

@router.get("/alignment")
def alignment():

    try:

        return {
            "success": True,

            "data":
                get_controller()
                .get_alignment(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Alignment target slew
# ============================================================

@router.post(
    "/alignment/slew"
)
def slew_alignment_target(
    request: AlignmentPointRequest
):

    try:

        mount = (
            get_controller()
        )


        if not mount.is_connected():

            raise RuntimeError(
                "Mount not connected"
            )


        success = (
            mount.slew_to_ra_dec(
                request.ra_hours,
                request.dec_degrees,
            )
        )


        if not success:

            raise RuntimeError(
                (
                    "Mount rejected alignment "
                    "target slew"
                )
            )


        mount.logger.info(
            (
                "Slewing to alignment target: "
                f"{request.name}"
            ),
            source="MOUNT",
        )


        return {
            "success": True,

            "data": {
                "name":
                    request.name,

                "ra_hours":
                    request.ra_hours,

                "dec_degrees":
                    request.dec_degrees,
            },
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Alignment nudge
# ============================================================

@router.post(
    "/alignment/nudge"
)
def nudge_alignment_target(
    request: AlignmentNudgeRequest
):

    try:

        result = (
            get_controller()
            .nudge(
                request.direction,
                request.step_arcsec,
            )
        )


        return {
            "success": True,

            "data": {
                "direction":
                    request.direction,

                "step_arcsec":
                    request.step_arcsec,

                "result":
                    result,
            },
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Add alignment point
# ============================================================

@router.post(
    "/alignment/add-point"
)
def add_alignment_point(
    request: AlignmentPointRequest
):

    try:

        data = (
            get_controller()
            .add_alignment_point(
                request.ra_hours,
                request.dec_degrees,
                request.name,
            )
        )


        return {
            "success": True,
            "data": data,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Delete individual point
# ============================================================

@router.delete(
    "/alignment/points/{index}"
)
def delete_alignment_point(
    index: int
):

    try:

        success = (
            get_controller()
            .delete_alignment_point(
                index
            )
        )


        if not success:

            raise RuntimeError(
                (
                    "Mount failed to delete "
                    f"alignment point {index}"
                )
            )


        return {
            "success": True,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Delete entire active model
# ============================================================

@router.delete("/alignment")
def delete_alignment():

    try:

        get_controller().delete_alignment_model()


        return {
            "success": True,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


# ============================================================
# Saved models
# ============================================================

@router.get("/models")
def models():

    try:

        return {
            "success": True,

            "data":
                get_controller()
                .get_saved_models(),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/models/save"
)
def save_model(
    request: ModelNameRequest
):

    try:

        success = (
            get_controller()
            .save_alignment_model(
                request.name
            )
        )


        if not success:

            raise RuntimeError(
                "Mount failed to save model"
            )


        return {
            "success": True,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/models/load"
)
def load_model(
    request: ModelNameRequest
):

    try:

        success = (
            get_controller()
            .load_alignment_model(
                request.name
            )
        )


        if not success:

            raise RuntimeError(
                "Mount failed to load model"
            )


        return {
            "success": True,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.delete(
    "/models/{name}"
)
def delete_model(
    name: str
):

    try:

        success = (
            get_controller()
            .delete_saved_model(
                name
            )
        )


        if not success:

            raise RuntimeError(
                "Mount failed to delete model"
            )


        return {
            "success": True,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc