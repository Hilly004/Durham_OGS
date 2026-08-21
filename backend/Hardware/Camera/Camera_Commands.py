from io import BytesIO
from threading import Lock

import numpy as np
from PIL import Image

from vmbpy import (
    VmbSystem,
    PixelFormat,
    FrameStatus,
)

class MakoCamera:

    def __init__(
        self,
        camera_id: str | None = None
    ):
        self.camera_id = camera_id

        self._vmb = None
        self._camera = None

        self._connected = False

        self._lock = Lock()

        self._streaming = False

        self._latest_jpeg = None

        self._frame_lock = Lock()

        self._frame_count = 0

    # =========================================================
    # Connection
    # =========================================================

    def connect(self):

        with self._lock:

            if self._connected:
                return True

            if not self.camera_id:
                raise RuntimeError(
                    "No camera ID configured. "
                    "Set the camera ID in Settings first."
                )

            try:

                print(
                    "[CAMERA] Connecting using ID:",
                    repr(self.camera_id),
                    "type:",
                    type(self.camera_id)
                )

                self._vmb = VmbSystem.get_instance()

                self._vmb.__enter__()

                self._camera = (
                    self._vmb.get_camera_by_id(
                        self.camera_id
                    )
                )

                self._camera.__enter__()

                self._connected = True

                print(
                    "[CAMERA] Connected:",
                    self._camera.get_model(),
                    self._camera.get_serial()
                )

                return True

            except Exception as exc:

                print(
                    "[CAMERA] Connection failed:",
                    type(exc).__name__,
                    str(exc)
                )

                self._cleanup()

                raise

    def disconnect(self) -> bool:
        """
        Disconnect from the camera and VmbSystem.
        """

        success = True

        try:
            if self._camera is not None:
                self._camera.__exit__(
                    None,
                    None,
                    None,
                )
        except Exception as exc:
            print(
                f"[CAMERA] Camera close failed: {exc}"
            )
            success = False

        finally:
            self._camera = None

        try:
            if self._vmb is not None:
                self._vmb.__exit__(
                    None,
                    None,
                    None,
                )
        except Exception as exc:
            print(
                f"[CAMERA] VmbSystem close failed: {exc}"
            )
            success = False

        finally:
            self._vmb = None

        return success

    def _cleanup(self):

        if self._camera is not None:

            try:
                self._camera.__exit__(
                    None,
                    None,
                    None
                )
            except Exception:
                pass

            self._camera = None


        if self._vmb is not None:

            try:
                self._vmb.__exit__(
                    None,
                    None,
                    None
                )
            except Exception:
                pass

            self._vmb = None


        self._connected = False


    def is_connected(self):

        return self._connected
    
    def set_camera_id(
        self,
        camera_id: str
    ):
        if not isinstance(camera_id, str):
            raise TypeError(
                "Camera ID must be a string"
            )

        camera_id = camera_id.strip()

        if not camera_id:
            raise ValueError(
                "Camera ID cannot be empty"
            )

        if self._connected:
            raise RuntimeError(
                "Disconnect camera before "
                "changing camera ID"
            )

        self.camera_id = camera_id

        print(
            "[CAMERA] Camera ID configured:",
            repr(self.camera_id)
        )

        return self.camera_id

    def _require_connection(self):

        if (
            not self._connected
            or self._camera is None
        ):
            raise ConnectionError(
                "Camera not connected"
            )


    # =========================================================
    # Camera information
    # =========================================================

    def get_info(self):

        self._require_connection()

        return {
            "id": self._camera.get_id(),
            "name": self._camera.get_name(),
            "model": self._camera.get_model(),
            "serial": self._camera.get_serial(),
        }


    # =========================================================
    # Exposure
    # =========================================================

    def get_exposure(self):

        self._require_connection()

        exposure = (
            self._camera
            .get_feature_by_name(
                "ExposureTime"
            )
        )

        return exposure.get()


    def set_exposure(
        self,
        exposure_us: float
    ):

        self._require_connection()

        exposure = (
            self._camera
            .get_feature_by_name(
                "ExposureTime"
            )
        )

        minimum, maximum = (
            exposure.get_range()
        )

        if not (
            minimum
            <= exposure_us
            <= maximum
        ):
            raise ValueError(
                (
                    f"Exposure must be between "
                    f"{minimum} and {maximum} µs"
                )
            )

        exposure.set(
            float(exposure_us)
        )

        return exposure.get()


    # =========================================================
    # Gain
    # =========================================================

    def get_gain(self):

        self._require_connection()

        gain = (
            self._camera
            .get_feature_by_name(
                "Gain"
            )
        )

        return gain.get()


    def set_gain(
        self,
        gain_db: float
    ):

        self._require_connection()

        gain = (
            self._camera
            .get_feature_by_name(
                "Gain"
            )
        )

        minimum, maximum = (
            gain.get_range()
        )

        if not (
            minimum
            <= gain_db
            <= maximum
        ):
            raise ValueError(
                (
                    f"Gain must be between "
                    f"{minimum} and {maximum} dB"
                )
            )

        gain.set(
            float(gain_db)
        )

        return gain.get()


    # =========================================================
    # Frame acquisition
    # =========================================================

    def get_frame(self):

        self._require_connection()

        frame = self._camera.get_frame(
            timeout_ms=5000
        )

        return frame

    def capture_jpeg(
        self,
        quality: int = 90
    ):

        self._require_connection()

        if self._streaming:

            raise RuntimeError(
                "Cannot perform synchronous capture "
                "while camera is streaming"
            )

        frame = self._camera.get_frame(
            timeout_ms=5000
        )

        return self._frame_to_jpeg(
            frame,
            quality=quality
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
                "frame_count": 0,
            }


        try:

            info = self.get_info()

            exposure = (
                self.get_exposure()
            )

            gain = (
                self.get_gain()
            )

            return {
                "connected": True,

                "streaming": (
                    self._streaming
                ),

                "camera": info,

                "exposure": exposure,

                "gain": gain,

                "frame_count": (
                    self.get_frame_count()
                ),
            }

        except Exception:

            return {
                "connected": False,
                "streaming": False,
                "camera": None,
                "exposure": None,
                "gain": None,
                "frame_count": 0,
            }

        
    def _frame_to_jpeg(
        self,
        frame,
        quality: int = 90
    ):

        frame.convert_pixel_format(
            PixelFormat.Mono8
        )

        image_array = (
            frame.as_numpy_ndarray()
        )

        image_array = np.squeeze(
            image_array
        )

        image_array = image_array.astype(
            np.uint8,
            copy=False
        )

        image = Image.fromarray(
            image_array
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=quality
        )

        return buffer.getvalue()
    
    def _frame_handler(
        self,
        camera,
        stream,
        frame
    ):

        try:

            if (
                frame.get_status()
                == FrameStatus.Complete
            ):

                jpeg_data = (
                    self._frame_to_jpeg(
                        frame
                    )
                )

                with self._frame_lock:

                    self._latest_jpeg = (
                        jpeg_data
                    )

                    self._frame_count += 1

        except Exception as e:

            print(
                f"Camera frame processing error: {e}"
            )

        finally:

            try:
                camera.queue_frame(frame)

            except Exception as e:
                print(
                    f"Unable to requeue camera frame: {e}"
                )


    def start_streaming(self):

        self._require_connection()

        if self._streaming:
            return True

        with self._frame_lock:

            self._latest_jpeg = None
            self._frame_count = 0

        self._camera.start_streaming(
            handler=self._frame_handler,
            buffer_count=5
        )

        self._streaming = True

        return True
    
    def stop_streaming(self):

        if not self._connected:
            return True

        if not self._streaming:
            return True

        self._camera.stop_streaming()

        self._streaming = False

        return True
    
    def is_streaming(self):

        return self._streaming
    
    def get_latest_jpeg(self):

        self._require_connection()

        if not self._streaming:

            raise RuntimeError(
                "Camera is not streaming"
            )

        with self._frame_lock:

            if self._latest_jpeg is None:
                return None

            return self._latest_jpeg
        
    def get_frame_count(self):

        with self._frame_lock:
            return self._frame_count