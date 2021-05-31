
from views.ReportEditView import ReportEditView

class ReportEditControl:
    def __init__(self, root):
        self.root = root
        
    def startActivity(self):
        self.views = ReportEditView(self, self.root)

    def back(self):
        try:
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()
        except:
            from WelcomeControl import WelcomeControl
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()

