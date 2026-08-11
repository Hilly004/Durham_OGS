from Controllers.safety_manager import SafetyManager
import time
import threading

class ObservatoryController:

    def __init__(self, dome, mount, weather):
        self.dome = dome
        self.mount = mount
        self.safety = SafetyManager(
            mount,
            dome,
            weather
        )

        self.running = False
        self.monitor_thread = None

    def start(self):
        self.running = True

        self.monitor_thread = threading.Thread(
            target = self._monitor,
            daemon=True
        )

        self.monitor_thread.start()


    def _monitor(self):

        prev_safe = True

        while self.running:
            try:
                self.weather.update()
                currently_safe = self.safety.is_safe()

                if prev_safe and not currently_safe:
                    print('Unsafe conditions detected')
                    self.safe_shutdown()

                prev_safe = currently_safe

            except Exception as e:
                print(f'Monitoring error: {e}')

            time.sleep(1000)    #change number eventually

    def stop(self):
        self.running = False

    def open_dome(self):
        if not self.safety.is_safe:
            self.logger.warning('Dome opening prevented')
            return False

        return self.dome.open_dome()



    def close_dome(self):
        self.mount.stop_motion()
        self.dome.close_dome()

    def safe_shutdown(self):
        self.dome.close_dome()
        self.mount.park()



    