
from views.LogView import LogView


views = None
def init(root):
    global views
    views = LogView(root)
    views.print("Welcome to VFT report reader!")
def n(text):
    try:
        views.print(text, "n")
    except:
        print(text)
def e(text):
    try:
        views.print(text, "e")
    except:
        print(text)

