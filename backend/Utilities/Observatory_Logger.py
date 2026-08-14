from dataclasses import dataclass
from datetime import datetime
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
    message: str

class ObservatoryLogger:

    def __init__(self):
        self.entries = []
        self.messages = []

    def log(self,info):
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

    def log_message(self, level, message):
        self.messages.append(
            ObservatoryMessageEntry(
                timestamp=datetime.now(),
                level=level,
                message=message
            )
        )

    def clear(self):
        self.entries.clear()

    def info(self, message):
        self.log_message('INFO', message)


    def warning(self, message):
        self.log_message('WARNING', message)


    def error(self, message):
        self.log_message('ERROR', message)

    def export_to_csv(self,filename):
        with open(filename,'w',newline='') as f:
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
