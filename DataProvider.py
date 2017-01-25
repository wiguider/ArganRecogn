from os import walk
from os import path
import shutil


class Provider:
    all_images = []
    face_nbrImage = dict()
    faces_path = None

    def init(self,faces_path):
        self.faces_path = faces_path
        for (dirpath, dirnames, filenames) in walk(self.faces_path):
            self.all_images.extend(filenames)
            break

    def split_data(self,testset):
        #counting face <-> number of this face
        for image in self.all_images:
            face_name = Provider.get_face_name(image)
            if self.face_nbrImage.__contains__(face_name):
                self.face_nbrImage[face_name] += 1
            else:
                self.face_nbrImage[face_name] = 1
        #create test_dataset from faces with value > 2
        for face in self.face_nbrImage:
            if self.face_nbrImage[face] > 1:
                for image in self.all_images:
                    if face == Provider.get_face_name(image):
                        suffix = Provider.get_face_name(image) + "0001.jpg"
                        if path.exists(self.faces_path + suffix):
                            shutil.move(self.faces_path + suffix, testset + suffix)



    @staticmethod
    def get_face_name(element_path):
        list_split_strings = element_path.split('/')
        face_name_num = list_split_strings[len(list_split_strings) - 1]
        face_name_arr = face_name_num.split('0')
        return face_name_arr[0]