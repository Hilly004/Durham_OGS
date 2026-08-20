from models.settings import ObservatorySettings


class SettingsRepository:
    def __init__(self, db):
        self.db = db

    def get(self):
        return (
            self.db.query(ObservatorySettings)
            .filter(ObservatorySettings.id == 1)
            .first()
        )

    def get_or_create(self):
        settings = self.get()
        if settings is not None:
            return settings

        settings = ObservatorySettings(id=1)
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def update(self, settings, values: dict):
        for key, value in values.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        self.db.commit()
        self.db.refresh(settings)
        return settings
