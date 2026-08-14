from Controllers.safety_manager import SafetyManager
from Utilities.Observatory_Logger import ObservatoryLogger
import time
import threading

class ObservatoryController:

    def __init__(self, dome, mount, weather):
        self.dome = dome
        self.mount = mount
        self.weather = weather

        self.safety = SafetyManager(
            mount,
            dome,
            weather
        )

        self.running = False
        self.monitor_thread = None
        self.logger = ObservatoryLogger()

        self.shutdown_in_progress = False
        self.unsafe_shutdown_triggered = False
        self.safety_monitor_armed = False

    def start(self):
        if self.running:
            return

        self.running = True

        self.monitor_thread = threading.Thread(
            target=self._monitor,
            daemon=True
        )

        self.monitor_thread.start()


    def _monitor(self):

        prev_safe = True

        while self.running:
            try:
                self.weather.update()
                currently_safe = self.safety.is_safe()

                if currently_safe:
                    self.safety_monitor_armed = True
                    self.unsafe_shutdown_triggered = False

                elif self.safety_monitor_armed:
                    if (
                        not self.unsafe_shutdown_triggered
                        and not self.shutdown_in_progress
                    ):
                        self.shutdown_in_progress = True

                        try:
                            self.safe_shutdown()
                            self.unsafe_shutdown_triggered = True

                        finally:
                            self.shutdown_in_progress = False

            except Exception as e:
                self.logger.error(f'Monitoring error: {e}')

            time.sleep(10)    #change number eventually

    def stop(self):
        self.running = False

        if self.monitor_thread is not None:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None

    def open_dome(self):
        if not self.safety.is_safe():
            self.logger.warning('Dome opening prevented')
            return False

        return self.dome.open_dome()


    def open_left(self):
        if not self.safety.is_safe():
            self.logger.warning('Left dome opening prevented')
            return False

        return self.dome.open_left()


    def open_right(self):
        if not self.safety.is_safe():
            self.logger.warning('Right dome opening prevented')
            return False

        return self.dome.open_right()
    
    def close_left(self):
        if self.mount.is_connected():
            self.mount.stop_motion()
        return self.dome.close_left()


    def close_right(self):
        if self.mount.is_connected():
            self.mount.stop_motion()
        return self.dome.close_right()

    def get_safety_status(self):
        return self.safety.get_status()

    def close_dome(self):
        if self.mount.is_connected():
            self.mount.stop_motion()
        return self.dome.close_dome()

    def safe_shutdown(self):
        if self.mount.is_connected():
            self.mount.stop_motion()
        self.dome.close_dome()


    def unpark_mount(self):
        if not self.safety.can_unpark_mount():
            self.logger.warning('Mount unpark prevented')
            return False

        return self.mount.unpark()
    
    def slew_mount(self, ra: float, dec: float):
        if not self.safety.can_start_observing():
            self.logger.warning('Mount slew prevented')
            return False

        return self.mount.slew_to_ra_dec(ra, dec)
    
    def start_tracking(self):
        if not self.safety.can_start_observing():
            self.logger.warning('Mount tracking start prevented')
            return False

        return self.mount.start_tracking()