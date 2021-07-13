
from tkinter import *
from tkinter import filedialog
from tkinter.font import families
from typing import Dict, List, Optional

from math import floor


class NumDbGraphView(Frame):
    """Utility class, contains the UI elements for a numeric dB graph.

    Consists of a title, and 76 entry boxes arranged in a shape similar to a numeric dB graph
    """
    def fill(self):
        """Initializes the entry boxes of a numeric dB graph.
        """
        self.entryViews = [[0 for i in range(10)] for j in range(10)]
        self.entryVariables = [[0 for i in range(10)] for j in range(10)]
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    self.entryVariables[i][j] = None
                else:
                     self.entryVariables[i][j] = StringVar()
                     
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    self.entryViews[i][j] = None
                else:
                    self.entryViews[i][j] = Entry(self, textvariable= self.entryVariables[i][j])
                    self.entryViews[i][j].place(relwidth= 0.07, relheight= 0.07, relx =0.03 + 0.1 * j , rely =0.03+ 0.1 * i)
    
    def setTitle(self, title):
        """Sets the name of a graph

        Args:
            title (str): The name of the graph.
        """
        self.title = Label(self, text = title)
        self.title.place(relx = 0, rely = 0)

    def getVariables(self):
        """Retrieve the values in the entry boxes.

        Returns:
            List[List[str]]: A 10 x 10 2D list containing the values.
        """
        result = [[0 for i in range(10)] for j in range(10)]
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    result[i][j] = None
                else:
                    result[i][j] = self.entryVariables[i][j].get()
        return result

    def setVariables(self, new_matrix):
        """Sets the values in the entry boxes with the new values

        Args:
            new_matrix (List[List[str]]): The new values, in a 10 x 10 matrix
        """
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    self.entryVariables[i][j] = None
                elif new_matrix[i][j] == None:
                    self.entryVariables[i][j].set("")
                else:
                    self.entryVariables[i][j].set(str(new_matrix[i][j]))

        
    def showWarning(self,eye,  blindspot):
        """Highlights boxes with potentially wrong values. Currently only highlights empty boxes.

        Args:
            eye (str): The eye side being displayed
            blindspot (bool): Set to false to ignore natural blindspots.

        Returns:
            bool: True if there are at least one wrong/missing value.
        """
        missing = False
        if eye.lower() == "right":
            for i  in range(10):
                for j in range(10):
                    if i + j <=3 or i+j >=15 or i - j >= 6 or j - i >=6 or i == 0 or i == 9 or j == 9:
                        continue
                    elif blindspot:
                        if (i, j) == (4, 7) or (i, j) == (5, 7):
                            self.entryViews[i][j].config(bg = "white")
                            continue
                    if self.entryVariables[i][j].get() == "":
                        self.entryViews[i][j].config(bg = "#FFF284")
                        missing = True
                    else:
                        self.entryViews[i][j].config(bg = "white")
        
        else:
            for i  in range(10):
                for j in range(10):
                    if i + j <=3 or i+j >=15 or i - j >= 6 or j - i >=6 or i == 0 or i == 9 or j == 0:
                        continue
                    elif blindspot:
                        if (i, j) == (4, 2) or (i, j) == (5, 2):
                            self.entryViews[i][j].config(bg = "white")
                            continue
                    if self.entryVariables[i][j].get() == "":
                        self.entryViews[i][j].config(bg = "#FFF284")
                        missing = True
                    else:
                        self.entryViews[i][j].config(bg = "white")
        return missing


