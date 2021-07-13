from control.WelcomeControl import WelcomeControl
from tkinter import Frame, Tk
import Constants
from control.Log import Log
import pytesseract
class Launcher:
    """Launcher class for the application

    Attributes:
        mainWindow: The window to contain the main application.
        logWindow: The window to contain the logs feature.
        mainFrame: The frame to contain the UI elements for the main application. This frame is to be destroyed when moving to a new application.
    """
    def main(self):
        """Initializes all windows to contain the application, and start the welcome activity.
        """
        pytesseract.pytesseract.tesseract_cmd = Constants.PYTESSERACT_PATH
        self.mainWindow = Tk(className= Constants.PROJECT_NAME)
        self.mainWindow.geometry(Constants.MAIN_WINDOW_GEOMETRY)
        self.logWindow = Tk(className= Constants.LOG_WINDOW_NAME)
        self.logWindow.geometry(Constants.LOG_WINDOW_GEOMETRY)

        main = WelcomeControl(self.mainWindow)
        main.startActivity()
        Log(self.logWindow)

        self.mainWindow.mainloop()
        self.logWindow.mainloop()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.main()