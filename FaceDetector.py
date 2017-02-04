import cv2
import os


class FaceDetector:
    @staticmethod
    def get_face_from_image(imagePath, cascPath):
        # Create the har cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        # Read the image
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30),
                                             flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        print("Found {0} faces!".format(len(faces)))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            crop_img = image[y: y + h, x: x + w]
        if len(faces) != 0:
            return crop_img
        return None

    # run once for extract faces from photos and save them in /faces for simple load in SFrame
    @staticmethod
    def face_extractor(imgsdir, cascPath, facesFolder):
        if os.listdir(facesFolder):
            return
        print("It can be a problem if the algorithm detect more or less than one Face!")
        # if the folder doesn't exist we just create it
        if not os.path.exists(facesFolder):
            os.makedirs(facesFolder)
        subdirs = [x[0] for x in os.walk(imgsdir)]

        for subdir in subdirs:
            files = os.walk(subdir).next()[2]
            if len(files) > 0:
                for file in files:
                    if file != '.DS_Store' and file != '':
                        pathimg = subdir + "/" + file
                        crop_img = FaceDetector.get_face_from_image(pathimg, cascPath)
                        if crop_img is not None:
                            imgNameSpliting = pathimg.split('/')
                            faceName = imgNameSpliting[len(imgNameSpliting) - 1]
                            print facesFolder
                            cv2.imwrite(os.path.join(facesFolder, faceName), crop_img)
                        else:
                            print "Face Null => can't be save "

    @staticmethod
    def face_extractor_google(images_google, cascPath, facesFolder):
        if os.listdir(facesFolder):
            return
        for (dirpath, dirnames, filenames) in os.walk(images_google):
            for filename in filenames:
                if len(filename) > 0:
                    pathimg = images_google + '/' + filename
                    crop_img = None
                    try:
                        crop_img = FaceDetector.get_face_from_image(pathimg, cascPath)
                    except:
                        print "Can't load the image: path wrong"
                    if crop_img is not None:
                        imgNameSpliting = pathimg.split('/')
                        faceName = imgNameSpliting[len(imgNameSpliting) - 1]
                        cv2.imwrite(os.path.join(facesFolder, faceName), crop_img)
                    else:
                        print "Face Null => can't be save "
