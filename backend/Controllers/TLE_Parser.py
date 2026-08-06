from datetime import datetime

class TLEParseError(Exception):
    pass

class TLEParser:

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
    
    def validate(
            self,
            line1,
            line2
    ):
        if not line1.startswith('1'):
            raise TLEParseError('First line is not a TLE line 1')
        
        if not line2.startswith('2'):
            raise TLEParseError('Second line is not a TLE line 2')
        
        if len(line1) != 69:
            raise TLEParseError('Invalid line length: line 1')
        
        if len(line2) != 69:
            raise TLEParseError('Invalid line length: line 2')
        

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
    
    def validate_checksum(self,line):

        checksum = int(line[:-1])

        for char in line[:-1]:

            if char.isdigit():
                total += int(char)

            elif char == '-':
                total +=1

        return total % 10 == checksum