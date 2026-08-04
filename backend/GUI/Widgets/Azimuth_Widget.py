from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter,QPen
from PySide6.QtCore import Qt,QPointF
import math

class AzimuthWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.azimuth = 0
        self.setMinimumSize(300,300)

    def set_azimuth(self,az):
        dms = az
        dms = dms.rstrip('#')
        degs,mins,secs = map(float,dms.split(':'))
        self.azimuth = degs +mins/60 +secs/3600
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        radius = min(w,h)/2 - 20
        centre = QPointF(w/2,h/2)

        painter.drawEllipse(centre,radius,radius)
        painter.drawEllipse(centre,radius-30, radius-30)
        painter.drawEllipse(centre,radius-60, radius-60)
        painter.drawEllipse(centre,radius-90, radius-90)

        angle = math.radians(self.azimuth-90)

        arrow_length = radius-15
        x = centre.x() + arrow_length*math.cos(angle)
        y = centre.y() + arrow_length*math.sin(angle)

        for deg in range(0,360,30):
            theta = math.radians(deg-90)

            x1 = centre.x()
            y1 = centre.y()

            x2 = centre.x() + radius*math.cos(theta)
            y2 = centre.y() + radius*math.sin(theta)

            painter.drawLine(QPointF(x1,y1), QPointF(x2,y2))

        for deg in range(0,360,90):
            theta = math.radians(deg-90)

            x1 = centre.x()
            y1 = centre.y()

            x2 = centre.x() + (radius+10)*math.cos(theta)
            y2 = centre.y() + (radius+10)*math.sin(theta)

            painter.drawLine(QPointF(x1,y1), QPointF(x2,y2))

            

        painter.setPen(QPen(Qt.red,3))
        painter.drawPoint(centre)
        painter.drawLine(centre,QPointF(x,y))