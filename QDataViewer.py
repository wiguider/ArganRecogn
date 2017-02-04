from shutil import copyfile

from PyQt4 import QtCore, QtGui

from DataProvider import Provider


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
        print 'File name :', Provider.get_face_name(self.filename)
        copyfile(str(self.filename), self.destination + "/" + Provider.get_face_name(self.filename) + ".jpg")

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
