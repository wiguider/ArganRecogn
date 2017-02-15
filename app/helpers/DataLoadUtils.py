import os
import graphlab as gl
from app.helpers.FaceDetector import FaceDetector as fd
from app.ui.QDataViewer import *


class DataLoaderUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_missing_images(faces_folder, test_set, images_google):

        try:
            provider = DataProvider(faces_folder)
            provider.split_data(test_set)
            provider.download_missing_images(images_google)
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    @staticmethod
    def extract_faces_from_images(faces_folder, cascade_path, images_directory):
        print "step 1 : DONE ONLY ONCE : Extract Faces from images and put in a dictionary " \
              "<label:name_of_face, value:path_to_face>, the dict is optionally"
        try:
            fd.face_extractor(images_directory, cascade_path, faces_folder)
            fd.face_extractor_google(images_directory, cascade_path, faces_folder)
        except Exception as e:
            QDataViewer.show_alert_dialog(e)

    @staticmethod
    def get_face_from_image(image_path, cascade_path):
        return fd.get_face_from_image(image_path, cascade_path)

    @staticmethod
    def load_images(folder):
        print "step 2 : Load the faces in a Frame : <Image_brut,Its_Class>"
        # load_images return an SFrame :  path |   image
        try:
            images_array = gl.image_analysis.load_images(folder,
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
