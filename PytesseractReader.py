from ReportReader import ReportReader
from datetime import datetime
from tkinter import EventType

from numpy.lib.twodim_base import eye
from models.VFTReport import VFTReport
import pytesseract
from PIL import Image
import pdf2image
import os
import numpy as np
import re
from math import floor

class PytesseractReader(ReportReader):

    def __init__(self) -> None:
        #TODO: Find a way to set the path for pytesseract
        pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
        self.poppler =  "C:/Users/HP - PC/Downloads/poppler-0.68.0_x86/poppler-0.68.0/bin"
    #report_height = 2340
    #report_width = 1655
    def read(self, dir):
        reportList = []
        for filename in os.listdir(dir):
            if filename.endswith(".Pdf"): 
                reportList.append(self.readfile(dir, filename))
    def pdf_to_img(self, pdf_file):
        #TODO: Same for poppler
        return pdf2image.convert_from_path(pdf_file, poppler_path= self.poppler)


    def ocr_core(self, file):
        text = pytesseract.image_to_string(file)
        return text

    def ocr_dB(self, file):
        text = pytesseract.image_to_string(file, config="--psm 6")
        return text
    def readfile(self, dir, filename):
        if "OD" in filename:
            eyeSide = "Right"
        elif "OS" in filename:
            eyeSide = "Left"
        
        pdf_file = os.path.join(dir, filename)
        images = self.pdf_to_img(pdf_file)
        for pg, img in enumerate(images):
            arr = np.array(img)
            #Crop graphs
            sensGraph = img.crop((314, 620, 860, 1070))
            MDGraph = img.crop((140, 1110, 520, 1410))
            PSDGraph = img.crop((660, 1110, 1040, 1410))
            resultInfo = img.crop((1100, 1250, 1600, 1550))
            
            #Delete axis from graph
            sensGraph_arr = np.array(sensGraph)
            sensGraph_arr[:, 285:305] = (255, 255, 255)
            sensGraph_arr[242:265, :] = (255, 255, 255)
            sensGraph = Image.fromarray(sensGraph_arr)

            sensGraph.show()

            MDGraph_arr = np.array(MDGraph)
            MDGraph_arr[:, 207:220] = (255, 255, 255)
            MDGraph_arr[140:150, :] = (255, 255, 255)
            MDGraph_arr = self.grid(MDGraph_arr)
            MDGraph = Image.fromarray(MDGraph_arr)
            MDGraph.show()

            PSDGraph_arr = np.array(PSDGraph)
            PSDGraph_arr[:, 207:220] = (255, 255, 255)
            PSDGraph_arr[140:150, :] = (255, 255, 255)
            PSDGraph_arr = self.grid(PSDGraph_arr)
            PSDGraph = Image.fromarray(PSDGraph_arr)
            PSDGraph.show()

            arr[0:230, 910:1150] = (255,255,255)
            arr[320:380, :1100] = (255, 255, 255)
            arr[622:1100, 300:1500] = (255, 255, 255)
            arr[1100:, :] = (255, 255, 255)

            cropped = Image.fromarray(arr)
      
            main_pattern = re.compile('Patient: (.*)\n*Date of Birth: (.*)\n*Gender: (.*)\n*Patient ID: (.*)\n*Fixation Monitor: (.*)\n*Fixation Target: (.*)\n*Fixation Losses: (.*)\n*False POS Errors: (.*)\n*False NEG Errors: (.*)\n*Test Duration: (.*)\n*Fovea: (.*)\n*.*(\d+-\d+).*\n*Stimulus: (.*) Date: (.*)\n*Background: (.*) Time: (.*)\n*Strategy: (.*) Age: (.*)')
            patientName, birth, gender, ID, FIXMon, FIXTar, FIXLOS, FPR, FNR, duration, fovea, pattern, stimulus, date, background, time, strategy, age = main_pattern.search(self.ocr_core(cropped)).groups()
            
            test_results_pattern = re.compile('GHT: (.*)\n*VFI: (.*)\n*MD\d+-\d+: (.*)(P<.*%)\n*PSD\d+-\d+: (.*)(P<.*%)')

            GHT, VFI, MD, MDp, PSD, PSDp = test_results_pattern.search(self.ocr_core(resultInfo)).groups()
            numdB_pattern = re.compile('\S+')
            
            sens_values = numdB_pattern.findall(self.ocr_dB(sensGraph))
            MD_values = numdB_pattern.findall(self.ocr_dB(MDGraph))
            PSD_values =numdB_pattern.findall(self.ocr_dB(PSDGraph))
            print(sens_values)
            return VFTReport(filename, eyeSide, datetime, age, ID, FIXLOS, FNR, FPR, duration, GHT, VFI, MD, MDp, PSD, PSDp,  pattern, strategy, stimulus, background, fovea ,self.to2dArray(sens_values,eyeSide, True), self.to2dArray(MD_values,eyeSide, False), self.to2dArray(PSD_values, eyeSide, False), False)




    def to2dArray(self, graph, eye, is_main):
        index = 0

        arr = [[0 for i in range(10)] for j in range(10)]
        if eye.lower() == "right":
            for j in range(10):
                for i in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        arr[i][j] = None
                    else:
                        if i + j <=3 or i+j >=15 or i - j >= 6 or j - i >=6 or i == 0 or i == 9 or j == 9:
                            arr[i][j] = "NA"
                        else:
                            if not is_main:
                                if (i, j) == (7, 5) or (i, j) == (7, 4) or index >= len(graph):
                                    arr[i][j] = "NA"
                                    continue
                            arr[i][j] = graph[index]

                            index +=1
        
        else:
            for j in range(10):
                for i in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        arr[i][j] = None
                    else:
                        if i + j <=3 or i+j >=15 or i - j >= 6 or j - i >=6 or i == 0 or i == 9 or j == 0:
                            arr[i][j] = "NA"
                        else:
                            if not is_main:
                                if (i, j) == (2, 5) or (i, j) == (2, 4):
                                    arr[i][j] = "NA"
                                    continue
                            arr[i][j] = graph[index]
                            index +=1
    def grid(self, graph):
        for i in range(10):
            graph[floor(i * graph.shape[0] / 10), :] = (0, 0, 0)
            graph[:, floor(i * graph.shape[1]/10)] = (0, 0, 0)

        return graph

dir = ('C:/Users/HP - PC/VFTReader')
reader = PytesseractReader()
reader.read(dir)        


            
