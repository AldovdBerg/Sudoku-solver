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



## 2. Find contours, @Tarryn Collins



## 3. Biggest contour = soduko, @Christoph Snell



  ## 4. Find digits, @Shimi Philemon Mashishi
  
  
  
  ## 5. Solve, @Kyle Kumm
  
  
  
  ## 6. Display solution, @Randall Traz Mocke



