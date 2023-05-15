import os
from Resources import *
import Solver
import argparse

####
imgHeight = 450
imgWidth = 450
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default = 'Folder/1.jpg', help = "Path to input image")
args = vars(ap.parse_args())
model = initializePredectionModel()  #for cnn model
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
cv2.drawContours(imageContours, contours, -1, (0, 255, 0),3)


## 3. Biggest contour = soduko, @Christoph Snell
biggest, areaMax = biggestContour(contours) 
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
    imageSolveDigits = blankImg.copy()
    box = splitBoxes(imageWarpColored)
    num = getPredection(box, model)
    imageDetectedDigits = displayNumbers(imageDetectedDigits, num, color = (255, 0, 255))
    num = np.asarray(num)
    arrayPos = np.where(num > 0, 0, 1)


  
  
  ## 5. Solve, @Kyle Kumm
  board = np.array_split(num,9) # Numbers variable coming from #4 #
    try:
        Solver.solve(board)
    except:
        pass
    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers =flatList*arrayPos # arrayPos coming from #4 #
    imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)
  
  
  ## 6. Display solution, @Randall Traz Mocke
      #only temporary decoding, can still update and improve
    #preparing the points for the warp both point 1 and 2
    points2 = np.float32(biggest) # PREPARE POINTS FOR WARP
    points1 =  np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])
    #Transforming the matrix with the points
    theMatrix = cv2.getPerspectiveTransform(points1,points2)
    #Copying the image and adding the digits to imageInvertWarpColored
    imageInvertWarpColored = image.copy()
    imageInvertWarpColored = cv2.warpPerspective(imgSolvedDigits, theMatrix, (imgWidth, imgHeight))
    invertPerspective = cv2.addWeighted(imageInvertWarpColored, 1, image, 0.5, 1)
    #drawing the digits onto the image
    imageDetectedDigits = drawGrid(image)
    imgSolvedDigits = drawGrid(imgSolvedDigits)
    #outputing the solved sodoku
    cv2.imshow('Output', invertPerspective)

else:
    print("No Sudoku Puzzle Found!")
    
cv2.waitKey(0)

