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
                    f"Camera connected: "
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

            self.camera.disconnect()

            self.logger.info(
                "Camera disconnected",
                source="CAMERA"
            )

            return True


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
                    f"{result:.1f} µs"
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
        gain_db: float
    ):

        try:

            result = (
                self.camera.set_gain(
                    gain_db
                )
            )

            self.logger.info(
                (
                    "Camera gain set to "
                    f"{result:.2f} dB"
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
    # Acquisition
    # =========================================================

    def capture_jpeg(self):

        try:

            return (
                self.camera.capture_jpeg()
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

            self.camera.start_streaming()

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

            self.camera.stop_streaming()

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