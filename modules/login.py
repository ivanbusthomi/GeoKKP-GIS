import os
import json

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from .utils import storeSetting, logMessage
from .postlogin import PostLoginDock
from .api import endpoints
from .memo import app_state

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '../ui/login.ui'))


class LoginDialog(QtWidgets.QDialog, FORM_CLASS):
    """ Dialog for Login """

    closingPlugin = pyqtSignal()
    loginChanged = pyqtSignal()

    def __init__(self, parent=iface.mainWindow()):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)
        self.postloginaction = PostLoginDock()

        self.bar = QgsMessageBar()

        # login action
        self.buttonBoxLogin.clicked.connect(self.doLoginRequest)
        if self.checkboxSaveLogin.isChecked:
            self.isSaved = True
        else:
            self.isSaved = False

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def closedone(self):
        self.close()

    def doLoginRequest(self):
        """
        Login using requests
        API backend: {}/validateUser
        """

        username = self.inputUsername.text()
        password = self.inputPassword.text()
        logMessage(f'{username}, {password}')
        response = endpoints.login(username, password)
        content = json.loads(response.content)
        if not content['status']:
            message = QMessageBox(parent=self)
            message.setIcon(QMessageBox.Information)
            message.setText(content['information'])
            message.setWindowTitle("Peringatan")
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()
        else:
            if self.isSaved:
                storeSetting("geokkp/isLoggedIn", content['status'])
            logMessage(str(content))
            self.iface.messageBar().pushMessage("Login Pengguna Berhasil:", username, level=Qgis.Success)
            self.profilUser(username)
            self.loginChanged.emit()
            app_state.set('username', username)
            app_state.set('logged_in', True)
            self.accept()

    def profilUser(self, username):
        """
        user entity
        API backend: {}/getEntityByUserName
        """

        response = endpoints.get_entity_by_username(username)
        response_json = json.loads(response.content)
        # print(response_json[0]["nama"])
        storeSetting("geokkp/jumlahkantor", len(response_json))
        storeSetting("geokkp/listkantor", response_json)
        self.iface.messageBar().pushMessage(
            "Simpan Data:",
            "Data kantor pengguna berhasil disimpan",
            level=Qgis.Success
        )
        self.postlogin()

    def postlogin(self):
        print("==========ps===========")

        # if self.postloginaction is None:
        # Create the dockwidget (after translation) and keep reference
        #    self.postloginaction = PostLoginDock()

        # connect to provide cleanup on closing of dockwidget
        # self.postloginaction.closingPlugin.connect(self.onClosePlugin)

        # show the dialog
        # self.postloginaction.show()
