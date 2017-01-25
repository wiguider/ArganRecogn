################################################################################>>>>>>
# 1 Define the problem
# 2 Prepare Data:
#               *Loading Data
#                       Loop all the training set<image> and Store the dected Face in SequenceFile: Succo : <nameofFolder=>nameofImage,Img => Face >
#               *Summarizing Data
#               *Visualizing Data
#		*Estrarne le caratteristiche
# 3 Evaluate Algorithms and Models
#                       Train the set of faces with diffrent Models : NN,.... based on Accurancy (for me, only )
# 4 Make some Predictions(i will stop here) and Improve Results
#                       Test the Test-img-set with calculating accurancy
# 5 Present Results
##################################################################################>>>>>

import graphlab as gl
import os
from docutils.nodes import image
from FaceDetector import FaceDetector as fd

# Get user supplied values
path = "/home/ilyas/Desktop/FaceRecognrtionDeepLearning/FaceRecogn/"
cascPath = path + "haarcascade_frontalface_default.xml"
facesFolder = path+"faces/"
facesFolderTest = path+"Test/"
imgsdir = "/home/ilyas/Dropbox/lfw"


def main():

    print "step 2 : DO IT ONECE : Extract Faces from images and put in a dictionary <label:name_of_face, value:path_to_face>, the dict is optionally"
    #extact all faces from images <do it just for the first time> : Done
    if os.path.exists(facesFolder) == False:
        fd.faceExtractor(imgsdir,cascPath, facesFolder)
    print "step 2 : Load the faces in a Frame : <Image_brut,Its_Class>"
    #load_images return an SFram :  path |   image
    image_sarray =  gl.image_analysis.load_images(facesFolder, "auto", with_path=True,recursive = True,ignore_failure=True)
    classes = []
    for element in image_sarray['path']:
        classes.append(getMyClass(element))
    #Columns :  path |   image | Class
    image_sarray.add_column(gl.SArray(data=classes), name='Class')
    image_sarray.remove_column('path')
    print "step 2 : Spliting the Data to Traing set, Validation and Test Sets"

    dataset, test_data = image_sarray.random_split(0.75)
    training_data, validation_data = dataset.random_split(0.8)
    # make sure that all faces have the same size
    training_data['image'] = gl.image_analysis.resize(training_data['image'], 50, 50, 1, decode=True)
    validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 50, 50, 1, decode=True)
    test_data['image'] = gl.image_analysis.resize(test_data['image'], 50, 50, 1, decode=True)
    print "step 2 : Summerizing data  "
    sketch = gl.Sketch(image_sarray['Class'])
    print sketch
    print "step 2 : Data Visualizing"
    training_data['image'].show()


    print "step 3 : Create and Train Data with Training,validation sets"
    net = gl.deeplearning.create(training_data, target='Class')
    m = gl.neuralnet_classifier.create(training_data, target='Class', network=net, validation_set=validation_data,metric=['accuracy', 'recall@2'], max_iterations=10)
    net.save("MyNet")


    print "step 4 : Classify Data with Test Set"
    # classify the test set and print predict
    #pred = m.classify(test_data)
    pred = m.classify(training_data)
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
