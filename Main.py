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
biggest, maxArea = biggestContour(contours) 
if biggest.size != 0:
    biggest = reorder(biggest)
    cv2.drawContours(imageBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
    points1 = np.float32(biggest) # PREPARE POINTS FOR WARP
    points2 = np.float32([[0, 0],[imgWidth, 0], [0, imgHeight],[imgWidth, imgHeight]]) # PREPARE POINTS FOR WARP
    theMatrix = cv2.getPerspectiveTransform(points1, points2) # GER
    imageWarpColored = cv2.warpPerspective(image, theMatrix, (imgWidth, imgHeight))
    imageDetectedDigits = blankImg.copy()
    imageWarpColored = cv2.cvtColor(imageWarpColored,cv2.COLOR_BGR2GRAY)


  ## 4. Find digits, @Shimi Philemon Mashishi
  
  
  
  ## 5. Solve, @Kyle Kumm
  board = np.array_split(numbers,9) # Numbers variable coming from #4 #
    try:
        Solver.solve(board)
    except:
        pass
    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers =flatList*posArray # posArray coming from #4 #
    imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)
  
  
  ## 6. Display solution, @Randall Traz Mocke



