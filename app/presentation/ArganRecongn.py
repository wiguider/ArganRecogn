import os
import graphlab as gl
from app.ui.QDataViewer import *
from app.helpers.DataLoadUtils import DataLoaderUtils as DAL


class ArganRecogn:
    def __init__(self, config, classifier_path, absolute_path):
        # Paths
        self.absolute_path = absolute_path
        self.data_loader = DAL()
        self.classifier_path = classifier_path
        self.config = config
        self.config.read(absolute_path + '/config.ini')
        self.testset = absolute_path + config.get('Paths', 'testset')
        self.facesFolder = self.absolute_path + self.config.get('Paths', 'facesFolder')
        self.facesFolderTest = self.absolute_path + self.config.get('Paths', 'facesFolderTest')
        self.cascPath = self.absolute_path + self.config.get('Paths', 'cascPath')
        self.images_google = self.absolute_path + self.config.get('Paths', 'images_google')

        # Network properties
        self.max_iterations = config.get('Net', 'max_iterations')
        self.target = config.get('Net', 'target')
        self.metric = config.get('Net', 'metric').split(',')

    def split_images_array(self, images_array):
        print "step 3 : Splitting the Data to Training set, Validation and Test Sets"
        try:
            # Creating test samples
            test_data = self.data_loader.load_images(self.testset)
            # Creating training samples
            training_data, validation_data = images_array.random_split(0.8)
            # make sure that all faces have the same size
            training_data['image'] = gl.image_analysis.resize(training_data['image'], 50, 50, 1, decode=True)
            validation_data['image'] = gl.image_analysis.resize(validation_data['image'], 50, 50, 1, decode=True)
            test_data['image'] = gl.image_analysis.resize(test_data['image'], 50, 50, 1, decode=True)
            return test_data, training_data, validation_data
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    def load_classifier(self):
        try:
            if os.path.exists(self.classifier_path):
                print "> load_classifier"
                classifier = gl.load_model(self.classifier_path)
                return classifier
        except Exception as e:
            print "ERROR : load_classifier"
            print e.message
            QDataViewer.show_alert_dialog(e)

    def get_classifier_network(self, training_data, validation_data):
        print "step 4 : Create and Train Data with Training,validation sets"
        try:
            network = gl.deeplearning.create(training_data, target=self.target)

            if os.path.exists(self.classifier_path):
                # Loading a trained classifier
                classifier = self.load_classifier()
            else:
                # Creating a new classifier
                classifier = gl.neuralnet_classifier.create(training_data,
                                                            target=self.target,
                                                            network=network,
                                                            validation_set=validation_data,
                                                            metric=self.metric,
                                                            max_iterations=self.max_iterations)
            return classifier, network
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    def classify_images(self, images_array):
        classifier = self.load_classifier()
        classifier.classify(images_array)
        print classifier
        return classifier

    def classify_and_save(self, classifier, test_data):
        print "step 5 : Classify Data with Test Set"
        # classify the test set and print predict
        try:
            pred = classifier.classify(test_data)
            print pred
            # Save to file
            if not os.path.exists(self.absolute_path + '/data'):
                os.makedirs(self.absolute_path + '/data')
            classifier.save(self.classifier_path)
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    def resize_images(self):
        images_array = self.data_loader.load_images(self.facesFolderTest)
        images_array['image'] = gl.image_analysis.resize(images_array['image'], 50, 50, 1, decode=True)
        return images_array

    def evaluate_images(self):
        try:
            images_array = self.resize_images()

            classifier = self.classify_images(images_array)

            eval_ = classifier.evaluate(images_array, metric=['accuracy', 'recall@2', 'confusion_matrix'])
            return eval_
            # it ll be executed after click on "toSframe" button
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    def learn(self):
        try:
            print 'Number of iterations :', self.max_iterations
            # Downloading Missing Data
            self.data_loader.get_missing_images(self.facesFolder, self.testset, self.images_google)
            # Face Detection
            self.data_loader.extract_faces_from_images(self.facesFolder, self.cascPath, self.images_google)
            # Loading Data
            images_array = self.data_loader.load_images(self.facesFolder)
            print gl.Sketch(images_array['Class'])
            # Splitting Data
            test_data, training_data, validation_data = self.split_images_array(images_array)
            # Network Training
            classifier, network = self.get_classifier_network(training_data, validation_data)
            print classifier
            # Data Classification
            self.classify_and_save(classifier, test_data)
            print "-------------------------------- Evaluation ----------------------------------"
            # Evaluating Classification
            print classifier.evaluate(test_data)
            # Saving the trained classifier
            classifier.save(self.classifier_path)
        except Exception as e:
            QDataViewer.show_alert_dialog(e)
