
from tkinter import Tk
from views.LogView import LogView

class Log:
    """Control class for the logs feature.

    Attributes:
        views: The UI elements of the logs.
    """
    views = None
    def __init__(self, root: Tk):
        """Initializes the logs activity

        Args:
            root (Tk): The root window for the logs
        """
        Log.views = LogView(root)
        Log.views.print("Welcome to VFT report reader!")
    def n(text: str):
        """Prints a normal line out in the logs window

        Args:
            text (str): Text to be printed
        """
        try:
            Log.views.print(text, "n")
        except:
            print(text)
    def e(text:str):
        """Prints an error line out in the logs window

        Args:
            text (str): Text to be printed
        """
        try:
            Log.views.print(text, "e")
        except:
            print(text)

