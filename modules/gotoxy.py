import os
import re

from qgis.PyQt.QtCore import Qt, QTimer, QUrl
from qgis.gui import QgsRubberBand

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import (Qgis,
                    QgsCoordinateReferenceSystem,
                    QgsCoordinateTransform,
                    QgsRectangle,
                    QgsPoint,
                    QgsPointXY,
                    QgsGeometry,
                    QgsWkbTypes,
                    QgsVectorLayer,
                    QgsFeature,
                    QgsProject, QgsApplication)
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.utils import iface


#using utils
from .utils import  epsg4326


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '../ui/goto.ui'))


class GotoXYDialog(QtWidgets.QDialog, FORM_CLASS):
    """ Dialog for Zoom to Location """


    closingPlugin = pyqtSignal()


    def __init__(self, parent=iface.mainWindow()):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        super(GotoXYDialog, self).__init__(parent)
        #self.utils = Utilities
        self.crossRb = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.crossRb.setColor(Qt.red)
        uri = os.path.join(os.path.dirname(__file__), '../images/icon.png')
        self.setWindowIcon(QtGui.QIcon(uri))

        self._currentcrs = None

        self.setupUi(self)
        self.buttonBox.accepted.connect(self.zoomtodialog)
        self.selectProj.crsChanged.connect(self.set_crs)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def set_crs(self):
        self._currentcrs = self.selectProj.crs()
        #print(self._currentcrs.description())

    def zoomtodialog(self):
        text = self.mLineEditXY.text().strip()
        #try:
        coords = re.split(r'[\s,;:]+', text, 1)
        lat = float(coords[0])
        lon = float(coords[1])
        #print("lat:", lat, " long:", lon)
        self.zoomTo(self._currentcrs, lat, lon)
        #except Exception:
        #   pass

    def zoomTo(self, src_crs, lat, lon):
        self.canvas.zoomScale(1000)
        canvas_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(src_crs, canvas_crs, QgsProject.instance())
        x, y = transform.transform(float(lon), float(lat))

        rect = QgsRectangle(x, y, x, y)
        self.canvas.setExtent(rect)

        pt = QgsPointXY(x, y)
        self.highlight(pt)
        self.canvas.refresh()

    def highlight(self, point):

        currExt = self.canvas.extent()

        leftPt = QgsPoint(currExt.xMinimum(), point.y())
        rightPt = QgsPoint(currExt.xMaximum(), point.y())

        topPt = QgsPoint(point.x(), currExt.yMaximum())
        bottomPt = QgsPoint(point.x(), currExt.yMinimum())

        horizLine = QgsGeometry.fromPolyline([leftPt, rightPt])
        vertLine = QgsGeometry.fromPolyline([topPt, bottomPt])

        self.crossRb.reset(QgsWkbTypes.LineGeometry)
        self.crossRb.addGeometry(horizLine, None)
        self.crossRb.addGeometry(vertLine, None)

        QTimer.singleShot(1000, self.resetRubberbands)

    def resetRubberbands(self):
        self.crossRb.reset()
