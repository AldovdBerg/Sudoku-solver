#Kivy used for interface

import cv2 #install opencv for camera to work
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
# set interface dimensions
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# imports for old Main
import os
from Resources import *
import Solver
import argparse

class MainApp(App): #@Aldo van der Berg
    def build(self):

        #Add layout to witch components are added
        global layout
        layout = FloatLayout(size=(360, 640))

        #background image
        back = Image(source='Resources/Background_Image.jpg',
                            pos=layout.pos,
                            size=layout.size)
        layout.add_widget(back)

        #label on top with name
        lblApp = Label(text='Sudoku Solver',
                       size_hint=(.5, .5),
                       pos_hint={'center_x': 0.5, 'center_y': 0.94},
                       color=(0.24,0.24,0.24,1))
        layout.add_widget(lblApp)

        #button for solving sudoku
        global btnSolve
        btnSolve = Button(text='Solve',
                          size_hint=(.4, .08),
                          pos_hint={'center_x': 0.5, 'y': 0.18},
                          disabled= True)
        btnSolve.bind(on_press=self.solve_press)
        layout.add_widget(btnSolve)

        #Exit button
        btnExit = Button(text='Exit',
                          size_hint=(.4, .08),
                          pos_hint={'center_x': 0.5, 'y': 0.05})
        btnExit.bind(on_press=self.exit_press)
        layout.add_widget(btnExit)

        #info button
        btnInfo = Button(text='i',
                         color=(0.24,0.24,0.24,1),
                         size_hint=(0.03,0.03),
                         pos_hint={'x': 0.06, 'y': 0.92},
                         background_normal='')
        btnInfo.bind(on_press=self.info_press)
        layout.add_widget(btnInfo)

        #info label
        global lblInfo
        lblInfo = Button(text='Hello. \n'
                             'This Sudoku Solver was made for our \nCMPG311 AI Project.\n'
                             'To use the app, take a picture of your \nSudoku puzzle.\n'
                             'The Solve button should the apper.\n'
                             'To activate the camera press the camera \nbutton again and take a new image.\n'
                             'Make sure the puzzle is clear and readable.\n\n'
                             'Our Team:\n'
                             'Aldo van der Berg(Team Leader)\n'
                             'Shimi Philemon Mashishi\n'
                             'Tarryn Collins\n'
                             'Obelya Fourie\n'
                             'Christoph Snell\n'
                             'Kyle Kumm\n'
                             'Johan Michael Lourens\n'
                             'Randall Traz Mocke',
                       size_hint=(.9, .6),
                       pos_hint={'x': 0.05, 'y': 0.39},
                       color=(0.24, 0.24, 0.35, 1))
        lblInfo.bind(on_press=self.infoClose_press)

        #image for displaying answer
        self.imgResult = Image(source='Resources/Answer.jpg',
                          size_hint=(0.75,0.75),
                          pos_hint={'x': 0.135, 'y': .245})

        #camera interface with image
        self.cameraObject=Camera(play=True,
                                 index=0,
                                 pos_hint={'x': 0, 'y': .12})
        layout.add_widget(self.cameraObject)

        #button that turns camera on and off
        self.camaraClick = Button(text="Capture Soduko",
                                  size_hint = (.4, .08),
                                  background_color=(0.24,0.7,0.44,1),
                                  pos_hint = {'center_x': 0.5, 'y': 0.28})
        self.camaraClick.bind(on_press=self.onCameraClick)
        layout.add_widget(self.camaraClick)

        #camer on or off
        self.take = True

        #answer display var
        self.dis=False

        return layout

    #button event that solves sudoku
    def solve_press(self,instance):
        print('button click')

        ####
        imgHeight = 450
        imgWidth = 450
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", default='Resources/puzzle.jpg', help="Path to input image")
        args = vars(ap.parse_args())
        model = intializePredectionModel()  # for cnn model
        ####

        ## 1. Image prep, @Tarryn Collins
        image = cv2.imread(args["image"])
        image = cv2.resize(image, (imgWidth, imgHeight))
        # Resizing image to a square image
        blankImg = np.zeros((imgHeight, imgWidth, 3), np.uint8)
        # Creating a blank image for testing
        tresholdImg = preProcess(image)

        ## 2. Find contours, @Tarryn Collins
        imageContours = image.copy()
        # Copying image for display
        imageBigContour = image.copy()
        contours, hierarchy = cv2.findContours(tresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Find contours
        cv2.drawContours(imageContours, contours, -1, (0, 255, 0), 3)

        ## 3. Biggest contour = soduko, @Christoph Snell
        biggest, areaMax = biggestContour(contours)
        if biggest.size != 0:
            biggest = reorder(biggest)
            cv2.drawContours(imageBigContour, biggest, -1, (0, 0, 255), 25)  # DRAW THE BIGGEST CONTOUR
            points1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
            points2 = np.float32(
                [[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])  # PREPARE POINTS FOR WARP
            theMatrix = cv2.getPerspectiveTransform(points1, points2)  # GER
            imageWarpColored = cv2.warpPerspective(image, theMatrix, (imgWidth, imgHeight))
            imageDetectedDigits = blankImg.copy()
            imageWarpColored = cv2.cvtColor(imageWarpColored, cv2.COLOR_BGR2GRAY)

            ## 4. Find digits, @Shimi Philemon Mashishi
            imageSolveDigits = blankImg.copy()
            box = splitBoxes(imageWarpColored)
            num = getPrediction(box, model)
            imageDetectedDigits = displayNumbers(imageDetectedDigits, num, color=(255, 0, 255))
            num = np.asarray(num)
            arrayPos = np.where(num > 0, 0, 1)

            ## 5. Solve, @Kyle Kumm
            board = np.array_split(num, 9)  ##Numbers variable coming from #4
            try:
                Solver.solve(board)
            except:
                pass
            flatList = []
            for sublist in board:
                for item in sublist:
                    flatList.append(item)
            solvedNumbers = flatList * arrayPos  # arrayPos coming from #4 #
            imgSolvedDigits = displayNumbers(imageSolveDigits, solvedNumbers)

            ## 6. Display solution, @Randall Traz Mocke
            # only temporary decoding, can still update and improve
            # preparing the points for the warp both point 1 and 2
            points2 = np.float32(biggest)  # PREPARE POINTS FOR WARP
            points1 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
            # Transforming the matrix with the points
            theMatrix = cv2.getPerspectiveTransform(points1, points2)
            # Copying the image and adding the digits to imageInvertWarpColored
            imageInvertWarpColored = image.copy()
            imageInvertWarpColored = cv2.warpPerspective(imgSolvedDigits, theMatrix, (imgWidth, imgHeight))
            invertPerspective = cv2.addWeighted(imageInvertWarpColored, 1, image, 0.5, 1)
            # drawing the digits onto the image
            imageDetectedDigits = drawGrid(image)
            imgSolvedDigits = drawGrid(imgSolvedDigits)
            # outputting the solved sodoku
            #cv2.imshow('Output', invertPerspective) (old)
            cv2.imwrite('Resources/Answer.jpg', invertPerspective)

            self.imgResult.source='Resources/Answer.jpg'
            self.imgResult.reload()
            layout.add_widget(self.imgResult)
            self.dis=True

        else:
            print("No Sudoku Puzzle Found!")

        cv2.waitKey(0)

    #button event to exit app
    def exit_press(self,instance):
        quit()

    #button event for info
    def info_press(self,instance):
        layout.add_widget(lblInfo)

    #closes info label
    def infoClose_press(self,instance):
        layout.remove_widget(lblInfo)

    #button event that turns camera on and off
    def onCameraClick(self, *args):
        #if camera on turn off
        if (self.take):
            self.cameraObject.export_to_png('./Resources/puzzle.jpg')
            self.cameraObject.play = False
            self.take = False
            btnSolve.disabled = False
            self.camaraClick.background_color = (1, 0, 0, 1)
        # if camera off turn on
        else:
            self.cameraObject.play = True
            self.take = 1
            btnSolve.disabled = True
            self.camaraClick.background_color = (0.24, 0.7, 0.44, 1)
            # remove answer
            if (self.dis):
                layout.remove_widget(self.imgResult)
                self.dis = False


if __name__ == '__main__':
    app = MainApp()
    app.run()