from datetime import datetime

class TLEParseError(Exception):
    pass

class TLEParser:

    def _catalog_number(self, line: str) -> str:
        return line[2:7].strip()
    
    def parse(
            self,
            name: str,
            line1: str,
            line2: str
    ):
        
        self.validate(
            line1,
            line2
        )

        return {
            'name': name,
            'norad_id': self.get_norad_id(line1),
            'line1': line1,
            'line2': line2,
            'epoch': self.get_epoch(line1),
            'inclination': self.get_inclination(line2),
            'eccentricity': self.get_eccentricity(line2)
        }
    
    def validate(self, line1: str, line2: str):
        line1 = line1.strip()
        line2 = line2.strip()

        if not line1.startswith('1 '):
            raise ValueError('Invalid TLE line 1')

        if not line2.startswith('2 '):
            raise ValueError('Invalid TLE line 2')

        catalog_1 = self._catalog_number(line1)
        catalog_2 = self._catalog_number(line2)

        if catalog_1 != catalog_2:
            raise ValueError(
                'TLE line 1 and line 2 refer to different satellites'
            )

        if not self.validate_checksum(line1):
            raise ValueError('Invalid TLE line 1 checksum')

        if not self.validate_checksum(line2):
            raise ValueError('Invalid TLE line 2 checksum')

        return True
        

    def get_norad_id(
            self,
            line1
    ):
        return int(line1[2:7])
    
    def get_epoch(
            self,
            line1
    ):
        return line1[18:32]
    
    def get_inclination(
            self,
            line2
    ):
        return float(
            line2[8:16]
        )
    
    def get_eccentricity(
            self,
            line2
    ):
        value = line2[26:33]

        return float('0.'+ value)
    
    def validate_checksum(self, line: str) -> bool:
        if len(line) < 2:
            return False

        expected_checksum = int(line[-1])

        total = 0

        for char in line[:-1]:
            if char.isdigit():
                total += int(char)

            elif char == '-':
                total += 1

        calculated_checksum = total % 10

        return calculated_checksum == expected_checksum