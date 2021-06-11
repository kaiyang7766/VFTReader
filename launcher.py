from WelcomeControl import WelcomeControl
from tkinter import Tk
import Constants
from WelcomeControl import WelcomeControl
import Log

main_window = Tk(className= Constants.PROJECT_NAME)
main_window.geometry("1000x600+200+200")

log_window = Tk(className= Constants.LOG_WINDOW_NAME)
log_window.geometry("500x200+800+400")

main = WelcomeControl(main_window)
main.startActivity()
Log.init(log_window)

main_window.mainloop()
log_window.mainloop()