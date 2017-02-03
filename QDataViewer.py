from PyQt4 import QtCore, QtGui
from shutil import copyfile
import graphlab as graphlab
import pathlib2 as pathlib
from DataProvider import Provider


class QDataViewer(QtGui.QWidget):
    def __init__(self,destination):
        QtGui.QWidget.__init__(self)
        # Layout Init.
        self.setGeometry(650, 300, 100, 100)
        self.setWindowTitle('Upload image')
        self.uploadButton = QtGui.QPushButton('UPLOAD', self)
        self.saveButton = QtGui.QPushButton('SAVE', self)
        self.toSFrame = QtGui.QPushButton('To SFrame', self)

        hBoxLayout = QtGui.QHBoxLayout()
        hBoxLayout.addWidget(self.uploadButton)
        hBoxLayout.addWidget(self.saveButton)
        hBoxLayout.addWidget(self.toSFrame)
        self.setLayout(hBoxLayout)
        # Attributes
        self.filename = ""
        self.destination = destination
        # Signal Init.
        self.connect(self.uploadButton, QtCore.SIGNAL('clicked()'), self.open)
        self.connect(self.saveButton, QtCore.SIGNAL('clicked()'), self.save)

    def open(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        print 'Path file :', Provider.get_face_name(self.filename)

    def save(self):
        copyfile(str(self.filename), self.destination+"/"+Provider.get_face_name(self.filename)+".jpg")

    def sframe_action(self,action):
        self.connect(self.toSFrame, QtCore.SIGNAL('clicked()'), action)

