import cv2
import numpy as np
from tensorflow.keras.models import load_model


## Get model weight
def intializePredectionModel():
    model = load_model('Resources/myModel.h5')
    return model

## 1. Process image,, @Tarryn Collins
def preProcess(img):
    grayImage = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Converting image to gray scale
    blurImage = cv2.GaussianBlur(grayImage, (5, 5), 1)
    #Adding gaussian blur
    tresholdImg = cv2.adaptiveThreshold(blurImage, 255, 1, 1, 11, 2)
    #Applying adaptive treshold
    return tresholdImg



## 2. Warp points correctly, #Christoph Snell
def reorder(points):
    points = points.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    pointsNew[0] = points[np.argmin(add)]
    pointsNew[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    pointsNew[1] = points[np.argmin(diff)]
    pointsNew[2] = points[np.argmax(diff)]
    return pointsNew



## 3. Find biggest countour = soduko, @Christoph Snell
def biggestContour(countours):
    biggest = np.array([])
    max_area = 0
    for r in countours:
        area = cv2.contourArea(r)
        if area > 50:
            peri = cv2.arcLength(r, True)
            approx = cv2.approxPolyDP(r, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area



## 4. Split into 81 images, @Obelya Fourie
def splitBoxes(img):
    rows = np.vsplit(img,9)
    boxes = []
    for i in rows:
        columns = np.hsplit(i,9)
        for box in columns:
            boxes.append(box)
    return boxes


## 5. Image predictions, @Johan Michael Lourens
def getPrediction(boxes, model):
    result = []
    for image in boxes:
        ## PREPARE IMAGE
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        ## GET PREDICTION
        predictions = model.predict(img)
        classIndex = np.argmax(model.predict(img), axis=-1) #<--- Had to edit this as predict_classes was removed from the libraries
        probabilityValue = np.amax(predictions)
        ## SAVE TO RESULT
        if probabilityValue > 0.8:
            result.append(classIndex[0])
        else:
            result.append(0)
    return result


## 6.  Dislpay solution, @Obelya Fourie
def displayNumbers(img,nums,color = (0,255,0)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    print(nums)
    for m in range (0,9):
        for n in range (0,9):
            if nums[(n*9)+m] != 0 :
                cv2.putText(img, str(nums[(n*9)+m]),
                            (m*secW+int(secW/2)-10, int((n+0.8)*secH)),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv2.LINE_AA)
    return img


## 7. Grid drwaing for warp, @Randall Traz Mocke
#must decode abit further
def drawGrid(img):
    #getting the sections width and their heights
    sectionWidth = int(img.shape[1] / 9)
    sectionHeight = int(img.shape[0] / 9)
    for i in range(0, 9):
        point1 = (0, sectionHeight * i)
        point2 = (img.shape[1], sectionHeight * i)
        point3 = (sectionWidth * i, 0)
        point4 = (sectionHeight * i, img.shape[0])
        cv2.line(img, point1, point2, (255, 255, 0), 2)
        cv2.line(img, point3, point4, (255, 255, 0), 2)
    return img
  
