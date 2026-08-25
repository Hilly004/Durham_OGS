from Hardware.Camera.Mako_Camera import MakoCamera
from Hardware.Camera.ZWO_Camera import ZWOCamera


class CameraManager:

    VALID_CAMERA_TYPES = {
        "allied",
        "zwo",
    }


    def __init__(
        self,
        camera_type: str = "allied",
        camera_id: str | int | None = None,
    ):

        self.camera_type = (
            camera_type
            .strip()
            .lower()
        )

        self.camera_id = camera_id

        self._camera = None

        self._create_camera()


    # =========================================================
    # Internal camera creation
    # =========================================================

    def _create_camera(self):

        if (
            self.camera_type
            not in self.VALID_CAMERA_TYPES
        ):

            raise ValueError(
                (
                    "Unsupported camera type: "
                    f"{self.camera_type}"
                )
            )


        if self.camera_type == "allied":

            self._camera = MakoCamera(
                camera_id=self.camera_id
            )


        elif self.camera_type == "zwo":

            self._camera = ZWOCamera(
                camera_id=self.camera_id
            )


        print(
            (
                "[CAMERA MANAGER] "
                f"Selected camera type: "
                f"{self.camera_type}, "
                f"ID: {self.camera_id}"
            )
        )


    # =========================================================
    # Camera selection
    # =========================================================

    def set_camera(
        self,
        camera_type: str,
        camera_id: str | int | None = None,
    ):

        camera_type = (
            camera_type
            .strip()
            .lower()
        )


        if (
            camera_type
            not in self.VALID_CAMERA_TYPES
        ):

            raise ValueError(
                (
                    "Unsupported camera type: "
                    f"{camera_type}"
                )
            )


        if (
            self._camera is not None
            and
            self._camera.is_connected()
        ):

            raise RuntimeError(
                (
                    "Disconnect the current "
                    "camera before changing "
                    "camera type"
                )
            )


        self.camera_type = camera_type
        self.camera_id = camera_id

        self._create_camera()


        return {
            "camera_type": self.camera_type,
            "camera_id": self.camera_id,
        }


    def set_camera_type(
        self,
        camera_type: str
    ):

        return self.set_camera(
            camera_type,
            self.camera_id,
        )


    def set_camera_id(
        self,
        camera_id: str | int | None
    ):

        if (
            self._camera is not None
            and
            self._camera.is_connected()
        ):

            raise RuntimeError(
                (
                    "Disconnect the current "
                    "camera before changing "
                    "camera ID"
                )
            )


        self.camera_id = camera_id


        if self._camera is not None:

            self._camera.set_camera_id(
                camera_id
            )


        return self.camera_id


    def get_camera_type(self):

        return self.camera_type


    def get_camera_id(self):

        return self.camera_id


    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        self._require_camera()

        return self._camera.connect()


    def disconnect(self):

        self._require_camera()

        return self._camera.disconnect()


    def is_connected(self):

        if self._camera is None:
            return False

        return self._camera.is_connected()


    # =========================================================
    # Information
    # =========================================================

    def get_info(self):

        self._require_camera()


        info = (
            self._camera.get_info()
        )


        return {
            **info,
            "camera_type": self.camera_type,
        }


    def get_status(self):

        self._require_camera()


        status = (
            self._camera.get_status()
        )


        return {
            **status,
            "camera_type": self.camera_type,
            "camera_id": self.camera_id,
        }


    # =========================================================
    # Exposure
    # =========================================================

    def get_exposure(self):

        self._require_camera()

        return (
            self._camera.get_exposure()
        )


    def set_exposure(
        self,
        exposure_us: float
    ):

        self._require_camera()

        return (
            self._camera.set_exposure(
                exposure_us
            )
        )


    # =========================================================
    # Gain
    # =========================================================

    def get_gain(self):

        self._require_camera()

        return (
            self._camera.get_gain()
        )


    def set_gain(
        self,
        gain: float
    ):

        self._require_camera()

        return (
            self._camera.set_gain(
                gain
            )
        )


    # =========================================================
    # Frame rate
    # =========================================================

    def get_frame_rate(self):

        self._require_camera()

        return (
            self._camera
            .get_frame_rate()
        )


    def set_frame_rate(
        self,
        fps: float
    ):

        self._require_camera()

        return (
            self._camera
            .set_frame_rate(
                fps
            )
        )


    # =========================================================
    # Still capture
    # =========================================================

    def get_frame(self):

        self._require_camera()

        return (
            self._camera.get_frame()
        )


    def capture_jpeg(
        self,
        quality: int = 90
    ):

        self._require_camera()

        return (
            self._camera
            .capture_jpeg(
                quality=quality
            )
        )


    # =========================================================
    # Streaming
    # =========================================================

    def start_streaming(self):

        self._require_camera()

        return (
            self._camera
            .start_streaming()
        )


    def stop_streaming(self):

        self._require_camera()

        return (
            self._camera
            .stop_streaming()
        )


    def is_streaming(self):

        if self._camera is None:
            return False

        return (
            self._camera
            .is_streaming()
        )


    def get_latest_jpeg(self):

        self._require_camera()

        return (
            self._camera
            .get_latest_jpeg()
        )


    def get_frame_count(self):

        self._require_camera()

        return (
            self._camera
            .get_frame_count()
        )


    # =========================================================
    # Helpers
    # =========================================================

    def _require_camera(self):

        if self._camera is None:

            raise RuntimeError(
                "No camera configured"
            )