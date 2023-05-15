import cv2 #install opencv for camera to work
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.camera import Camera
from kivy.uix.image import Image
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

class MainApp(App):
    def build(self):
        layout = FloatLayout(size=(360, 640))

        #background image
        back = Image(source='Background_Image.jpg',
                            pos=layout.pos,
                            size=layout.size)
        layout.add_widget(back)

        #label on top with name
        lblApp = Label(text='Sudoku Solver',
                       size_hint=(.5, .5),
                       pos_hint={'center_x': 0.5, 'center_y': 0.92},
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
                         pos_hint={'x': 0.05, 'y': 0.92},
                         background_normal='')
        btnInfo.bind(on_press=self.info_press)
        layout.add_widget(btnInfo)

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

        self.take = 1

        return layout

    #button event that solves sudoku
    def solve_press(self,instance):
        print('button click')

    #button event to exit app
    def exit_press(self,instance):
        quit()

    #button event for info
    def info_press(self,instance):
        print('info')

    #button event that turns camera on and off
    def onCameraClick(self, *args):
        #if camera off turn on
        if (self.take == 0):
            self.cameraObject.play=True
            self.take=1
            btnSolve.disabled=True
            self.camaraClick.background_color=(0.24,0.7,0.44,1)
        #if camera on turn off
        else:
            self.cameraObject.export_to_png('./puzzle.png')
            self.cameraObject.play=False
            self.take=0
            btnSolve.disabled=False
            self.camaraClick.background_color=(1,0,0,1)


if __name__ == '__main__':
    app = MainApp()
    app.run()
