class SettingsController:
    def __init__(
        self,
        repository,
        weather=None,
        observatory=None,
        logger=None,
        mount_connection=None,
        dome_connection=None,
        weather_connection=None,
    ):
        self.repository = repository
        self.weather = weather
        self.observatory = observatory
        self.logger = logger
        self.mount_connection = mount_connection
        self.dome_connection = dome_connection
        self.weather_connection = weather_connection

    def get_settings(self):
        return self.repository.get_or_create()

    def update_settings(self, values: dict):
        current = self.get_settings()

        mount_changed = (
            values.get("mount_host") != current.mount_host
            or values.get("mount_port") != current.mount_port
        )
        dome_changed = (
            values.get("dome_host") != current.dome_host
            or values.get("dome_port") != current.dome_port
        )
        weather_changed = (
            values.get("weather_port") != current.weather_port
            or values.get("weather_baudrate") != current.weather_baudrate
        )

        if mount_changed and self.mount_connection and self.mount_connection.connected:
            raise RuntimeError("Disconnect mount before changing its connection settings")

        if dome_changed and self.dome_connection and self.dome_connection.is_connected():
            raise RuntimeError("Disconnect dome before changing its connection settings")

        if weather_changed and self.weather_connection:
            serial_port = getattr(self.weather_connection, "serial", None)
            if serial_port is not None and serial_port.is_open:
                raise RuntimeError("Disconnect weather station before changing its connection settings")

        updated = self.repository.update(current, values)
        self.apply_settings(updated)

        if self.logger:
            self.logger.success("Observatory settings saved", source="SYSTEM")

        return updated

    def apply_saved_settings(self):
        settings = self.get_settings()
        self.apply_settings(settings)
        return settings

    def apply_settings(self, settings):
        if self.weather is not None:
            self.weather.max_wind_speed = settings.max_wind_speed
            self.weather.max_humidity = settings.max_humidity

        if self.observatory is not None:
            self.observatory.automatic_shutdown_enabled = settings.automatic_shutdown_enabled
            self.observatory.safety.weather_timeout_seconds = settings.weather_timeout_seconds

        if self.logger is not None:
            self.logger.max_messages = settings.activity_log_max_entries

        if self.mount_connection is not None and not self.mount_connection.connected:
            self.mount_connection.configure(settings.mount_host, settings.mount_port)

        if self.dome_connection is not None and not self.dome_connection.is_connected():
            self.dome_connection.configure(settings.dome_host, settings.dome_port)

        if self.weather_connection is not None:
            serial_port = getattr(self.weather_connection, "serial", None)
            if serial_port is None or not serial_port.is_open:
                self.weather_connection.configure(settings.weather_port, settings.weather_baudrate)