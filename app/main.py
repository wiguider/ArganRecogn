################################################################################>>>>>>
# 1 Define the problem
# 2 Prepare Data:
#               *Loading Data
#                       Loop all the training set<image> and Store the dected Face in SequenceFile: Succo : <nameofFolder=>nameofImage,Img => Face >
#               *Summarizing Data
#               *Visualizing Data
# 3 Evaluate Algorithms and Models
#                       Train the set of faces with diffrent Models : NN,.... based on Accurancy (for me, only )
# 4 Make some Predictions(i will stop here) and Improve Results
#                       Test the Test-img-set with calculating accurancy
# 5 Present Results
##################################################################################>>>>>

import ConfigParser
import os
import sys
import platform
import graphlab as gl
from PyQt4 import QtGui

from app.ui.QDataViewer import *

from app.presentation.ArganRecongn import ArganRecogn
from app.helpers.DataLoadUtils import DataLoaderUtils as DAL


class Main:
    def __init__(self):
        # Paths properties
        self.absolute_path = self.get_absolute_path()
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.absolute_path + '/config.ini')
        self.facesFolderTest = self.absolute_path + self.config.get('Paths', 'facesFolderTest')
        self.classifier_path = self.absolute_path + self.config.get('Paths', 'classifier_path')
        # Attributes
        self.mw = None
        self.label = None
        self.data_loader = DAL()
        self.argan_recogn = ArganRecogn(self.config, self.classifier_path, self.absolute_path)

    @staticmethod
    def get_absolute_path():
        system = platform.system()
        if system == 'Darwin':
            return os.getcwd()
        elif system == 'Linux':
            return os.path.dirname(os.getcwd())
        else:
            return os.getcwd()

    def show_evaluate_data(self, eval_):
        cf_mat = eval_['confusion_matrix']
        accuracy = float(eval_['accuracy']) * 100.0

        print 'accuracy', accuracy
        print cf_mat

        if accuracy == 0.0:
            text = 'The network failed to recognize this person ( accuracy = {accuracy} ) %'.format(accuracy=accuracy)
        else:
            text = '{prefix}{predicted} with an accuracy of {accuracy} %'.format(
                prefix='This photo matches : ',
                predicted=cf_mat['predicted_label'][0]
                    .replace("_", " "),
                accuracy=accuracy)

        self.label.setText(text)

    def evaluate(self):
        self.label.setText('Evaluating...')
        eval_ = self.argan_recogn.evaluate_images()
        self.show_evaluate_data(eval_)

    def learn(self):
        self.argan_recogn.learn()

    def upload(self):
        self.mw.upload()
        self.evaluate()

    def run(self):
        app = QtGui.QApplication(sys.argv)

        self.mw = QDataViewer()

        self.mw.label = self.mw.add_label('Hello !')
        self.mw.image = self.mw.add_label('')
        self.label = self.mw.add_label('')
        self.mw.set_upload_destination(self.facesFolderTest)
        # self.mw.add_button('UPLOAD', self.upload)
        self.mw.add_button('EVALUATE', self.upload)
        self.mw.add_button('TRAIN', self.learn)
        self.mw.build()
        self.mw.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Main().run()
