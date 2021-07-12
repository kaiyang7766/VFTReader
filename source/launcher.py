from control.WelcomeControl import WelcomeControl
from tkinter import Frame, Tk
import Constants
from Log import Log
class Launcher:
    """Launcher class for the application

    Attributes:
        mainWindow: The window to contain the main application.
        logWindow: The window to contain the logs feature.
        mainFrame: The frame to contain the UI elements for the main application. This frame is to be destroyed when moving to a new application.
    """
    def main(self):
        """initializes all windows to contain the application, and start the welcome activity.
        """
        self.mainWindow = Tk(className= Constants.PROJECT_NAME)
        self.mainWindow.geometry("1000x600+200+200")
        self.logWindow = Tk(className= Constants.LOG_WINDOW_NAME)
        self.logWindow.geometry("500x200+800+400")

        main = WelcomeControl(self.mainWindow)
        main.startActivity()
        Log(self.logWindow)

        self.mainWindow.mainloop()
        self.logWindow.mainloop()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.main()