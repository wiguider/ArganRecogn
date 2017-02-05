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

import graphlab as gl

import ConfigParser

import sys

import os

from shutil import copyfile

from FaceDetector import FaceDetector as fd

from DataProvider import Provider

from NeurNetEval import NetEval

from QDataViewer import *

from PyQt4.QtGui import *

from PyQt4.QtCore import *

# Paths properties
config = ConfigParser.ConfigParser()
config.read('config.ini')
path = config.get('Paths', 'path')
cascPath = config.get('Paths', 'cascPath')
facesFolder = config.get('Paths', 'facesFolder')
testset = config.get('Paths', 'testset')
images_google = config.get('Paths', 'images_google')
facesFolderTest = config.get('Paths', 'facesFolderTest')
imgsdir = config.get('Paths', 'imgsdir')

# Network properties
max_iterations = config.get('Net', 'max_iterations')
target = config.get('Net', 'target')
metric = config.get('Net', 'metric').split(',')


def extract_faces_from_images():
    print "step 1 : DONE ONLY ONCE : Extract Faces from images and put in a dictionary " \
          "<label:name_of_face, value:path_to_face>, the dict is optionally"
    try:
        fd.face_extractor(imgsdir, cascPath, facesFolder)
        fd.face_extractor_google(images_google, cascPath, facesFolder)
    except Exception as e:
        show_dialog(e)


def load_images(images_folder):
    print "step 2 : Load the faces in a Frame : <Image_brut,Its_Class>"
    # load_images return an SFrame :  path |   image
    try:
        images_array = gl.image_analysis.load_images(images_folder,
                                                     "auto",
                                                     with_path=True,
                                                     recursive=True,
                                                     ignore_failure=True)
        classes = []
        for element in images_array['path']:
            classes.append(Provider.get_face_name(element))
        # Columns :  path |   image | Class
        images_array.add_column(gl.SArray(data=classes), name='Class')
        images_array.remove_column('path')
        return images_array
    except Exception as e:
        show_dialog(e)


def split_images_array(images_array):
    print "step 3 : Splitting the Data to Traing set, Validation and Test Sets"
    try:
        # Creating test samples
        test_data = load_images(testset)
        # Creating training samples
        training_data, validation_data = images_array.random_split(0.8)
        # make sure that all faces have the same size
        training_data['image'] = gl.image_analysis.resize(training_data['image'], 50, 50, 1, decode=True)
        validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 50, 50, 1, decode=True)
        test_data['image'] = gl.image_analysis.resize(test_data['image'], 50, 50, 1, decode=True)
        return test_data, training_data, validation_data
    except Exception as e:
        show_dialog(e)


def train_network(training_data, validation_data):
    print "step 4 : Create and Train Data with Training,validation sets"
    try:
        network = gl.deeplearning.create(training_data, target=target)
        try:
            classifier = load_classifier()
        except Exception as e:
            classifier = gl.neuralnet_classifier.create(training_data,
                                                        target=target,
                                                        network=network,
                                                        validation_set=validation_data,
                                                        metric=metric,
                                                        max_iterations=max_iterations)
        return classifier, network
    except Exception as e:
        show_dialog(e)


def load_classifier():
    try:
        classifier = gl.deeplearning.load('data/classifier.conf')
        return classifier
    except Exception as e:
        print e.message
        show_dialog(e)


def classify_and_save(classifier, test_data):
    print "step 5 : Classify Data with Test Set"
    # classify the test set and print predict
    try:
        pred = classifier.classify(test_data)
        print pred
        # Save to file
        if not os.path.exists('data'):
            os.makedirs('data')
        pred.save('data/training_data.json', format='json')
    except Exception as e:
        show_dialog(e)


def image_to_sframe():
    try:
        print load_images(facesFolderTest)
        # it ll be executed after click on "toSframe" button
    except Exception as e:
        show_dialog(e)


def get_missing_images():
    try:
        provider = Provider(facesFolder)
        provider.split_data(testset)
        provider.download_missing_images(images_google)
    except Exception as e:
        show_dialog(e)


def train_classify_network():
    try:
        get_missing_images()
        extract_faces_from_images()
        images_array = load_images(facesFolder)
        print gl.Sketch(images_array['Class'])
        test_data, training_data, validation_data = split_images_array(images_array)
        classifier, network = train_network(training_data, validation_data)
        print classifier
        classify_and_save(classifier, test_data)
        print "Evaluation"
        print classifier.evaluate(test_data)
        classifier.save('data/classifier.conf')
    except Exception as e:
        show_dialog(e)


def build_gui():
    app = QtGui.QApplication(sys.argv)
    mw = QDataViewer(facesFolderTest)
    layout = QtGui.QHBoxLayout()
    mw.add_button_upload('UPLOAD', layout)
    mw.add_button('To SFrame', image_to_sframe, layout)
    mw.add_button('TRAIN', train_classify_network, layout)
    mw.setLayout(layout)
    mw.show()
    sys.exit(app.exec_())


def show_dialog(exception):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Something wrong occurred")
    msg.setInformativeText("Additional information")
    msg.setWindowTitle("Something wrong occurred")
    msg.setIcon("Warning")
    msg.setDetailedText("The details are as follows:\n" + exception.message)
    print "The details are as follows:\n" + exception.message
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print "value of pressed message box button:", retval


def msgbtn(i):
    print "Button pressed is:", i.text()


def main():
    build_gui()


if __name__ == '__main__':
    main()
