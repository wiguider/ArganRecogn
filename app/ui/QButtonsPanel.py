from PyQt4 import QtCore, QtGui


class QButtonsPanel(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QHBoxLayout()

    def add_button(self, text, action):
        button = QtGui.QPushButton(text, self)
        self.connect(button, QtCore.SIGNAL('clicked()'), action)
        self.layout.addWidget(button)

    def add_buttons(self, buttons):
        for button in buttons:
            self.layout.addWidget(button)

    def set_layout(self, layout):
        self.layout = layout

    def build(self):
        self.setLayout(self.layout)
