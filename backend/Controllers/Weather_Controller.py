class WeatherController:

    def __init__(self, monitor, logger):

        self.monitor = monitor
        self.logger = logger

        # None  = use real weather
        # True  = force safe
        # False = force unsafe
        self._safety_override = None


    def set_safety_override(
        self,
        value: bool | None
    ):

        self._safety_override = value

        if value is True:

            self.logger.warning(
                "Weather safety override enabled: FORCE SAFE",
                source="WEATHER"
            )

        elif value is False:

            self.logger.warning(
                "Weather safety override enabled: FORCE UNSAFE",
                source="WEATHER"
            )

        else:

            self.logger.info(
                "Weather safety override disabled",
                source="WEATHER"
            )


    def get_safety_override(self):
        return self._safety_override


    def connect(self):

        try:

            connected = self.monitor.connect()

            if not connected:

                self.logger.error(
                    "Weather station connection failed",
                    source="WEATHER"
                )

                return False


            if not self.monitor.is_connected():

                self.logger.error(
                    "Weather station connection failed",
                    source="WEATHER"
                )

                return False


            self.logger.success(
                "Weather station connected",
                source="WEATHER"
            )

            return True


        except Exception as e:

            self.logger.error(
                f"Weather station connection failed: {e}",
                source="WEATHER"
            )

            return False


    def disconnect(self):
        return self.monitor.disconnect()


    @property
    def is_connected(self):
        return self.monitor.is_connected()


    def update(self):
        return self.monitor.update()


    @property
    def last_update(self):
        return self.monitor.last_update


    def safe(self):
        """
        Effective observatory safety state.

        Override takes priority over the
        real weather state.
        """

        if self._safety_override is not None:
            return self._safety_override

        return self._get_actual_status()["safe"]


    def _get_actual_status(self):
        """
        Return the real weather condition,
        ignoring any safety override.
        """

        if not self.is_connected:

            return {
                "state": "unknown",
                "safe": False,
                "reason": "Weather station disconnected"
            }


        try:

            raining = self.monitor.is_raining()
            wind_speed = self.monitor.wind_speed()
            humidity = self.monitor.humidity()

        except Exception as e:

            self.logger.error(
                f"Unable to read weather conditions: {e}",
                source="WEATHER"
            )

            return {
                "state": "unknown",
                "safe": False,
                "reason": "Weather data unavailable"
            }


        if raining:

            return {
                "state": "unsafe",
                "safe": False,
                "reason": "Rain detected"
            }


        if wind_speed >= 40:

            return {
                "state": "unsafe",
                "safe": False,
                "reason": "Wind speed above safety limit"
            }


        if humidity >= 95:

            return {
                "state": "unsafe",
                "safe": False,
                "reason": "Humidity above safety limit"
            }


        return {
            "state": "safe",
            "safe": True,
            "reason": None
        }


    def get_status(self):
        """
        Return both the real sensor state and
        the effective state used by the observatory.
        """

        actual_status = self._get_actual_status()

        actual_safe = actual_status["safe"]

        effective_safe = self.safe()


        if self._safety_override is True:

            state = "safe"
            reason = "Weather safety overridden: FORCE SAFE"

        elif self._safety_override is False:

            state = "unsafe"
            reason = "Weather safety overridden: FORCE UNSAFE"

        else:

            state = actual_status["state"]
            reason = actual_status["reason"]


        return {
            "connected": self.is_connected,

            # Effective state used by observatory
            "safe": effective_safe,

            # Real sensor state
            "actualSafe": actual_safe,

            # None / True / False
            "override": self._safety_override,

            "state": state,
            "reason": reason,
        }