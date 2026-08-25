class CameraController:

    def __init__(
        self,
        camera,
        logger
    ):

        self.camera = camera
        self.logger = logger


    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        try:

            connected = (
                self.camera.connect()
            )

            if not connected:

                self.logger.error(
                    "Camera connection failed",
                    source="CAMERA"
                )

                return False

            info = (
                self.camera.get_info()
            )

            self.logger.success(
                (
                    "Camera connected: "
                    f"{info['model']} "
                    f"({info['serial']})"
                ),
                source="CAMERA"
            )

            return True

        except Exception as e:

            self.logger.error(
                (
                    "Camera connection failed: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            return False


    def disconnect(self):

        try:

            result = (
                self.camera.disconnect()
            )

            if result:

                self.logger.info(
                    "Camera disconnected",
                    source="CAMERA"
                )

            else:

                self.logger.warning(
                    (
                        "Camera disconnected with "
                        "one or more cleanup errors"
                    ),
                    source="CAMERA"
                )

            return result

        except Exception as e:

            self.logger.error(
                (
                    "Camera disconnect failed: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            return False


    def is_connected(self):

        return (
            self.camera.is_connected()
        )


    # =========================================================
    # Status
    # =========================================================

    def get_status(self):

        return (
            self.camera.get_status()
        )


    # =========================================================
    # Exposure
    # =========================================================

    def get_exposure(self):

        try:

            return (
                self.camera.get_exposure()
            )

        except Exception as e:

            self.logger.error(
                (
                    "Unable to read camera exposure: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            raise


    def set_exposure(
        self,
        exposure_us: float
    ):

        try:

            result = (
                self.camera.set_exposure(
                    exposure_us
                )
            )

            self.logger.info(
                (
                    "Camera exposure set to "
                    f"{result:.0f} µs"
                ),
                source="CAMERA"
            )

            return result

        except Exception as e:

            self.logger.error(
                (
                    "Unable to set camera exposure: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            raise


    # =========================================================
    # Gain
    # =========================================================

    def get_gain(self):

        try:

            return (
                self.camera.get_gain()
            )

        except Exception as e:

            self.logger.error(
                (
                    "Unable to read camera gain: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            raise


    def set_gain(
        self,
        gain: float
    ):

        try:

            result = (
                self.camera.set_gain(
                    gain
                )
            )

            self.logger.info(
                (
                    "Camera gain set to "
                    f"{result:.0f}"
                ),
                source="CAMERA"
            )

            return result

        except Exception as e:

            self.logger.error(
                (
                    "Unable to set camera gain: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            raise


    # =========================================================
    # Frame rate
    # =========================================================

    def get_frame_rate(self):

        try:

            return (
                self.camera.get_frame_rate()
            )

        except Exception as e:

            self.logger.error(
                (
                    "Unable to read camera "
                    f"frame rate: {e}"
                ),
                source="CAMERA"
            )

            raise


    def set_frame_rate(
        self,
        fps: float
    ):

        try:

            result = (
                self.camera.set_frame_rate(
                    fps
                )
            )

            self.logger.info(
                (
                    "Camera frame rate set to "
                    f"{result:.2f} FPS"
                ),
                source="CAMERA"
            )

            return result

        except Exception as e:

            self.logger.error(
                (
                    "Unable to set camera "
                    f"frame rate: {e}"
                ),
                source="CAMERA"
            )

            raise

    def get_frame_count(self):

        return (
            self.camera.get_frame_count()
        )

    # =========================================================
    # Capture
    # =========================================================

    def capture_jpeg(self):

        try:

            return (
                self.camera.capture_jpeg(
                    quality=90
                )
            )

        except Exception as e:

            self.logger.error(
                (
                    "Camera capture failed: "
                    f"{e}"
                ),
                source="CAMERA"
            )

            raise


    # =========================================================
    # Streaming
    # =========================================================

    def start_streaming(self):

        try:

            if not self.camera.is_connected():

                raise ConnectionError(
                    "Camera not connected"
                )

            if self.camera.is_streaming():

                return True

            result = (
                self.camera.start_streaming()
            )

            if not result:

                raise RuntimeError(
                    (
                        "Camera failed to "
                        "start streaming"
                    )
                )

            self.logger.success(
                "Camera live acquisition started",
                source="CAMERA"
            )

            return True

        except Exception as e:

            self.logger.error(
                (
                    "Unable to start camera "
                    f"stream: {e}"
                ),
                source="CAMERA"
            )

            raise


    def stop_streaming(self):

        try:

            if not self.camera.is_streaming():

                return True

            result = (
                self.camera.stop_streaming()
            )

            if not result:

                raise RuntimeError(
                    (
                        "Camera failed to "
                        "stop streaming"
                    )
                )

            self.logger.info(
                "Camera live acquisition stopped",
                source="CAMERA"
            )

            return True

        except Exception as e:

            self.logger.error(
                (
                    "Unable to stop camera "
                    f"stream: {e}"
                ),
                source="CAMERA"
            )

            raise


    def is_streaming(self):

        return (
            self.camera.is_streaming()
        )


    def get_latest_jpeg(self):

        try:

            return (
                self.camera.get_latest_jpeg()
            )

        except Exception as e:

            self.logger.error(
                (
                    "Unable to retrieve "
                    f"camera frame: {e}"
                ),
                source="CAMERA"
            )

            raise