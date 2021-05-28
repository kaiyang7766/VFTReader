from tkinter import Tk
import Constants
from WelcomeView import WelcomeView
from LogView import *

main_window = Tk(className= Constants.PROJECT_NAME)
main_window.geometry("1000x600+200+200")
main_window.resizable(False, False)
log_window = Tk(className= Constants.LOG_WINDOW_NAME)
log_window.geometry("500x200+800+400")

WelcomeView(main_window)
LogView(log_window)

main_window.mainloop()
log_window.mainloop()