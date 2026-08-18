from dataclasses import dataclass
from datetime import datetime
from threading import Lock
import csv


@dataclass
class ObservatoryLogEntry:
    timestamp: datetime
    ra: str
    dec: str
    az: str
    alt: str
    status: str
    slew_status: str


@dataclass
class ObservatoryMessageEntry:
    timestamp: datetime
    level: str
    source: str
    message: str


class ObservatoryLogger:

    def __init__(self):
        self.entries = []
        self.messages = []

        self._lock = Lock()


    def log(self, info):
        with self._lock:
            self.entries.append(
                ObservatoryLogEntry(
                    timestamp=datetime.now(),
                    ra=info['ra'],
                    dec=info['dec'],
                    az=info['az'],
                    alt=info['alt'],
                    status=info['stat'],
                    slew_status=info['slew_stat']
                )
            )


    def log_message(
        self,
        level: str,
        message: str,
        source: str = "SYSTEM"
    ):
        with self._lock:

            self.messages.append(
                ObservatoryMessageEntry(
                    timestamp=datetime.now(),
                    level=level,
                    source=source.upper(),
                    message=message
                )
            )

            # Prevent the activity log growing forever
            if len(self.messages) > 500:
                self.messages = self.messages[-500:]


    def get_messages(self, limit: int = 100):

        with self._lock:
            messages = self.messages[-limit:]

            return list(messages)


    def clear_messages(self):
        with self._lock:
            self.messages.clear()


    def clear(self):
        with self._lock:
            self.entries.clear()


    def info(
        self,
        message: str,
        source: str = "SYSTEM"
    ):
        self.log_message(
            "INFO",
            message,
            source
        )


    def success(
        self,
        message: str,
        source: str = "SYSTEM"
    ):
        self.log_message(
            "SUCCESS",
            message,
            source
        )


    def warning(
        self,
        message: str,
        source: str = "SYSTEM"
    ):
        self.log_message(
            "WARNING",
            message,
            source
        )


    def error(
        self,
        message: str,
        source: str = "SYSTEM"
    ):
        self.log_message(
            "ERROR",
            message,
            source
        )


    def export_to_csv(self, filename):

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow([
                "Timestamp",
                "RA",
                "DEC",
                "AZ",
                "ALT",
                "Status",
                "Slew Status"
            ])

            for entry in self.entries:
                writer.writerow([
                    entry.timestamp.isoformat(),
                    entry.ra,
                    entry.dec,
                    entry.az,
                    entry.alt,
                    entry.status,
                    entry.slew_status
                ])

        print('Log exported to CSV')