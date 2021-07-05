import traceback

import PIL

from models.VFTReport import VFTReport
import pytesseract
from PIL import Image, ImageEnhance
import pdf2image
import os
import numpy as np
import re
from math import floor

class HFAv2Reader:
    def __init__(self) -> None:
        #TODO: Find a way to set the path for pytesseract
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        self.poppler =  "poppler-0.68.0_x86/poppler-0.68.0/bin"
        self.patterns = {
            "Eye": re.compile("Eye: (.*)"),
            "Name": re.compile("Patient:\s*(.*)"),
            "Birth": re.compile("Date of Birth:\s*(.*)"),
            "Gender": re.compile("Gender:\s*(.*)"),
            "ID": re.compile("Patient ID:\s*(.*)"),
            #"FIXMON": re.compile("Fixation Monitor: (.*)"),
            #"FIXTAR": re.compile("Fixation Target: (.*)"),
            "FIXLOS": re.compile("Fixation Losses:\s*(.*)\s* Strategy:"),
            "FPR": re.compile("False POS Errors:\s*(.*)"),
            "Duration": re.compile("Test Duration: (.*)"),
            "FNR": re.compile("False NEG Errors:\s*(.*)"),
            "Fovea": re.compile("Fovea:\s*(.*)"),
            "Pattern": re.compile(".*(\d\d\s*-\s*\d).*"),
            "Stimulus": re.compile("Stimulus:\s*(.*)\s*Pupil"),
            "Date": re.compile("Date:\s*(.*)\s*"),
            "Background": re.compile("Background:\s*(.*)\s*Visual Acuity:"),
            "Time": re.compile("Time:\s*(.*)\s*"),
            "Strategy": re.compile("Strategy:\s*(.*)\s*RX:"),
            "Age": re.compile("Age:\s*(.*)\s*"),
            "GHT": re.compile("GHT\s*\n*(.*)"),
            "VFI": re.compile("VFI\s*(.*)"),
            "MD": re.compile("MD\s*(.*)dB"),
            "MDp": re.compile("MD\s*.*(P\s*<\s*.*%)"),
            "PSD": re.compile("PSD\s*(.*)dB"),
            "PSDp": re.compile("PSD\s*.*(P\s*<\s*.*%)"),
        }
        self.values = {}
        self.numdB_pattern = re.compile('FIELD\s*(\S*)\s*FIELD')
        self.numdB_aux = Image.open("numdB_aux.png")
        
    def pdf_to_img(self, pdf_file):
        #TODO: Same for poppler
        return pdf2image.convert_from_path(pdf_file,dpi = 500, poppler_path= self.poppler)

    def ocr_num(self, image):
        text = pytesseract.image_to_string(image, config= "--psm 7 -c tessedit_char_whitelist=FIELD-<0123456789")
        return text

    def ocr_core(self, file):
        text = pytesseract.image_to_string(file)
        return text
    def ocr_main_graph(self, image):
        text = pytesseract.image_to_string(image, config= "--psm 7 -c tessedit_char_whitelist=FIELD-<0123456789 CONFIGFILE=VFTgraph")
        return text
    def concat_images(self, imga, imgb):
        """
        Combines two color image ndarrays side-by-side.
        """
        print("imga: ", imga.shape)
        print("imgb: ", imgb.shape)
        ha,wa = imga.shape[:2]
        hb,wb = imgb.shape[:2]
        max_height = np.max([ha, hb])
        total_width = wa+wb
        new_img = np.zeros(shape=(max_height, total_width, 3))
        new_img[:ha,:wa]=imga
        new_img[:hb,wa:wa+wb]=imgb
        return new_img

    def concat_n_images(self, image_list):
        """
        Combines N color images from a list of image paths.
        """
        output = None
        for i, img in enumerate(image_list):
            if i==0:
                output = img
            else:
                output = self.concat_images(output, img)
        return output

    def readfile(self, dir, filename):
        
        eyeSide = "Right" #TODO: CHANGE
        file = os.path.join(dir, filename)
        
        if filename.endswith(".Pdf") or filename.endswith(".pdf"):
            images = self.pdf_to_img(file)
            img = images[0]
        else:
            img = Image.open(file)    
        img = img.resize((4250, 5500))
        #report_height = 2200
        #report_width = 1700
        arr = np.array(img)
        
        #Crop graphs
        sensGraph = img.crop((1038, 1050, 2232, 2463))
        MDGraph = img.crop((633,2383, 1455, 3292))
        PSDGraph = img.crop((1866, 2383, 2658, 3292))
        resultInfo = img.crop((2660, 2660, 4000, 3500))
        
        #Delete axis from sensitivity graph, as it is different than the 2 remaining graphs
        sensGraph_arr = np.array(sensGraph)
        sensGraph_arr[683:738, :] = (255, 255, 255)
        sensGraph_arr[:, 583:625] = (255, 255, 255)
        sensGraph = Image.fromarray(sensGraph_arr)
        
        MDGraph_arr = np.array(MDGraph)
        PSDGraph_arr = np.array(PSDGraph)

        arr[1050:1800, 1038:] = (255, 255, 255)
        arr[1800:, :] = (255, 255, 255)
        cropped = Image.fromarray(arr)
      
        main_text = self.ocr_core(cropped)
        print(main_text)
        
        test_result_text = self.ocr_core(resultInfo)
        print(test_result_text)
        fulltext = main_text + "\n" + test_result_text
        
        for k, v in self.patterns.items():
            match = v.search(fulltext)
            if match:
                self.values[k] = match.group(1)
            else:
                self.values[k] = ""
        try:
            FIXLOS, FIXTST = self.values["FIXLOS"].split("/")
        except ValueError:
            FIXLOS = self.values["FIXLOS"]
            FIXTST = ""
        return VFTReport(filename,self.values["Name"], self.values["Eye"], self.values["Date"] + " " + self.values["Time"], self.values["Age"], self.values["Birth"], self.values["ID"], FIXLOS, FIXTST, self.values["FNR"], self.values["FPR"], self.values["Duration"],self.values["GHT"], self.values["VFI"], self.values["MD"], self.values["MDp"], self.values["PSD"], self.values["PSDp"],  self.values["Pattern"], self.values["Strategy"], self.values["Stimulus"], self.values["Background"], self.values["Fovea"] ,self.HFAv2mainGraph2data(sensGraph_arr), self.image2data(MDGraph_arr), self.image2data(PSDGraph_arr), 0)


    def image2data(self, image):
        image[(floor(image.shape[0]/2)-6):(floor(image.shape[0]/2)+6),:] = (255, 255, 255)
        image[:, (floor(image.shape[1]/2)-6):(floor(image.shape[1]/2)+6)] = (255, 255, 255)
        

        arr = [[0 for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                cell = image[floor(i * image.shape[0] / 10):floor((i+1) * image.shape[0] / 10),floor(j * image.shape[1] / 10):floor((j+1) * image.shape[1] / 10)]
                """val = self.ocr_num(Image.fromarray(cell))
                
                match = self.numdB_pattern.search(val)

                if match:
                    arr[i][j] = match.group(0)

                else:
                    arr[i][j] = ''"""
                val_img = Image.fromarray(cell)
                aux = self.numdB_aux.resize((val_img.width*2, val_img.height))
                images = [aux.copy(), val_img, aux.copy()]
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new('RGB', (total_width, max_height), color="white")
                
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                val = self.ocr_num(new_im)
                match = self.numdB_pattern.search(val)
                if match and match.group(1) != "-":
                    arr[i][j] = match.group(1)
                else:
                    arr[i][j] = ''
        
        for i in arr:
            print(i)
        print("\n"*3)
        return arr

    def HFAv2mainGraph2data(self, image):
        pattern = re.compile("\S*")
        arr = [["" for i in range(19)] for j in range(20)]
        for i in range(19):
            for j in range(19):

                cell = image[floor(i * image.shape[0] / 20):floor((i+1) * image.shape[0] / 20),floor(j * image.shape[1] / 20+image.shape[1] / 40):floor((j+1) * image.shape[1] / 20 + image.shape[1] / 40)]
                cell_img = Image.fromarray(cell)
                
                enhancer = ImageEnhance.Sharpness(cell_img)
                cell_img = enhancer.enhance(3)
                cell_img = cell_img.convert("1")
                val = self.ocr_main_graph(cell_img)
                
                match = pattern.search(val)

                if match:
                    arr[i][j] = match.group(0)
                    """if len(arr[i][j]) == 1:
                        Image.fromarray(cell).show()"""
                else:
                    arr[i][j] = ''
        result = [["" for i in range(10)] for j in range(10)]       
        for i in range(10):
            for j in range(19):
                if i % 2 == 1 and j%2 == 0:
                    result[int((i-1)/2)][int(j/2)] = arr[i][j]
                else:
                    continue
        for i in range(10, 20):
            for j in range(19):
                if i % 2 == 0 and j % 2 == 0:
                    result[int(i/2)][int(j/2)] = arr[i][j]
                else:
                    continue
        for i in result:
            print(i)
            print("\n"*3)
        return arr

    def grid(self, image):
        for i in range(20):
            image[floor(image.shape[0]/20 * i) ,:] = (0, 0, 0)
            image[:,floor(image.shape[1]/40 + image.shape[1]/20 * i)] = (0, 0, 0)
            
        Image.fromarray(image).show()
