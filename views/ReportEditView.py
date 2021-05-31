
from tkinter import *
from tkinter.font import families
from typing import Dict, Optional
import Constants
from math import floor



class NumDbGraphView(Frame):
    def fill(self):
        self.entryViews = [[0 for i in range(10)] for j in range(10)]
        self.entryVariables = [[0 for i in range(10)] for j in range(10)]

        print(self.entryVariables)
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
                    self.entryViews[i][j].configure(state = DISABLED)
                    self.entryViews[i][j].place(relwidth= 0.07, relheight= 0.07, relx =0.03 + 0.1 * i , rely =0.03+ 0.1 * j)
    def setTitle(self, title):
        self.title = Label(self, text = title)
        self.title.place(relx = 0, rely = 0)

    def getVariables(self):
        result = [[0 for i in range(10)] for j in range(10)]
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    result[i][j] = None
                else:
                    result[i][j] = self.entryVariables[i][j].get()

    def setVariables(self, new_matrix):
        for i  in range(10):
            for j in range(10):
                if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                    self.entryVariables[i][j] = None
                else:
                    self.entryVariables[i][j].set(str(new_matrix[i][j]))


class ReportEditView:
    def __init__(self, control, root) -> None:
        self.root = root
        self.control = control
        self.main = Frame(root)
        self.main.pack(fill = "both", expand= True)

        self.reportSelectionContainer = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.reportSelectionContainer.pack()
        self.reportSelectionContainer.place(relwidth=0.3, relheight=0.5, relx=0, rely=0)

        self.reportSelectionHeader = Label(self.reportSelectionContainer, font = ("Arial", 14), text="Choose a report")
        self.reportSelectionHeader.pack(fill = "x", expand= True, pady=10)
        self.reportSelectionHeader.place(relx = 0.5, anchor = "n")

        self.reportSelectionList = Listbox(self.reportSelectionContainer)
        self.vsb = Scrollbar(self.reportSelectionList, command=self.reportSelectionList.yview, orient="vertical")
        self.reportSelectionList.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.reportSelectionList, command=self.reportSelectionList.xview, orient="horizontal")
        self.reportSelectionList.configure(yscrollcommand=self.hsb.set)
        self.reportSelectionList.pack(fill = "both", pady= 5)
        self.reportSelectionList.place(relwidth= 1, relheight=0.95, rely = 0.15)
        #TODO: Replace with proper logic
        self.reportSelectionList.insert(-1, "    SAMPLE_FILE.PDF")
        self.reportSelectionList.insert(-1, "   SAMPLE_FILE_2.PDF")
        self.reportSelectionList.insert(-1, "   SAMPLE_FILE_3.PDF")
        self.reportSelectionList.insert(-1, "   SAMPLE_FILE_4.PDF")
        self.reportSelectionList.insert(-1, "   SAMPLE_FILE_5.PDF")
        self.reportSelectionList.itemconfig(0, {"bg": "green"})

        
        self.commitButton = Button(self.main, text = "Commit")
        self.commitButton.place(anchor = "n",relx= 0.07, rely = 0.6)

        self.loadButton = Button(self.main, text = "Load")
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
        self.patientFrame.place(relwidth = 0.25,relheight= 0.13, relx = 0.35, rely = 0.03)
        self.patientLabel = Label(self.patientFrame,text="Patient", highlightbackground="black", highlightthickness=1)
        self.patientLabel.pack(side = "top")

        self.patientName = StringVar()
        self.patientNameLabel = Label(self.patientFrame, text = "Name:", font = ("Arial", 8))
        self.patientNameLabel.place(relx = 0.05, rely = 0.35)
        self.patientNameEntry = Entry(self.patientFrame, textvariable = self.patientName)
        self.patientNameEntry.place(relx = 0.3, rely = 0.35, relwidth= 0.5) 

        self.patientEye = StringVar()
        self.patientEyeLabel = Label(self.patientFrame, text = "Eye:", font = ("Arial", 8))
        self.patientEyeLabel.place(relx = 0.05, rely = 0.65)
        self.patientEyeEntry = Entry(self.patientFrame, textvariable = self.patientEye)
        self.patientEyeEntry.place(relx = 0.2, rely = 0.65, relwidth= 0.15) 

        self.patientTestDate = StringVar()
        self.patientTestDateLabel = Label(self.patientFrame, text = "Date:", font = ("Arial", 8))
        self.patientTestDateLabel.place(relx = 0.45, rely = 0.65)
        self.patientTestDateEntry = Entry(self.patientFrame, textvariable = self.patientTestDate)
        self.patientTestDateEntry.place(relx = 0.6, rely = 0.65, relwidth= 0.3) 

    
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
        self.settingsStimulusEntry.place(relx = 0.65, rely = 0.35, relwidth= 0.3) 

        self.strategy = StringVar()
        self.settingsStrategyLabel = Label(self.settingsFrame, text = "Strategy:", font = ("Arial", 7))
        self.settingsStrategyLabel.place(relx = 0.02, rely = 0.65)
        self.settingsStrategyEntry = Entry(self.settingsFrame, textvariable = self.strategy)
        self.settingsStrategyEntry.place(relx = 0.18, rely = 0.65, relwidth= 0.25) 

        self.background = StringVar()
        self.settingsBackgroundLabel = Label(self.settingsFrame, text = "Background:", font = ("Arial", 7))
        self.settingsBackgroundLabel.place(relx = 0.45, rely = 0.65)
        self.settingsBackgroundEntry = Entry(self.settingsFrame, textvariable = self.background)
        self.settingsBackgroundEntry.place(relx = 0.70, rely = 0.65, relwidth= 0.25) 

        self.sensitivityGraph = NumDbGraphView(self.main)
        self.sensitivityGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.66, rely = 0.03)
        self.sensitivityGraph.fill()
        self.sensitivityGraph.setTitle("Sensitivity")


        self.reliabilityMetricsFrame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.reliabilityMetricsFrame.place(relwidth = 0.25,relheight= 0.13, relx = 0.35, rely = 0.35)
        self.reliabilityMetricsLabel = Label(self.reliabilityMetricsFrame,text="Settings", highlightbackground="black", highlightthickness=1)
        self.reliabilityMetricsLabel.pack(side = "top")

        self.FIXLOSLabel = Label(self.reliabilityMetricsFrame, text = "FIX LOS", font = ("Arial", 8))
        self.FIXLOSLabel.place(relx = 0.02, rely = 0.35)
        self.FIXLOSEntry = Entry(self.reliabilityMetricsFrame)
        self.FIXLOSEntry.place(relx = 0.18, rely = 0.35, relwidth= 0.25) 

        self.durationLabel = Label(self.reliabilityMetricsFrame, text = "Duration", font = ("Arial", 8))
        self.durationLabel.place(relx = 0.45, rely = 0.35)
        self.durationEntry = Entry(self.reliabilityMetricsFrame)
        self.durationEntry.place(relx = 0.65, rely = 0.35, relwidth= 0.3) 

        self.FPRLabel = Label(self.reliabilityMetricsFrame, text = "FPR", font = ("Arial", 7))
        self.FPRLabel.place(relx = 0.02, rely = 0.65)
        self.FPREntry = Entry(self.reliabilityMetricsFrame)
        self.FPREntry.place(relx = 0.18, rely = 0.65, relwidth= 0.25) 

        self.FNRLabel = Label(self.reliabilityMetricsFrame, text = "FNR", font = ("Arial", 7))
        self.FNRLabel.place(relx = 0.45, rely = 0.65)
        self.FNREntry = Entry(self.reliabilityMetricsFrame)
        self.FNREntry.place(relx = 0.70, rely = 0.65, relwidth= 0.25) 



        self.totalDeviationGraph = NumDbGraphView(self.main)
        self.totalDeviationGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.35, rely = 0.55)
        self.totalDeviationGraph.fill()
        self.totalDeviationGraph.setTitle("Total deviation")

        self.patternDeviationGraph = NumDbGraphView(self.main)
        self.patternDeviationGraph.place(relheight=0.40, relwidth= 0.30, relx = 0.70, rely = 0.55)
        self.patternDeviationGraph.fill()
        self.patternDeviationGraph.setTitle("Pattern deviation")
    
    def back(self):
        self.main.destroy()
        self.control.back()
            

    

    



        


        

