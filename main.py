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
import os

from FaceDetector import FaceDetector as fd
from DataProvider import Provider
from  NeurNetEval import NetEval

# Get user supplied values
config = ConfigParser.ConfigParser()
config.read('config.ini')
path = config.get('Paths', 'path')
cascPath = config.get('Paths', 'cascPath')
facesFolder = config.get('Paths', 'facesFolder')
testset = config.get('Paths', 'testset')
facesFolderTest = config.get('Paths', 'facesFolderTest')
imgsdir = config.get('Paths', 'imgsdir')


# TODO: 1.Crop the face zone # STATUS: DONE
# TODO: 2.Extract the characteristics from the face zone # STATUS: WHICH CHARACTERISTICS ?
# TODO: 3.Compare the characteristics vectors of the probe set samples with the ones of the gallery samples # STATUS: ?

def extract_faces_from_images():
    print "step 1 : DONE ONLY ONCE : Extract Faces from images and put in a dictionary " \
          "<label:name_of_face, value:path_to_face>, the dict is optionally"
    fd.face_extractor(imgsdir, cascPath, facesFolder)


def load_images_in_frame():
    print "step 2 : Load the faces in a Frame : <Image_brut,Its_Class>"
    # load_images return an SFrame :  path |   image
    images_array = gl.image_analysis.load_images(facesFolder,
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

def load_test_images_set():
    print "step 2 : Load the facesTest in a Frame : <Image_brut,Its_Class>"
    # load_images return an SFrame :  path |   image
    images_array = gl.image_analysis.load_images(testset,
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


def split_images_array(images_array):
    print "step 3 : Spliting the Data to Traing set, Validation and Test Sets"
    # Creating test samples
    test_data = load_test_images_set()
    # Creating training samples
    training_data, validation_data = images_array.random_split(0.8)
    # make sure that all faces have the same size
    training_data['image'] = gl.image_analysis.resize(training_data['image'], 50, 50, 1, decode=True)
    validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 50, 50, 1, decode=True)
    test_data['image'] = gl.image_analysis.resize(test_data['image'], 50, 50, 1, decode=True)
    return test_data, training_data, validation_data


def train_network(training_data, validation_data,nmbr_iter):
    print "step 4 : Create and Train Data with Training,validation sets"
    network = gl.deeplearning.create(training_data, target='Class')
    classifier = gl.neuralnet_classifier.create(training_data,
                                                target='Class',
                                                network=network,
                                                validation_set=validation_data,
                                                metric=['accuracy', 'recall@2'],
                                                max_iterations=nmbr_iter)
    return classifier


def classify_and_save(classifier, test_data):
    print "step 5 : Classify Data with Test Set"
    # classify the test set and print predict
    pred = classifier.classify(test_data)
    print pred
    # Save to file
    if not os.path.exists('data'):
        os.makedirs('data')
    pred.save('data/training_data.json', format='json')


def main():
    provider = Provider()
    if os.path.exists(testset) == False:
        provider.init(facesFolder)
        provider.split_data(testset)
    extract_faces_from_images()
    images_array = load_images_in_frame()
    print gl.Sketch(images_array['Class'])
    test_data, training_data, validation_data = split_images_array(images_array)
    classifier = train_network(training_data, validation_data,100)
    classify_and_save(classifier, test_data)
    print "Evaluation" + classifier.evaluate(test_data)
    #TODO: for face unique photos : sugg 1 : make an algo that browse in net for others imgs (hard but more points)
    #TODO                           sugg 2 : copy/past the same img in test data (easy but not effiecent)



if __name__ == '__main__':
    main()
