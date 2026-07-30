from dataclasses import dataclass
from datetime import datetime
import csv

@dataclass
class MountLogEntry:
    timestamp: datetime
    ra: str
    dec: str
    az: str
    alt: str
    status: str
    slew_status: str

class MountLogger:

    def __init__(self):
        self.entries = []

    def log(self,info):
        self.entries.append(
            MountLogEntry(
                timestamp=datetime.now(),
                ra=info['ra'],
                dec=info['dec'],
                az=info['az'],
                alt=info['alt'],
                status=info['stat'],
                slew_status=info['slew_stat']
            )
        )

    def clear(self):
        self.entries.clear()


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
