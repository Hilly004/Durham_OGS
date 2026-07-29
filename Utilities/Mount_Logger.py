from dataclasses import dataclass
from datetime import datetime

@dataclass
class MountLogEntry:
    timestamp: datetime
    ra: str
    dec: str
    status: str
    slew_status: str

class MountLogger:

    def __init__(self):
        self.entries = []

    def log(self,ra,dec,status,slew_status):
        self.entries.append(
            MountLogEntry(
                timestamp=datetime.now(),
                ra=ra,
                dec=dec,
                status=status,
                slew_status=slew_status
            )
        )

    def clear(self):
        self.entries.clear()