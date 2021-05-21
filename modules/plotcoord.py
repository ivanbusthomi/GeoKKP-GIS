import os

from qgis.core import (
    QgsCoordinateTransform,
    QgsPointXY,
    QgsGeometry,
    QgsFeature,
    QgsProject)
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.utils import iface

# using utils
from .utils import icon

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '../ui/plot_coordinate.ui'))


class PlotCoordinateDialog(QtWidgets.QDialog, FORM_CLASS):
    """ Dialog for Coordinate Plot """

    closingPlugin = pyqtSignal()

    def __init__(self, parent=iface.mainWindow()):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        super(PlotCoordinateDialog, self).__init__(parent)
        self.project = QgsProject

        self.setWindowIcon(icon("icon.png"))

        self._currentcrs = None

        self.setupUi(self)
        self.buttonBox.accepted.connect(self.startplot)
        self.listCoordsProj.crsChanged.connect(self.set_crs)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def set_crs(self):
        self._currentcrs = self.listCoordsProj.crs()
        # print(self._currentcrs.description())

    def startplot(self):

        # read the input
        text = self.list_coords.toPlainText().strip()
        # try:
        # coords = re.split(r'[\s,;:]+', text)

        # transform coordinates
        source_crs = self._currentcrs
        canvas_crs = self.canvas.mapSettings().destinationCrs()
        tr = QgsCoordinateTransform(source_crs, canvas_crs, self.project.instance().transformContext())

        # extract coordinate pairs
        coords = text.split(";")
        list_coordinates = []
        for index, coord in enumerate(coords):
            text = coords[index].split(",")
            print(text)
            X = float(text[0])
            Y = float(text[1])
            # print('X {}; Y {}'.format(X, Y))
            # x, y = tr.transform(QgsPointXY(X,Y))
            # print('nilai x {}; nilai y {}'.format(x, y))
            # geom = QgsGeometry.fromPointXY(QgsPointXY(X,Y))
            list_coordinates.append(QgsPointXY(X, Y))
            # print('{} indeks pada {}'.format(index,coord))

        print(list_coordinates)

        # layer = QgsVectorLayer('Polygon', 'Bidang Tanah' , 'memory')
        layer = self.project.instance().mapLayersByName('Persil')[0]
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygonXY([list_coordinates]))
        prov = layer.dataProvider()
        prov.addFeatures([feat])
        # layer.setCrs(source_crs)
        layer.updateExtents()
        # uri = os.path.join(os.path.dirname(__file__), '../styles/dimension.qml')
        # layer.loadNamedStyle(uri)
        # layer = self.iface.activeLayer()
        # print(layer.name())
        # self.project.instance().addMapLayers([layer])
        layer.triggerRepaint()
        extent = layer.extent()
        self.canvas.setExtent(tr.transform(extent))

        # polygon = QgsRubberBand(self.canvas)
        # polygon.setToGeometry(QgsGeometry.fromPolygonXY([list_coordinates]), None)
        # polygon.setColor(QColor(0, 0, 255))
        # polygon.setFillColor(QColor(255,255,0))
        # polygon.setWidth(3)
        # self.canvas.setCenter(list_coordinates[0])

        # print("then, {}".format(coords[3].split(",")[0]))
        # print("then, {}".format(coords[3].split(",")[1]))
        # self.zoomTo(self._currentcrs, lat, lon)
        # except Exception:
        #   pass
