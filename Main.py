import os
from Resources import *
import Solver
import argparse

####
imgHeight = 450
imgWidth = 450
ap = argparse.ArgumentParser()
ap.add.argument("-i", "--image", default = 'recorces/1.jpg', help = "Path to input image")
args = vars(ap.parse_args())
model = initializePredectionModel()  #for cnn mode
####



## 1. Image prep, @Tarryn Collins
image = cv2.imread(args["image"])
image = cv2.resize(image, (imgWidth, imgHeight))
#Resizing image to a square image
blankImg = np.zeros((imgHeight, imgWidth,3),np.uint8)
#Creating a blank image for testing
tresholdImg = preProcess(image)


## 2. Find contours, @Tarryn Collins
imageContours = image.copy()
#Copying image for display
imageBigContour = image.copy()
contours, hierarchy = cv2.findContours(tresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#Find contours
cv2.contourDrawing(imageContours, contours, -1, (0, 255, 0),3)


## 3. Biggest contour = soduko, @Christoph Snell



  ## 4. Find digits, @Shimi Philemon Mashishi
  
  
  
  ## 5. Solve, @Kyle Kumm
  
  
  
  ## 6. Display solution, @Randall Traz Mocke



