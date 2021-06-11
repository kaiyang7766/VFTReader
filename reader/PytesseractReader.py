from ExtractionControl import ExtractionControl
from typing import Text
from reader.ReportReader import ReportReader
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
    def read(self, dir, curActivity: ExtractionControl):
        filelist = []
        reportList = []
        for filename in os.listdir(dir):
            if filename.endswith(".Pdf"): 
                filelist.append(filename) 
        curActivity.logNumFiles(len(filelist))
        for filename in filelist:
            reportList.append(self.readfile(dir, filename))  
                
        return reportList
    def pdf_to_img(self, pdf_file):
        #TODO: Same for poppler
        return pdf2image.convert_from_path(pdf_file, poppler_path= self.poppler)

    def ocr_num(self, image):
        text = pytesseract.image_to_string(image)
        return text

    def ocr_core(self, file):
        text = pytesseract.image_to_string(file)
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
            sensGraph = img.crop((361, 622, 852, 1115))
            MDGraph = img.crop((190, 1090, 518, 1416))
            PSDGraph = img.crop((700, 1090, 1028, 1416))
            resultInfo = img.crop((1100, 1250, 1600, 1550))
            
            #Delete axis from graph
            sensGraph_arr = np.array(sensGraph)
            MDGraph_arr = np.array(MDGraph)         
            PSDGraph_arr = np.array(PSDGraph)
            

            arr[0:230, 910:1150] = (255,255,255)
            arr[320:380, :1100] = (255, 255, 255)
            arr[622:1100, 300:1500] = (255, 255, 255)
            arr[1100:, :] = (255, 255, 255)

            cropped = Image.fromarray(arr)
      
            main_pattern = re.compile('Patient: (.*)\n*Date of Birth: (.*)\n*Gender: (.*)\n*Patient ID: (.*)\n*Fixation Monitor: (.*)\n*Fixation Target: (.*)\n*Fixation Losses: (.*)\n*False POS Errors: (.*)\n*False NEG Errors: (.*)\n*Test Duration: (.*)\n*Fovea: (.*)\n*.*(\d+-\d+).*\n*Stimulus: (.*) Date: (.*)\n*Background: (.*) Time: (.*)\n*Strategy: (.*) Age: (.*)')
            patientName, birth, gender, ID, FIXMon, FIXTar, FIXLOS, FPR, FNR, duration, fovea, pattern, stimulus, date, background, time, strategy, age = main_pattern.search(self.ocr_core(cropped)).groups()
            
            test_results_pattern = re.compile('GHT: (.*)\n*VFI: (.*)\n*MD\d+-\d+: (.*)(P<.*%)\n*PSD\d+-\d+: (.*)(P<.*%)')
            GHT, VFI, MD, MDp, PSD, PSDp = test_results_pattern.search(self.ocr_core(resultInfo)).groups()

            return VFTReport(filename, eyeSide, datetime, age, ID, FIXLOS, FNR, FPR, duration, GHT, VFI, MD, MDp, PSD, PSDp,  pattern, strategy, stimulus, background, fovea ,self.image2data(sensGraph_arr), self.image2data(MDGraph_arr), self.image2data(PSDGraph_arr), False)




    def image2data(self, image):
        
        image[(floor(image.shape[1]/2)-6):(floor(image.shape[1]/2)+6),:] = (255, 255, 255)
        image[:, (floor(image.shape[0]/2)-6):(floor(image.shape[0]/2)+6)] = (255, 255, 255)
        i, j = 4, 4
        
        index = 0
        arr = [[0 for i in range(10)] for j in range(10)]
        numdB_pattern = re.compile('\S+')
        
        for i in range(10):
            for j in range(10):
                text = numdB_pattern.findall(self.ocr_num(Image.fromarray(image[floor(i * image.shape[0] / 10):floor((i+1) * image.shape[0] / 10),floor(j * image.shape[0] / 10):floor((j+1) * image.shape[0] / 10)])))
                if len(text) == 0:
                    arr[i][j] = None
                else:
                    arr[i][j] = text[0]
        for i in arr:
            print(i)
        print("\n"*3)
        return arr
    
    def grid(self, image):
        for i in range(10):
            image[floor(image.shape[1]/10 * i) ,:] = (0, 0, 0)
            image[:,floor(image.shape[0]/10 * i)] = (0, 0, 0)
            
        Image.fromarray(image).show()


            
