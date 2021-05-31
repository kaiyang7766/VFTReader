
from views.WelcomeView import WelcomeView

class WelcomeControl:
    def __init__(self, root):
        self.root = root

    def startActivity(self):
        self.view = WelcomeView(self.root, self)
        
    def extract(self, filepath):
        pass
    
    def onNextActivity():
        pass
    

    
        