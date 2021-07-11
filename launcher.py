from control.WelcomeControl import WelcomeControl
from tkinter import Tk
import Constants
import Log
class Launcher:
    def main(self):
        self.main_window = Tk(className= Constants.PROJECT_NAME)
        self.main_window.geometry("1000x600+200+200")

        self.log_window = Tk(className= Constants.LOG_WINDOW_NAME)
        self.log_window.geometry("500x200+800+400")

        main = WelcomeControl(self.main_window)
        main.startActivity()
        Log.init(self.log_window)

        self.main_window.mainloop()
        self.log_window.mainloop()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.main()