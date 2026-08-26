import time


class SafetyManager:

    def __init__(
        self,
        mount,
        dome,
        weather
    ):
        self.weather = weather
        self.mount = mount
        self.dome = dome

        self.weather_timeout_seconds = 10

    def get_status(self):

        # ---------------------------------
        # Weather
        # ---------------------------------

        override = (
            self.weather
            .get_safety_override()
        )


        # Force unsafe always wins.
        if override is False:

            return {
                "safe": False,
                "reason":
                    "Weather override: FORCE UNSAFE"
            }


        # Force safe bypasses physical
        # weather availability / freshness.
        if override is not True:

            if self.weather.last_update is None:

                return {
                    "safe": False,
                    "reason":
                        "Weather data unavailable"
                }


            if (
                time.monotonic()
                - self.weather.last_update
                > self.weather_timeout_seconds
            ):

                return {
                    "safe": False,
                    "reason":
                        "Weather data stale"
                }


            weather_status = (
                self.weather.get_status()
            )


            if not weather_status["safe"]:

                return {
                    "safe": False,
                    "reason":
                        weather_status["reason"]
                }


        # ---------------------------------
        # Dome
        # ---------------------------------
        #
        # Only query physical dome fault
        # registers if the dome is connected.
        #
        # Otherwise read_coil() raises:
        # "Dome not connected".
        # ---------------------------------

        if self.dome.is_connected:

            try:

                if self.dome.has_fault:

                    return {
                        "safe": False,
                        "reason":
                            "Dome fault detected"
                    }

            except Exception as e:

                return {
                    "safe": False,
                    "reason":
                        f"Dome status unavailable: {e}"
                }


        # ---------------------------------
        # Safe
        # ---------------------------------

        return {
            "safe": True,
            "reason": None
        }


    def is_safe(self):
        return self.get_status()["safe"]


    def can_close_dome(self):
        return True


    def can_unpark_mount(self):
        return self.is_safe()


    def can_start_observing(self):
        return self.is_safe()