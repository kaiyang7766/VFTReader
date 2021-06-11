
from views.LogView import LogView


views = None
def init(root):
    global views
    views = LogView(root)
    views.print("Welcome to VFT report reader!")
def n(text):
    views.print(text + "\n", "n")
    views.update()
    
def e(text):
    views.print(text + "\n", "e")

