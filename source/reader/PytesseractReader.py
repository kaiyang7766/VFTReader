
from reader.HFAv2Reader import HFAv2Reader
from reader.HFAv3Reader import HFAv3Reader
import traceback
from reader.ReportReader import ReportReader
import Constants
from models.VFTReport import VFTReport
import pytesseract
from PIL import Image
import pdf2image
import os
import numpy as np
import re
from math import floor
from threading import Thread
class PytesseractReader(ReportReader, Thread):

    def __init__(self, dir, curActivity) -> None:
        """A VFT report reader using pytesseract as the OCR engine

        Attributes:
            curActivity: The control of the activity that initialized an instance of the reader. Must subclass ExtractionControl.
            dir: The directory containing the reports to be extracted
            HFAv3reader: Algorithm for processing HFAv3 format
            HFAv2reader: Algorithm for processing HFAv2 format
        """
        Thread.__init__(self)
        self.curActivity = curActivity
        self.dir = dir
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        
        self.HFAv3reader = HFAv3Reader()
        self.HFAv2reader = HFAv2Reader()

    def run(self):
        reportList = self.read(self.dir)
        self.curActivity.onFinishExtraction(reportList)
        self.curActivity.queueMessage(0)
    #report_height = 2340
    #report_width = 1655
    def read(self, dir):
        """Reads all eligible VFT reports in a directory.

        Eligible extensions include: .pdf, .png, .jpg, .tif . The application has only been tested against .tif and .pdf files.

        Args:
            dir (str): The path to the directory

        Returns:
            List[VFTReport]: The list of extracted VFT reports
        """
        filelist = []
        reportList = []
        for filename in os.listdir(dir):
            if filename.lower().endswith((".pdf", ".png", ".jpg", ".tif")): 
                filelist.append(filename)
        length =len(filelist)
        self.curActivity.queueMessage("Found " + str(length) + " files with supported format in selected directory")
        i = 0
        for filename in filelist:
            try:
                i+=1
                self.curActivity.queueMessage("(" + str(i) + '/' + str(length) + ')Processing ' + filename)
                reportList.append(self.readfile(dir, filename))
            except:
                self.curActivity.queueError("An error has occured while processing file. Skipping to the next report")
                traceback.print_exc()
        return reportList

    def pdf_to_img(self, pdf_file):
        """Converts a .pdf file to an Image

        Args:
            pdf_file (str): The path to the file

        Returns:
            List: The pages of the pdf file
        """
        return pdf2image.convert_from_path(pdf_file, poppler_path= Constants.POPPLER_PATH)

    def ocr_core(self, image):
        """Extracts the text from an image

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(image)
        return text

    def readfile(self, dir, filename):
        """Reads an individual report.

        We noticed that HFAv3-type reports have a different format compared to HFAv2-type reports.
        Moreover, we have noticed that VFT reports seem to have a small line near the bottom indicating
        whether it is a HFAv3 report or a HFAv2 report. We also assumed that HFAv3 reports will
        always be colorized, and HFAv2 reports will always be black and white.

        This method firstly crops out the bottom 1/10th of the report. It then scans the cropped part
        for the string 'HFA II' or 'HFA 3'. If either of those exists, the appropriate reader will be 
        called to continue processing. If neither of them exists, the appropriate reader will be decided
        based on whether the image is in black & white or not.

        Note:
            A typical report should take about 2 minutes to be processed, with no other heavy processes running in the background.

        Args:
            dir (str): The directory leading to the file.
            filename (str): The name of the file.

        Returns:
            VFTReport: The VFT report in the image.
        """
        #Creates an Image object from the file
        filepath = os.path.join(dir, filename)
        if filename.lower().endswith(".pdf"):
            images = self.pdf_to_img(filepath)
            img = images[0]
        else:
            img = Image.open(filepath)
        
        width, height = img.size
        img = img.convert("RGB")
        arr = np.array(img)
        #Crops the image
        report_type_arr = arr[floor(height * 9 / 10):, :]
        #Extract the text
        text = self.ocr_core(report_type_arr)
        #Checks the text for the version indicator
        if "HFA Il" in text or "HFA II" in text:
            return self.HFAv2reader.readImage(dir, filename)
        elif "HFA 3" in text:
            return self.HFAv3reader.readImage(dir, filename)
        else:   # Checks if the image is in black & white
            if (arr[:, :, 0] != arr[:, :, 1]).any() or (arr[:, :, 2] != arr[:,:, 1]).any():
                return self.HFAv3reader.readImage(dir, filename)
            else:
                return self.HFAv2reader.readImage(dir, filename)

        




            
