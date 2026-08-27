from Controllers.safety_manager import SafetyManager
import time
import threading

class ObservatoryController:

    def __init__(self, dome, mount, weather,logger):
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
        self.logger = logger

        self.shutdown_in_progress = False
        self.unsafe_shutdown_triggered = False

        self.automatic_shutdown_enabled = True

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

        last_monitor_error = None

        while self.running:

            try:

                self.weather.update()

                if not self.automatic_shutdown_enabled:
                    time.sleep(2)
                    continue

                currently_safe = (
                    self.safety.is_safe()
                )

                if currently_safe:

                    self.unsafe_shutdown_triggered = False

                else:

                    if (
                        not self.unsafe_shutdown_triggered
                        and
                        not self.shutdown_in_progress
                    ):

                        self.shutdown_in_progress = True

                        try:

                            self.logger.warning(
                                "Unsafe conditions detected - stopping mount and closing dome",
                                source="SYSTEM"
                            )

                            self.safe_shutdown()

                            self.unsafe_shutdown_triggered = True

                        finally:

                            self.shutdown_in_progress = False

                last_monitor_error = None

            except Exception as e:

                error_message = str(e)

                if error_message != last_monitor_error:

                    self.logger.error(
                        f"Monitoring error: {error_message}",
                        source="SYSTEM"
                    )

                    last_monitor_error = error_message

            time.sleep(2)

    def stop(self):
        self.running = False

        if self.monitor_thread is not None:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None

    def open_dome(self):
        if not self.safety.is_safe():
            self.logger.warning('Dome opening prevented',
                                source='DOME')
            return False

        return self.dome.open_dome()


    def open_left(self):
        if not self.safety.is_safe():
            self.logger.warning('Left dome opening prevented',
                                source='DOME')
            return False

        return self.dome.open_left()


    def open_right(self):
        if not self.safety.is_safe():
            self.logger.warning('Right dome opening prevented',
                                source='DOME')
            return False

        return self.dome.open_right()
    
    def close_left(self):

        if self.mount.is_connected():
            self.mount.stop_motion()


        if not self.dome.is_connected:
            return False


        return self.dome.close_left()


    def close_right(self):

        if self.mount.is_connected():
            self.mount.stop_motion()


        if not self.dome.is_connected:
            return False


        return self.dome.close_right()

    def get_safety_status(self):
        return self.safety.get_status()

    def close_dome(self):

        if self.mount.is_connected():
            self.mount.stop_motion()


        if not self.dome.is_connected:
            return False


        return self.dome.close_dome()

    def safe_shutdown(self):

        if self.mount.is_connected():
            self.mount.stop_motion()

        if self.dome.is_connected:
            self.dome.close_dome()


    def unpark_mount(self):
        if not self.safety.can_unpark_mount():
            self.logger.warning('Mount unpark prevented',
                                source='MOUNT')
            return False

        return self.mount.unpark()
    
    def slew_mount(self, ra: float, dec: float):
        if not self.safety.can_start_observing():
            self.logger.warning('Mount slew prevented',
                                source='MOUNT')
            return False

        return self.mount.slew_to_ra_dec(ra, dec)
    
    def start_tracking(self):
        if not self.safety.can_start_observing():
            self.logger.warning('Mount tracking start prevented',
                                source='MOUNT')
            return False

        return self.mount.start_tracking()
    
    def nudge_mount(
        self,
        direction: str,
        step_arcsec: float
    ):

        if not self.safety.can_start_observing():

            self.logger.warning(
                "Mount nudge prevented by safety system",
                source="MOUNT"
            )

            return False

        self.mount.nudge(
            direction,
            step_arcsec
        )

    
    def move_mount(
        self,
        direction: str,
    ):

        if not self.safety.can_start_observing():

            self.logger.warning(
                "Mount movement prevented by safety system",
                source="MOUNT"
            )

            return False

        if direction == "north":
            self.mount.move_north()

        elif direction == "south":
            self.mount.move_south()

        elif direction == "east":
            self.mount.move_east()

        elif direction == "west":
            self.mount.move_west()

        else:
            raise ValueError(
                f"Invalid mount direction: {direction}"
            )

        return True