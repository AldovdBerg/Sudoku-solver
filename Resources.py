import cv3
import numphy as np
from tensorflow.keras.models import load_model


## Get model weight
def intializePredectionModel():
    model = load_model('Resources/myModel.h5')
    return model
  
## 1. Process image,, @Tarryn Collins
def preProcess(img):

  
  
## 2. Warp points correctly, #Christoph Snell
def reorder(points):
  
  

## 3. Find biggest countour = soduko, @Christoph Snell
def biggestCountour(countours):
  


## 4. Split into 81 images, @Obelya Fourie
def splitBoxes(img):
               
           

## 5. Image predictions, @Johan Michael Lourens
def getPrediction(boxes, model):
  
  

## 6.  Dislpay solution, @Obelya Fourie
def displayNumbers(img, numbers, color = (0,255,0)):
  
  

## 7. Grid drwaing for warp, @Randall Traz Mocke
def drawGrid(img):
  
  
