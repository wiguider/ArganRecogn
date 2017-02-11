from shutil import copyfile

from PyQt4 import QtCore, QtGui

from app.helpers.DataProvider import DataProvider


class QDataViewer(QtGui.QWidget):
    def __init__(self, destination):
        QtGui.QWidget.__init__(self)
        # Layout Init.
        self.setGeometry(650, 300, 100, 100)
        self.setWindowTitle('Upload image')
        # Attributes
        self.filename = ""
        self.destination = destination
        self.layout = QtGui.QHBoxLayout()
        # Signal Init.
        # self.connect(self.uploadButton, QtCore.SIGNAL('clicked()'), self.upload)

    def upload(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Upload File', '.')
        DataProvider.empty_folder(self.destination)
        print 'File name :', self.filename  # DataProvider.get_face_name(self.filename)
        copyfile(str(self.filename), self.destination + "/" + DataProvider.get_face_name(self.filename) + ".jpg")

    def button_action(self, button, action):
        self.connect(button, QtCore.SIGNAL('clicked()'), action)

    def add_button(self, text, action, layout):
        button = QtGui.QPushButton(text, self)
        self.button_action(button, action)
        layout.addWidget(button)

    def add_button_upload(self, text, layout):
        button = QtGui.QPushButton(text, self)
        self.button_action(button, self.upload)
        layout.addWidget(button)

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
