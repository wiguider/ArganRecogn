import cv2
import os

class FaceDetector:

    @staticmethod
    def  getFaceFromImage(imagePath,cascPath):
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        # Read the image
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=2,minSize=(30, 30),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        print("Found {0} faces!".format(len(faces)))
        ## Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            crop_img = image[y: y + h, x: x + w]
        if len(faces) != 0:
            return crop_img
        return None

    #run once for extract faces from photos and save them in /faces for simple load in SFrame
    @staticmethod
    def faceExtractor(imgsdir,cascPath, facesFolder):
        print("It can be a problem if the algorithm detect more or less than one Face!")
        subdirs = [x[0] for x in os.walk(imgsdir)]
        for subdir in subdirs:
            files = os.walk(subdir).next()[2]
            if (len(files) > 0):
                for file in files:
                    pathimg = subdir + "/" + file
                    crop_img = FaceDetector.getFaceFromImage(pathimg, cascPath)
                    if(crop_img != None):
                        imgNameSpliting = pathimg.split('/')
                        faceName = imgNameSpliting[len(imgNameSpliting) - 1]
                        cv2.imwrite(os.path.join(facesFolder, faceName), crop_img)
                    else:
                        print "Face Null => can't be save "