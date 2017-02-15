from shutil import copyfile

from PyQt4 import QtCore, QtGui

from app.helpers.DataProvider import DataProvider

from app.ui.QButtonsPanel import QButtonsPanel as ButtonsPanel
from app.ui.QLabelsPanel import QLabelsPanel as LabelsPanel


class QDataViewer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Layout Init.
        self.setGeometry(300, 300, 600, 100)
        self.setWindowTitle('Upload image')
        # Attributes
        self.filename = ""
        self.upload_destination = ""

        self.layout = QtGui.QVBoxLayout()
        self.image = QtGui.QLabel()
        self.labels_panel = LabelsPanel()
        self.buttons_panel = ButtonsPanel()

    def set_upload_destination(self, upload_destination):
        self.upload_destination = upload_destination

    def upload(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Upload File', '.')
        self.label.setPixmap(QtGui.QPixmap())

        DataProvider.empty_folder(self.upload_destination)
        print 'File name :', self.filename  # DataProvider.get_face_name(self.filename)
        copyfile(str(self.filename), self.upload_destination + "/" + DataProvider.get_face_name(self.filename) + ".jpg")

        pixmap = QtGui.QPixmap(self.filename)
        # self.label.setPixmap(pixmap)
        # self.label.show()
        self.image.setPixmap(pixmap)

    def add_button(self, text, action):
        self.buttons_panel.add_button(text, action)

    def add_label(self, text):
        return self.labels_panel.add_label(text)

    @staticmethod
    def show_alert_dialog(exception):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        msg.setText("Something wrong occurred")
        msg.setInformativeText(exception.message)
        msg.setWindowTitle("Something wrong occurred")
        msg.setDetailedText("The details are as follows:\n" + exception.message)
        print "The details are as follows:\n" + exception.message
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msg.buttonClicked.connect(QDataViewer.msgbtn)

        retval = msg.exec_()
        print "value of pressed message box button:", retval

    @staticmethod
    def show_dialog(message, title):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("Something wrong occurred")
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msg.buttonClicked.connect(QDataViewer.msgbtn)

        retval = msg.exec_()
        print "value of pressed message box button:", retval

    @staticmethod
    def msgbtn(i):
        print "Button pressed is:", i.text()

    def build(self):
        self.labels_panel.build()
        self.buttons_panel.build()
        self.layout.addWidget(self.labels_panel)
        self.layout.addWidget(self.buttons_panel)
        self.setLayout(self.layout)
