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

# Get user supplied values
config =ConfigParser.ConfigParser()
config.read('config.ini')
path = config.get('Paths','path')
cascPath = config.get('Paths','cascPath')
facesFolder = config.get('Paths','facesFolder')
facesFolderTest = config.get('Paths','facesFolderTest')
imgsdir = config.get('Paths','imgsdir')



def main():
    #TODO : integrate this step in the main procesus
    print "step 1 : DO IT ONECE : Extract Faces from images and put in a dictionary <label:name_of_face, value:path_to_face>, the dict is optionally"
    #extact all faces from images <do it just for the first time> : Done
    #fd.faceExtractor(imgsdir,cascPath, facesFolder)

    print "step 2 : Load the faces in a Frame : <Image_brut,Its_Class>"
    #load_images return an SFram :  path |   image
    image_sarray =  gl.image_analysis.load_images(facesFolder, "auto", with_path=True,recursive = True,ignore_failure=True)
    classes = []
    for element in image_sarray['path']:
        classes.append(getMyClass(element))
    #Columns :  path |   image | Class
    image_sarray.add_column(gl.SArray(data=classes), name='Class')
    image_sarray.remove_column('path')

    print "step 3 : Spliting the Data to Traing set, Validation and Test Sets"
    dataset, test_data = image_sarray.random_split(0.75)
    training_data, validation_data = dataset.random_split(0.8)
    # make sure that all faces have the same size
    training_data['image'] = gl.image_analysis.resize(training_data['image'], 110, 110, 1, decode=True)
    validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 110, 110, 1, decode=True)

    print "step 4 : Create and Train Data with Training,validation sets"
    # create my NN
    net = gl.deeplearning.create(training_data, target='Class')
    # Train NN
    m = gl.neuralnet_classifier.create(training_data, target='Class', network=net, validation_set=validation_data,metric=['accuracy', 'recall@2'], max_iterations=3)

    print "step 5 : Classify Data with Test Set"
    # classify the test set and print predict
    pred = m.classify(test_data)
    print pred

#TODO : make the main clean : put this method in amother class
def getMyClass(elment_path):
    list_split_strings = elment_path.split('/')
    faceName = list_split_strings[len(list_split_strings) - 1]
    imgNameClass = faceName.split('0')
    imgClass = imgNameClass[0]
    return imgClass

if __name__ == '__main__':
      main()