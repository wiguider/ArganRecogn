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

from app.helpers.FaceDetector import FaceDetector as fd
from app.ui.QDataViewer import *

# Paths properties
system = platform.system()
if system == 'Darwin':
    absolute_path = os.getcwd()
elif system == 'Linux':
    absolute_path = os.path.dirname(os.getcwd())
else:
    absolute_path = os.getcwd()

config = ConfigParser.ConfigParser()
config.read(absolute_path + '/config.ini')

cascPath = absolute_path + config.get('Paths', 'cascPath')
facesFolder = absolute_path + config.get('Paths', 'facesFolder')
testset = absolute_path + config.get('Paths', 'testset')
images_google = absolute_path + config.get('Paths', 'images_google')
facesFolderTest = absolute_path + config.get('Paths', 'facesFolderTest')
imgsdir = absolute_path + config.get('Paths', 'imgsdir')
classifier_path = absolute_path + config.get('Paths', 'classifier_path')

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
        QDataViewer.show_alert_dialog(e)


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
            classes.append(DataProvider.get_face_name(element))
        # Columns :  path |   image | Class
        images_array.add_column(gl.SArray(data=classes), name='Class')
        images_array.remove_column('path')
        return images_array
    except Exception as e:
        QDataViewer.show_alert_dialog("ERROR : Load the faces in a Frame ")


def split_images_array(images_array):
    print "step 3 : Splitting the Data to Training set, Validation and Test Sets"
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
        QDataViewer.show_alert_dialog(e)


def train_network(training_data, validation_data):
    print "step 4 : Create and Train Data with Training,validation sets"
    try:
        network = gl.deeplearning.create(training_data, target=target)

        if os.path.exists(classifier_path):
            # Loading a trained classifier
            classifier = load_classifier()
        else:
            # Creating a new classifier
            classifier = gl.neuralnet_classifier.create(training_data,
                                                        target=target,
                                                        network=network,
                                                        validation_set=validation_data,
                                                        metric=metric,
                                                        max_iterations=max_iterations)
        return classifier, network
    except Exception as e:
        QDataViewer.show_alert_dialog(e)


def load_classifier():
    try:
        if os.path.exists(classifier_path):
            print "> load_classifier"
            classifier = gl.load_model(classifier_path)
            return classifier
    except Exception as e:
        print "ERROR : load_classifier"
        print e.message
        QDataViewer.show_alert_dialog(e)


def classify_and_save(classifier, test_data):
    print "step 5 : Classify Data with Test Set"
    # classify the test set and print predict
    try:
        pred = classifier.classify(test_data)
        print pred
        # Save to file
        if not os.path.exists(absolute_path + '/data'):
            os.makedirs(absolute_path + '/data')
        classifier.save(classifier_path)
    except Exception as e:
        QDataViewer.show_alert_dialog(e)


def evaluate_image():
    try:
        label.setText('Evaluating...')
        images_array = load_images(facesFolderTest)
        images_array['image'] = gl.image_analysis.resize(images_array['image'], 50, 50, 1, decode=True)
        classifier = load_classifier()
        print classifier
        classifier.classify(images_array)
        eval_ = classifier.evaluate(images_array, metric=['accuracy', 'recall@2', 'confusion_matrix'])
        cf_mat = eval_['confusion_matrix']
        print 'accuracy', float(eval_['accuracy']) * 100.0, cf_mat
        print 'This photo matches :', cf_mat['predicted_label'][0]
        text = '{prefix}{predicted} with an accuracy of {accuracy}'.format(prefix='This photo matches : ',
                                                                           predicted=cf_mat['predicted_label'][0]
                                                                           .replace("_", " "),
                                                                           accuracy=eval_['accuracy'])
        if eval_['accuracy'] == 0.0:
            pixmap = QtGui.QPixmap(testset + '/' + cf_mat['predicted_label'][0] + '_0001.jpg')
            label.setPixmap(pixmap)
            label.show()
            global message
            message = text
        else:
            label.setText(text)


            # it ll be executed after click on "toSframe" button
    except Exception as e:
        QDataViewer.show_alert_dialog(e)


def get_missing_images():
    try:
        provider = DataProvider(facesFolder)
        provider.split_data(testset)
        provider.download_missing_images(images_google)
    except Exception as e:
        QDataViewer.show_alert_dialog(e)


def train_classify_network():
    try:
        get_missing_images()
        # Face Detection
        extract_faces_from_images()
        # Loading Data
        images_array = load_images(facesFolder)
        print gl.Sketch(images_array['Class'])
        # Splitting Data
        test_data, training_data, validation_data = split_images_array(images_array)
        # Network Training
        classifier, network = train_network(training_data, validation_data)
        print classifier
        # Data Classification
        classify_and_save(classifier, test_data)
        print "Evaluation"
        # Evaluating Classification
        print classifier.evaluate(test_data)
        # Saving the trained classifier
        classifier.save(classifier_path)
    except Exception as e:
        QDataViewer.show_alert_dialog(e)


def build_gui():
    app = QtGui.QApplication(sys.argv)

    mw = QDataViewer(facesFolderTest)

    layout = QtGui.QVBoxLayout()
    btn_layout = QtGui.QVBoxLayout()
    lbl_layout = QtGui.QHBoxLayout()
    global label
    label = mw.add_label('Hello !', lbl_layout)
    mw.image = mw.add_label('', lbl_layout)
    mw.label = mw.add_label('', lbl_layout)

    mw.add_button_upload('UPLOAD', btn_layout)
    mw.add_button('EVALUATE', evaluate_image, btn_layout)
    mw.add_button('TRAIN', train_classify_network, btn_layout)
    layout.addLayout(lbl_layout)
    layout.addLayout(btn_layout)
    mw.setLayout(layout)
    mw.show()
    sys.exit(app.exec_())


def main():
    build_gui()


if __name__ == '__main__':
    main()
