from PyQt4 import QtCore, QtGui


class QLabelsPanel(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()

    def add_label(self, text):
        label = QtGui.QLabel()
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(text)
        self.layout.addWidget(label)
        return label

    def add_labels(self, labels):
        for label in labels:
            self.add_label(label)

    def set_layout(self, layout):
        self.layout = layout

    def build(self):
        self.setLayout(self.layout)