class ReportEditView:
    """UI elements for the report viewing and editing activity.
    """
    def __init__(self, control, root) -> None:
        """Initializes the UI elements

        Args:
            control (ReportEditControl): The control of the activity.
            root (): The main application window.
        """
        self.root = root
        self.control = control
        self.main = Frame(self.root)
        self.main.pack(fill = "both", expand= True)

        self.reportSelectionContainer = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.reportSelectionContainer.pack()
        self.reportSelectionContainer.place(relwidth=0.3, relheight=0.5, relx=0, rely=0)

        self.reportSelectionHeader = Label(self.reportSelectionContainer, font = ("Arial", 14), text="Choose a report")
        self.reportSelectionHeader.pack(fill = "x", expand= True, pady=10)
        self.reportSelectionHeader.place(relx = 0.5, anchor = "n")

        self.reportSelectionList = Listbox(self.reportSelectionContainer, exportselection=False)
        self.vsb = Scrollbar(self.reportSelectionList, command=self.reportSelectionList.yview, orient="vertical")
        self.reportSelectionList.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.reportSelectionList, command=self.reportSelectionList.xview, orient="horizontal")
        self.reportSelectionList.configure(yscrollcommand=self.hsb.set)
        self.reportSelectionList.pack(fill = "both", pady= 5)
        self.reportSelectionList.place(relwidth= 1, relheight=0.95, rely = 0.15)
        #TODO: Replace with proper logic
        
        self.reportSelectionList.bind("<<ListboxSelect>>", self.onSelectReport)

        
        self.commitButton = Button(self.main, text = "Commit", command= self.commit)
        self.commitButton.place(anchor = "n",relx= 0.07, rely = 0.6)

        self.loadButton = Button(self.main, text = "Load", command = self.loadStudy)
        self.loadButton.place(anchor = "n",relx= 0.07, rely = 0.65)
        
        self.backButton = Button(self.main, text = "Back", command= self.back)
        self.backButton.place(anchor = "n",relx= 0.23, rely = 0.6)

        self.GHT = StringVar()
        self.GHTFrame = Frame(self.main)
        self.GHTFrame.pack()
        self.GHTFrame.place(relwidth= 0.3, anchor = "n", relx = 0.15, rely = 0.73)
        self.GHTLabel = Label(self.GHTFrame, text = "GHT")
        self.GHTLabel.pack(side = "left", padx=10)
        self.GHTEntry = Entry(self.GHTFrame, textvariable=self.GHT)
        self.GHTEntry.pack(side = "left", fill = 'x', expand = True, padx= 10) 

        self.VFI = StringVar()
        self.VFIFrame = Frame(self.main)
        self.VFIFrame.pack()
        self.VFIFrame.place(relwidth= 0.3, anchor = "n", relx = 0.15, rely = 0.78)
        self.VFILabel = Label(self.VFIFrame, text = "VFI")
        self.VFILabel.pack(side = "left", padx=10)
        self.VFIEntry = Entry(self.VFIFrame, textvariable = self.VFI)
        self.VFIEntry.pack(side = "left", fill = 'x', expand = True, padx= 10) 

        self.MD = StringVar()
        self.MDp = StringVar()
        self.MDFrame = Frame(self.main)
        self.MDFrame.pack()
        self.MDFrame.place(relwidth= 0.3, anchor = "n", relx = 0.15, rely = 0.83)
        self.MDLabel = Label(self.MDFrame, text = "MD")
        self.MDLabel.pack(side = "left", padx=10)
        self.MDEntry = Entry(self.MDFrame, width= 10, textvariable = self.MD)
        self.MDEntry.pack(side = "left", padx= 5) 
        self.MDUnit =  Label(self.MDFrame, text = "dB")
        self.MDUnit.pack(side = "left", padx=5)
        self.MDpvalueEntry = Entry(self.MDFrame, width= 10, textvariable = self.MDp)
        self.MDpvalueEntry.pack(side = "left", padx= 10) 

        self.PSD = StringVar()
        self.PSDp = StringVar()
        self.PSDFrame = Frame(self.main)
        self.PSDFrame.pack()
        self.PSDFrame.place(relwidth= 0.3, anchor = "n", relx = 0.15, rely = 0.88)
        self.PSDLabel = Label(self.PSDFrame, text = "PSD")
        self.PSDLabel.pack(side = "left", padx=10)
        self.PSDEntry = Entry(self.PSDFrame, width= 10, textvariable = self.PSD)
        self.PSDEntry.pack(side = "left", padx= 5) 
        self.PSDUnit =  Label(self.PSDFrame, text = "dB")
        self.PSDUnit.pack(side = "left", padx=5)
        self.PSDpvalueEntry = Entry(self.PSDFrame, width= 10, textvariable = self.PSDp)
        self.PSDpvalueEntry.pack(side = "left", padx= 10) 

        self.patientFrame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.patientFrame.place(relwidth = 0.25,relheight= 0.15, relx = 0.35, rely = 0.03)
        self.patientLabel = Label(self.patientFrame,text="Patient", highlightbackground="black", highlightthickness=1)
        self.patientLabel.pack(side = "top")

        self.patientName = StringVar()
        self.patientNameLabel = Label(self.patientFrame, text = "Name:", font = ("Arial", 8))
        self.patientNameLabel.place(relx = 0.05, rely = 0.25)
        self.patientNameEntry = Entry(self.patientFrame, textvariable = self.patientName)
        self.patientNameEntry.place(relx = 0.2, rely = 0.25, relwidth= 0.7) 

        self.patientEye = StringVar()
        self.patientEyeLabel = Label(self.patientFrame, text = "Eye:", font = ("Arial", 8))
        self.patientEyeLabel.place(relx = 0.05, rely = 0.50)
        self.patientEyeEntry = Entry(self.patientFrame, textvariable = self.patientEye)
        self.patientEyeEntry.place(relx = 0.2, rely = 0.50, relwidth= 0.15) 

        self.patientTestDate = StringVar()
        self.patientTestDateLabel = Label(self.patientFrame, text = "Date:", font = ("Arial", 8))
        self.patientTestDateLabel.place(relx = 0.45, rely = 0.50)
        self.patientTestDateEntry = Entry(self.patientFrame, textvariable = self.patientTestDate)
        self.patientTestDateEntry.place(relx = 0.6, rely = 0.50, relwidth= 0.3) 

        self.patientAge = StringVar()
        self.patientAgeLabel = Label(self.patientFrame, text = "Age:", font = ("Arial", 8))
        self.patientAgeLabel.place(relx = 0.05, rely = 0.75)
        self.patientAgeEntry = Entry(self.patientFrame, textvariable = self.patientAge)
        self.patientAgeEntry.place(relx = 0.2, rely = 0.75, relwidth= 0.1) 

        self.patientBirthDate = StringVar()
        self.patientBirthDateLabel = Label(self.patientFrame, text = "Date of Birth:", font = ("Arial", 8))
        self.patientBirthDateLabel.place(relx = 0.4, rely = 0.75)
        self.patientBirthDateEntry = Entry(self.patientFrame, textvariable = self.patientBirthDate)
        self.patientBirthDateEntry.place(relx = 0.6, rely = 0.75, relwidth= 0.3) 
    
        self.settingsFrame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.settingsFrame.place(relwidth = 0.25,relheight= 0.13, relx = 0.35, rely = 0.2)
        self.settingsLabel = Label(self.settingsFrame,text="Settings", highlightbackground="black", highlightthickness=1)
        self.settingsLabel.pack(side = "top")

        self.pattern = StringVar()
        self.settingsPatternLabel = Label(self.settingsFrame, text = "Pattern:", font = ("Arial", 8))
        self.settingsPatternLabel.place(relx = 0.02, rely = 0.35)
        self.settingsPatternEntry = Entry(self.settingsFrame, textvariable = self.pattern)
        self.settingsPatternEntry.place(relx = 0.18, rely = 0.35, relwidth= 0.25) 

        self.stimulus = StringVar()
        self.settingsStimulusLabel = Label(self.settingsFrame, text = "Stimulus:", font = ("Arial", 8))
        self.settingsStimulusLabel.place(relx = 0.45, rely = 0.35)
        self.settingsStimulusEntry = Entry(self.settingsFrame, textvariable = self.stimulus)
        self.settingsStimulusEntry.place(relx = 0.6, rely = 0.35, relwidth= 0.3) 

        self.strategy = StringVar()
        self.settingsStrategyLabel = Label(self.settingsFrame, text = "Strategy:", font = ("Arial", 7))
        self.settingsStrategyLabel.place(relx = 0.02, rely = 0.65)
        self.settingsStrategyEntry = Entry(self.settingsFrame, textvariable = self.strategy)
        self.settingsStrategyEntry.place(relx = 0.18, rely = 0.65, relwidth= 0.25) 

        self.background = StringVar()
        self.settingsBackgroundLabel = Label(self.settingsFrame, text = "Background:", font = ("Arial", 7))
        self.settingsBackgroundLabel.place(relx = 0.45, rely = 0.65)
        self.settingsBackgroundEntry = Entry(self.settingsFrame, textvariable = self.background)
        self.settingsBackgroundEntry.place(relx = 0.60, rely = 0.65, relwidth= 0.3) 

        self.sensitivityGraph = NumDbGraphView(self.main)
        self.sensitivityGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.66, rely = 0.03)
        self.sensitivityGraph.fill()
        self.sensitivityGraph.setTitle("Sensitivity")


        self.reliabilityMetricsFrame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.reliabilityMetricsFrame.place(relwidth = 0.25,relheight= 0.13, relx = 0.35, rely = 0.35)
        self.reliabilityMetricsLabel = Label(self.reliabilityMetricsFrame,text="Reliability Metrics", highlightbackground="black", highlightthickness=1)
        self.reliabilityMetricsLabel.pack(side = "top")

        self.FIXLOS = StringVar()
        self.FIXLOSLabel = Label(self.reliabilityMetricsFrame, text = "FIX LOS", font = ("Arial", 8))
        self.FIXLOSLabel.place(relx = 0.02, rely = 0.35)
        self.FIXLOSEntry = Entry(self.reliabilityMetricsFrame, textvariable=self.FIXLOS)
        self.FIXLOSEntry.place(relx = 0.18, rely = 0.35, relwidth= 0.25) 

        self.duration = StringVar()
        self.durationLabel = Label(self.reliabilityMetricsFrame, text = "Duration", font = ("Arial", 8))
        self.durationLabel.place(relx = 0.45, rely = 0.35)
        self.durationEntry = Entry(self.reliabilityMetricsFrame, textvariable=self.duration)
        self.durationEntry.place(relx = 0.6, rely = 0.35, relwidth= 0.3) 

        self.FPR = StringVar()
        self.FPRLabel = Label(self.reliabilityMetricsFrame, text = "FPR", font = ("Arial", 7))
        self.FPRLabel.place(relx = 0.02, rely = 0.65)
        self.FPREntry = Entry(self.reliabilityMetricsFrame, textvariable = self.FPR)
        self.FPREntry.place(relx = 0.18, rely = 0.65, relwidth= 0.25)  

        self.FNR = StringVar()
        self.FNRLabel = Label(self.reliabilityMetricsFrame, text = "FNR", font = ("Arial", 7))
        self.FNRLabel.place(relx = 0.45, rely = 0.65)
        self.FNREntry = Entry(self.reliabilityMetricsFrame, textvariable = self.FNR)
        self.FNREntry.place(relx = 0.60, rely = 0.65, relwidth= 0.3) 

        self.totalDeviationGraph = NumDbGraphView(self.main)
        self.totalDeviationGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.35, rely = 0.55)
        self.totalDeviationGraph.fill()
        self.totalDeviationGraph.setTitle("Total deviation")

        self.patternDeviationGraph = NumDbGraphView(self.main)
        self.patternDeviationGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.70, rely = 0.55)
        self.patternDeviationGraph.fill()
        self.patternDeviationGraph.setTitle("Pattern deviation")

        self.entries = {
            "VFI": self.VFIEntry,
            "GHT": self.GHTEntry,
            "MD": self.MDEntry,
            "MDp": self.MDpvalueEntry,
            "PSD": self.PSDEntry,
            "PSDp": self.PSDpvalueEntry,
            "Name": self.patientNameEntry,
            "Eye": self.patientEyeEntry,
            "Visit": self.patientTestDateEntry,
            "Age": self.patientAgeEntry,
            "Date of Birth": self.patientBirthDateEntry,
            "Stimulus":self.settingsStimulusEntry,
            "Strategy":self.settingsStrategyEntry,
            "Pattern": self.settingsPatternEntry,
            "Background": self.settingsBackgroundEntry,
            "FIXLOS": self.FIXLOSEntry,
            "Duration": self.durationEntry,
            "FNR": self.FNREntry,
            "FPR": self.FPREntry,
        }
        self.variables ={
            "VFI": self.VFI,
            "GHT": self.GHT,
            "MD": self.MD,
            "MDp": self.MDp,
            "PSD": self.PSD,
            "PSDp": self.PSDp,
            "Name": self.patientName,
            "Eye": self.patientEye,
            "Visit": self.patientTestDate,
            "Age": self.patientAge,
            "Date of Birth": self.patientBirthDate,
            "Stimulus":self.stimulus,
            "Strategy":self.strategy,
            "Pattern": self.pattern,
            "Background": self.background,
            "FIXLOS": self.FIXLOS,
            "Duration": self.duration,
            "FNR": self.FNR,
            "FPR": self.FPR,
        }

    def onSelectReport(self, event):
        """Method to be called after selecting a report in the list.

        Args:
            event (Any): Argument needed for retrieving the selected item in the list.
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.control.displayReport(index)

    def back(self):
        """Returns to the welcome activity
        """
        self.main.destroy()
        self.control.back()

    def loadStudy(self):
        """Loads a .csv file into the program
        """
        path = filedialog.askopenfilename()
        self.reportSelectionList.delete(0, END)
        self.control.readCsv(path)

    def displayReportList(self, namelist: List[str], checklist: List[str]):
        """Displays the list of reports read from the .csv file

        Args:
            namelist (List[str]): The list of filenames of the reports.
            checklist ([type]): The list of 'checked' status of the reports.
        """
        for i in range(len(namelist)):
            self.reportSelectionList.insert(i, namelist[i])
        for i in range(len(checklist)):
            if int(checklist[i]) == 1 :
                self.reportSelectionList.itemconfig(i, {'bg': 'green'})
    
    def commit(self):
        """Saves all changes to the current report.
        """
        if self.control.saveReport():
            index = self.reportSelectionList.curselection()
            self.reportSelectionList.itemconfig(index, {'bg': 'green'})
        
    def showWarning(self):
        """Highlights all entry boxes with wrong/missing values.

        Returns:
            bool: True if at least one entry box has a wrong/missing value.
        """
        missing= False
        for k,v in self.entries.items():
            if self.variables[k].get() == "":
                v.config(bg="#FFF284")
                missing = True
            else:
                v.config(bg = "white")
        if self.sensitivityGraph.showWarning(self.patientEye.get(), False):
            missing = True
        if self.totalDeviationGraph.showWarning(self.patientEye.get(), True):
            missing = True
        if self.patternDeviationGraph.showWarning(self.patientEye.get(), True):
            missing = True
        return missing

        

    

    



        


        

