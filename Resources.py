import cv3
import numphy as np
from tensorflow.keras.models import load_model


## Get model weight
def intializePredectionModel():
    model = load_model('Resources/myModel.h5')
    return model
  
## 1. Process image
def preProcess(img):

  
  
## 2. Warp points correctly
def reorder(points):
  
  

## 3. Find biggest countour = soduko
def biggestCountour(countours):
  


## 4. Split into 81 images
def splitBoxes(img):
               
           

## 5. Image predictions
def getPrediction(boxes, model):
  
  

## 6.  Dislpay solution
def displayNumbers(img, numbers, color = (0,255,0)):
  
  

## 7. Grid drwaing for warp
def drawGrid(img):
  
  
