from io import BytesIO
from threading import Lock, Thread

import time

import numpy as np
from PIL import Image

import pyzwoasi
from pyzwoasi import ZWOCamera as PyZWOCamera
from pyzwoasi.pyzwoasi import ASIImageType


class ZWOCamera:

    def __init__(
        self,
        camera_id: str | int | None = None
    ):

        self.camera_id = (
            str(camera_id)
            if camera_id is not None
            else "0"
        )

        self._camera = None

        self._connected = False
        self._streaming = False

        self._lock = Lock()
        self._frame_lock = Lock()

        self._latest_jpeg = None
        self._frame_count = 0

        self._stream_thread = None
        self._stop_stream = False

        self._last_frame_time = None
        self._measured_fps = None


    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        with self._lock:

            if self._connected:
                return True


            try:

                camera_index = int(
                    self.camera_id
                )

            except (
                TypeError,
                ValueError,
            ) as exc:

                raise ValueError(
                    (
                        "ZWO camera ID must be "
                        "a numeric camera index, "
                        "for example 0."
                    )
                ) from exc


            number_of_cameras = (
                pyzwoasi
                .getNumOfConnectedCameras()
            )


            if number_of_cameras <= 0:

                raise RuntimeError(
                    "No ZWO cameras detected"
                )


            if (
                camera_index < 0
                or
                camera_index >= number_of_cameras
            ):

                raise RuntimeError(
                    (
                        "Requested ZWO camera "
                        f"index {camera_index}, "
                        "but only "
                        f"{number_of_cameras} "
                        "camera(s) were detected."
                    )
                )


            try:

                print(
                    (
                        "[ZWO CAMERA] "
                        "Connecting using index:"
                    ),
                    camera_index,
                )


                self._camera = (
                    PyZWOCamera(
                        camera_index
                    )
                )


                #
                # Select an appropriate image format.
                #
                # pyzwoasi exposes whether the sensor is
                # colour via _isColorCam.
                #
                if getattr(
                    self._camera,
                    "_isColorCam",
                    False
                ):

                    self._camera.imageType = (
                        ASIImageType
                        .ASI_IMG_RGB24
                    )

                else:

                    self._camera.imageType = (
                        ASIImageType
                        .ASI_IMG_RAW8
                    )


                self._connected = True
                self._streaming = False

                self._stop_stream = False

                self._last_frame_time = None
                self._measured_fps = None


                with self._frame_lock:

                    self._latest_jpeg = None
                    self._frame_count = 0


                camera_info = (
                    self.get_info()
                )


                print(
                    (
                        "[ZWO CAMERA] Connected: "
                        f"{camera_info['model']}"
                    )
                )


                return True


            except Exception as exc:

                print(
                    (
                        "[ZWO CAMERA] "
                        "Connection failed:"
                    ),
                    type(exc).__name__,
                    str(exc),
                )

                self._cleanup()

                raise


    def disconnect(self) -> bool:

        success = True


        if self._streaming:

            try:

                self.stop_streaming()

            except Exception as exc:

                print(
                    (
                        "[ZWO CAMERA] "
                        "Stream stop failed: "
                        f"{exc}"
                    )
                )

                success = False


        if self._camera is not None:

            try:

                self._camera.close()

            except Exception as exc:

                print(
                    (
                        "[ZWO CAMERA] "
                        "Camera close failed: "
                        f"{exc}"
                    )
                )

                success = False


        self._camera = None

        self._connected = False
        self._streaming = False

        self._stop_stream = False

        self._stream_thread = None

        self._last_frame_time = None
        self._measured_fps = None


        with self._frame_lock:

            self._latest_jpeg = None
            self._frame_count = 0


        return success


    def _cleanup(self):

        self._stop_stream = True


        if self._camera is not None:

            try:

                self._camera.stopVideoCapture()

            except Exception:
                pass


            try:

                self._camera.close()

            except Exception:
                pass


        self._camera = None

        self._connected = False
        self._streaming = False

        self._stream_thread = None

        self._last_frame_time = None
        self._measured_fps = None


        with self._frame_lock:

            self._latest_jpeg = None
            self._frame_count = 0


    def is_connected(self):

        return self._connected


    def set_camera_id(
        self,
        camera_id: str | int
    ):

        if self._connected:

            raise RuntimeError(
                (
                    "Disconnect camera before "
                    "changing camera ID"
                )
            )


        try:

            camera_index = int(
                camera_id
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                (
                    "ZWO camera ID must be "
                    "a numeric camera index"
                )
            ) from exc


        if camera_index < 0:

            raise ValueError(
                (
                    "ZWO camera index "
                    "cannot be negative"
                )
            )


        self.camera_id = str(
            camera_index
        )


        print(
            (
                "[ZWO CAMERA] "
                "Camera ID configured:"
            ),
            self.camera_id,
        )


        return self.camera_id


    def _require_connection(self):

        if (
            not self._connected
            or
            self._camera is None
        ):

            raise ConnectionError(
                "Camera not connected"
            )


    # =========================================================
    # Camera information
    # =========================================================

    def get_info(self):

        self._require_connection()


        model = getattr(
            self._camera,
            "_name",
            "ZWO ASI Camera",
        )


        camera_index = int(
            self.camera_id
        )


        return {
            "id": self.camera_id,

            "name": model,

            "model": model,

            #
            # pyzwoasi's high-level class does not
            # currently expose a convenient serial
            # property.
            #
            # Using the camera index as a stable fallback
            # keeps your existing status interface intact.
            #
            "serial": (
                f"ZWO-{camera_index}"
            ),
        }


    # =========================================================
    # Exposure
    # =========================================================

    def get_exposure(self):

        self._require_connection()


        exposure = (
            self._camera.exposure
        )


        if exposure is None:

            raise RuntimeError(
                (
                    "Exposure control is not "
                    "available on this ZWO camera"
                )
            )


        return float(
            exposure
        )


    def set_exposure(
        self,
        exposure_us: float
    ):

        self._require_connection()


        requested = int(
            exposure_us
        )


        minimum, maximum = (
            self._camera
            .exposureLimits
        )


        if (
            minimum is None
            or
            maximum is None
        ):

            raise RuntimeError(
                (
                    "Exposure control is not "
                    "available on this ZWO camera"
                )
            )


        if not (
            minimum
            <= requested
            <= maximum
        ):

            raise ValueError(
                (
                    "Exposure must be between "
                    f"{minimum} and "
                    f"{maximum} µs"
                )
            )


        self._camera.exposure = (
            requested
        )


        return self.get_exposure()


    # =========================================================
    # Gain
    # =========================================================

    def get_gain(self):

        self._require_connection()

        gain = (
            self._camera.gain
        )

        if gain is None:

            raise RuntimeError(
                (
                    "Gain control is not "
                    "available on this ZWO camera"
                )
            )

        return float(
            gain
        )


    def set_gain(
        self,
        gain: float
    ):

        self._require_connection()

        requested = int(
            gain
        )

        minimum, maximum = (
            self._camera.gainLimits
        )

        if (
            minimum is None
            or
            maximum is None
        ):

            raise RuntimeError(
                (
                    "Gain control is not "
                    "available on this ZWO camera"
                )
            )

        if not (
            minimum
            <= requested
            <= maximum
        ):

            raise ValueError(
                (
                    "Gain must be between "
                    f"{minimum} and "
                    f"{maximum}"
                )
            )

        self._camera.gain = (
            requested
        )

        return self.get_gain()
    # =========================================================
    # Frame rate
    # =========================================================

    def get_frame_rate(self):

        self._require_connection()


        #
        # There is no direct FPS control exposed in
        # the same way as your Allied Vision camera.
        #
        # Return the rate measured by our streaming
        # thread instead.
        #
        return self._measured_fps


    def set_frame_rate(
        self,
        fps: float
    ):

        self._require_connection()


        if fps <= 0:

            raise ValueError(
                (
                    "Frame rate must be "
                    "greater than zero"
                )
            )


        raise RuntimeError(
            (
                "ZWO frame rate cannot be set "
                "directly. It depends on exposure, "
                "ROI, binning and USB bandwidth."
            )
        )


    # =========================================================
    # Still capture
    # =========================================================

    def get_frame(self):

        self._require_connection()


        if self._streaming:

            raise RuntimeError(
                (
                    "Cannot perform synchronous "
                    "capture while live view "
                    "is running"
                )
            )


        frame = (
            self._camera.shot()
        )


        return frame


    def capture_jpeg(
        self,
        quality: int = 90
    ):

        frame = self.get_frame()


        return self._array_to_jpeg(
            frame,
            quality=quality,
        )


    # =========================================================
    # Status
    # =========================================================

    def get_status(self):

        if not self._connected:

            return {
                "connected": False,
                "streaming": False,
                "camera": None,
                "exposure": None,
                "gain": None,
                "gain_unit": "ASI",
                "frame_rate": None,
                "frame_count": 0,
            }


        try:

            return {
                "connected": True,

                "streaming": (
                    self._streaming
                ),

                "camera": (
                    self.get_info()
                ),

                "exposure": (
                    self.get_exposure()
                ),

                "gain": (
                    self.get_gain()
                ),

                "gain_unit": "ASI",

                "frame_rate": (
                    self.get_frame_rate()
                ),

                "frame_count": (
                    self.get_frame_count()
                ),
            }


        except Exception as exc:

            print(
                (
                    "[ZWO CAMERA] "
                    "Unable to read full status: "
                    f"{exc}"
                )
            )


            return {
                "connected": (
                    self._connected
                ),

                "streaming": (
                    self._streaming
                ),

                "camera": None,

                "exposure": None,

                "gain": None,

                "gain_unit": "ASI",

                "frame_rate": (
                    self._measured_fps
                ),

                "frame_count": (
                    self.get_frame_count()
                ),
            }


    # =========================================================
    # JPEG conversion
    # =========================================================

    def _array_to_jpeg(
        self,
        image_array,
        quality: int = 90
    ):

        quality = max(
            1,
            min(
                int(quality),
                95,
            )
        )


        image_array = np.asarray(
            image_array
        )


        image_array = np.squeeze(
            image_array
        )


        if (
            image_array.dtype
            == np.uint16
        ):

            maximum = (
                int(
                    image_array.max()
                )
                if image_array.size
                else 0
            )


            if maximum > 0:

                image_array = (
                    (
                        image_array.astype(
                            np.float32
                        )
                        /
                        maximum
                    )
                    *
                    255.0
                ).astype(
                    np.uint8
                )

            else:

                image_array = (
                    image_array.astype(
                        np.uint8
                    )
                )


        elif (
            image_array.dtype
            != np.uint8
        ):

            image_array = (
                np.clip(
                    image_array,
                    0,
                    255,
                )
                .astype(
                    np.uint8
                )
            )


        #
        # ZWO RGB24 data is BGR.
        #
        if (
            image_array.ndim == 3
            and
            image_array.shape[2] == 3
        ):

            image_array = (
                image_array[
                    :,
                    :,
                    ::-1
                ]
            )


            image = Image.fromarray(
                image_array,
                mode="RGB",
            )


        elif image_array.ndim == 2:

            image = Image.fromarray(
                image_array,
                mode="L",
            )


        else:

            raise RuntimeError(
                (
                    "Unsupported ZWO frame "
                    f"shape: {image_array.shape}"
                )
            )


        buffer = BytesIO()


        image.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=False,
        )


        return buffer.getvalue()


    # =========================================================
    # Video frame conversion
    # =========================================================

    def _get_video_frame(self):

        self._require_connection()


        width, height, _, image_type = (
            self._camera.roi
        )


        buffer_size = (
            self._camera.bufferSize
        )


        #
        # pyzwoasi getVideoData timeout is in milliseconds.
        #
        exposure_us = (
            self.get_exposure()
        )


        timeout_ms = int(
            (
                2
                *
                exposure_us
                /
                1000
            )
            +
            500
        )


        timeout_ms = max(
            timeout_ms,
            1000,
        )


        raw_frame = (
            pyzwoasi.getVideoData(
                int(
                    self.camera_id
                ),
                buffer_size,
                timeout_ms,
            )
        )


        if (
            image_type
            ==
            ASIImageType.ASI_IMG_RAW16
        ):

            frame = np.frombuffer(
                raw_frame,
                dtype=np.uint16,
            )

            frame = frame.reshape(
                height,
                width,
            )


        elif (
            image_type
            ==
            ASIImageType.ASI_IMG_RGB24
        ):

            frame = np.frombuffer(
                raw_frame,
                dtype=np.uint8,
            )

            frame = frame.reshape(
                height,
                width,
                3,
            )


        else:

            frame = np.frombuffer(
                raw_frame,
                dtype=np.uint8,
            )

            frame = frame.reshape(
                height,
                width,
            )


        return frame


    # =========================================================
    # Streaming
    # =========================================================

    def start_streaming(self):

        self._require_connection()

        if self._streaming:
            return True

        with self._frame_lock:
            self._latest_jpeg = None
            self._frame_count = 0

        self._stop_stream = False
        self._last_frame_time = None
        self._measured_fps = None

        self._camera.startVideoCapture()

        self._streaming = True

        self._stream_thread = Thread(
            target=self._stream_loop,
            name="ZWO-Camera-Stream",
            daemon=True,
        )

        self._stream_thread.start()

        return True


    def _stream_loop(self):

        print(
            "[ZWO CAMERA] Stream thread started"
        )

        try:

            while (
                self._streaming
                and
                not self._stop_stream
                and
                self._connected
            ):

                try:

                    frame = (
                        self._get_video_frame()
                    )

                    jpeg_data = (
                        self._array_to_jpeg(
                            frame,
                            quality=75,
                        )
                    )

                    current_time = (
                        time.monotonic()
                    )

                    if (
                        self._last_frame_time
                        is not None
                    ):

                        elapsed = (
                            current_time
                            -
                            self._last_frame_time
                        )

                        if elapsed > 0:

                            self._measured_fps = (
                                1.0 / elapsed
                            )

                    self._last_frame_time = (
                        current_time
                    )

                    with self._frame_lock:

                        self._latest_jpeg = (
                            jpeg_data
                        )

                        self._frame_count += 1

                except Exception as exc:

                    if self._streaming:

                        print(
                            (
                                "[ZWO CAMERA] "
                                "Video frame error: "
                                f"{exc}"
                            )
                        )

                    time.sleep(
                        0.02
                    )

        finally:

            print(
                "[ZWO CAMERA] Stream thread stopped"
            )


    def stop_streaming(self):

        if not self._connected:

            self._streaming = False
            self._stop_stream = True

            return True


        if not self._streaming:

            return True


        self._stop_stream = True
        self._streaming = False


        try:

            self._camera.stopVideoCapture()

        except Exception as exc:

            print(
                (
                    "[ZWO CAMERA] "
                    "Unable to stop video "
                    f"capture: {exc}"
                )
            )


        if (
            self._stream_thread is not None
            and
            self._stream_thread.is_alive()
        ):

            self._stream_thread.join(
                timeout=2.0
            )


        self._stream_thread = None

        self._last_frame_time = None
        self._measured_fps = None


        with self._frame_lock:

            self._latest_jpeg = None


        return True


    def is_streaming(self):

        return self._streaming


    def get_latest_jpeg(self):

        self._require_connection()


        if not self._streaming:

            return None


        with self._frame_lock:

            return self._latest_jpeg


    def get_frame_count(self):

        with self._frame_lock:

            return self._frame_count