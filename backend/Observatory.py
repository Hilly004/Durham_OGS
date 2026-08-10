import asyncio

class ObservatoryOperations:

    def __init__(self, dome, mount, safety):
        self.dome = dome
        self.mount = mount
        self.safety = safety

        self.running = False

    def open_dome(self):
        if not self.safety.open_safe():
            print('Weather conditions unsafe')
            return False
        if not self.weather.is_connected():
            print('Weather monitor not connnected')
            return False
        
        self.dome.open_dome()


    def close_dome(self):
        self.mount.stop_motion()
        self.dome.close_dome()

    def safe_shutdown(self):
        self.state.mode = ObservatoryMode.SAFE_SHUTDOWN

        try:
            self.mount.stop_motion()
        except Exception:
            pass

        try:
            self.dome.close_dome()
        except Exception:
            pass


    async def monitor_safety(self):
        while self.running:
            self.weather.update()

            if not self.safety.is_safe():
                await self.safe_shutdown()

            await asyncio.sleep(1)


    