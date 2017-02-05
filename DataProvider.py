import shutil
from os import walk
from os import path
from ImageProvider import ImageProvider


class Provider:
    all_images = []
    face_nbrImage = dict()
    faces_path = None
    oneListPersons = []

    def __init__(self, faces_path=""):
        self.faces_path = faces_path
        for (dirpath, dirnames, filenames) in walk(self.faces_path):
            self.all_images.extend(filenames)
            break
        # counting face <-> number of this face
        for image in self.all_images:
            face_name = Provider.get_face_name(image)
            if face_name in self.face_nbrImage.keys():
                self.face_nbrImage[face_name] += 1
            else:
                self.face_nbrImage[face_name] = 1
        # create one persons list
        for face in self.face_nbrImage.keys():
            if self.face_nbrImage[face] == 1:
                l = [face]
                self.oneListPersons.append(l)
        print "Number of people with more than image  :" + str(len(self.face_nbrImage.keys()))
        print "Number of people with one image  :" + str(len(self.oneListPersons))

    def split_data(self, testset):
        # create test_dataset from faces with value > 1 => move image.001 in dataset
        if not path.exists(testset):
            for face in self.face_nbrImage:
                if self.face_nbrImage[face] > 1:
                    for image in self.all_images:
                        nom = Provider.get_face_name(image)
                        if face == nom:
                            suffix = nom + "0001.jpg"
                            if path.exists(self.faces_path + suffix):
                                shutil.move(self.faces_path + suffix, testset + suffix)
                            else:
                                print "Image Already exist in TestSet"
                                # 203 person had only one image => copy the unique image.001 in dataset
            for person in self.oneListPersons:
                suffix = person[0] + "0001.jpg"
                if path.exists(self.faces_path + suffix):
                    shutil.copy(self.faces_path + suffix, testset + suffix)

    def download_missing_images(self, images_google):
        if not path.exists(images_google):
            for l in self.oneListPersons:
                ImageProvider().get_images_from_google(l, 3)

    @staticmethod
    def get_face_name(element_path):
        list_split_strings = element_path.split('/')
        face_name_num = list_split_strings[len(list_split_strings) - 1]
        face_name_arr = face_name_num.split('0')
        return face_name_arr[0][:-1]
