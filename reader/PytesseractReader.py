
from reader.HFAv2Reader import HFAv2Reader
from reader.HFAv3Reader import HFAv3Reader
import traceback
from reader.ReportReader import ReportReader

from models.VFTReport import VFTReport
import pytesseract
from PIL import Image
import pdf2image
import os
import numpy as np
import re
from math import floor
from threading import Thread
class PytesseractReader(ReportReader):    
    def __init__(self, dir, curActivity) -> None:
        #TODO: Find a way to set the path for pytesseract
        Thread.__init__(self)
        self.curActivity = curActivity
        self.dir = dir
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        self.poppler =  "poppler-0.68.0_x86/poppler-0.68.0/bin"
        self.HFAv3reader = HFAv3Reader()
        self.HFAv2reader = HFAv2Reader()

    def run(self):
        self.read()
    #report_height = 2340
    #report_width = 1655
    def read(self):
        filelist = []
        reportList = []
        for filename in os.listdir(self.dir):
            if filename.lower().endswith((".pdf", ".png", ".jpg", ".tif")): 
                filelist.append(filename)
        length =len(filelist)
        self.curActivity.queueMessage("Found " + str(length) + " files with supported format in selected directory")
        i = 0
        for filename in filelist:
            try:
                i+=1
                self.curActivity.queueMessage("(" + str(i) + '/' + str(length) + ')Processing ' + filename)
                reportList.append(self.readfile(self.dir, filename))
            except:
                self.curActivity.queueError("An error has occured while processing file. Skipping to the next report")
                traceback.print_exc()
        self.curActivity.onFinishExtraction(reportList)
        self.curActivity.queueMessage(0)

    def pdf_to_img(self, pdf_file):
        #TODO: Same for poppler
        return pdf2image.convert_from_path(pdf_file, poppler_path= self.poppler)

    def ocr_core(self, file):
        text = pytesseract.image_to_string(file)
        return text

    def readfile(self, dir, filename):
        filepath = os.path.join(dir, filename)
        if filename.lower().endswith(".pdf"):
            images = self.pdf_to_img(filepath)
            img = images[0]
        else:
            img = Image.open(filepath)
        width, height = img.size
        img = img.convert("RGB")
        arr = np.array(img)
        report_type_arr = arr[floor(height * 9 / 10):, :]

        text = self.ocr_core(report_type_arr)
        if "HFA Il" in text or "HFA II" in text:
            return self.HFAv2reader.readImage(dir, filename)
        elif "HFA 3" in text:
            return self.HFAv3reader.readImage(dir, filename)
        else:
            if (arr[:, :, 0] != arr[:, :, 1]).any() or (arr[:, :, 2] != arr[:,:, 1]).any():
                return self.HFAv3reader.readImage(dir, filename)
            else:
                return self.HFAv2reader.readImage(dir, filename)

        




            
