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
from docutils.nodes import image
from FaceDetector import FaceDetector as fd
import ConfigParser
import os

# Get user supplied values
config = ConfigParser.ConfigParser()
config.read('config.ini')
path = config.get('Paths', 'path')
cascPath = config.get('Paths', 'cascPath')
facesFolder = config.get('Paths', 'facesFolder')
facesFolderTest = config.get('Paths', 'facesFolderTest')
imgsdir = config.get('Paths', 'imgsdir')


# TODO: 1.Crop the face zone # STATUS: DONE
# TODO: 2.Extract the characteristics from the face zone # STATUS: WHICH CHARACTERISTICS ?
# TODO: 3.Compare the characteristics vectors of the probe set samples with the ones of the gallery samples # STATUS: ?

def extract_faces_from_images():
    print "step 1 : DONE ONLY ONCE : Extract Faces from images and put in a dictionary " \
          "<label:name_of_face, value:path_to_face>, the dict is optionally"
    # extract all faces from images <do it just for the first time> : Done
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
        classes.append(get_face_name(element))
    # Columns :  path |   image | Class
    images_array.add_column(gl.SArray(data=classes), name='Class')
    images_array.remove_column('path')
    return images_array


def split_images_array(images_array):
    print "step 3 : Spliting the Data to Traing set, Validation and Test Sets"
    # Creating test samples
    dataset, test_data = images_array.random_split(0.75)
    # Creating training samples
    training_data, validation_data = dataset.random_split(0.8)
    # make sure that all faces have the same size
    training_data['image'] = gl.image_analysis.resize(training_data['image'], 110, 110, 1, decode=True)
    validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 110, 110, 1, decode=True)
    return dataset, test_data, training_data, validation_data


def train_network(training_data, validation_data):
    print "step 4 : Create and Train Data with Training,validation sets"
    network = gl.deeplearning.create(training_data, target='Class')
    classifier = gl.neuralnet_classifier.create(training_data,
                                                target='Class',
                                                network=network,
                                                validation_set=validation_data,
                                                metric=['accuracy', 'recall@2'],
                                                max_iterations=3)
    return classifier


# TODO : make the main clean : put this method in another class
def get_face_name(element_path):
    list_split_strings = element_path.split('/')
    face_name_num = list_split_strings[len(list_split_strings) - 1]
    face_name_arr = face_name_num.split('_')
    print face_name_num
    return face_name_arr[0] + ' ' + face_name_arr[1]


def classify_and_save(classifier, test_data):
    print "step 5 : Classify Data with Test Set"
    # classify the test set and print predict
    pred = classifier.classify(test_data)
    # Save to file
    if not os.path.exists('data'):
        os.makedirs('data')
    pred.save('data/training_data.json', format='json')


def main():
    extract_faces_from_images()
    images_array = load_images_in_frame()
    # vis = gl.Sketch(images_array['Class'])
    # print vis
    data_set, test_data, training_data, validation_data = split_images_array(images_array)
    classifier = train_network(training_data, validation_data)
    classify_and_save(classifier, test_data)


if __name__ == '__main__':
    main()
