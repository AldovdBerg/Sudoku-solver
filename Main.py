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



## 1. Image prep



## 2. Find contours


## 3. Biggest contour = soduko


  ## 4. Find digits
  
  
  ## 5. Solve
  
  
  ## 6. Display solution



