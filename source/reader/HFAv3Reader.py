    
from math import floor
from models.VFTReport import VFTReport
import os
import re
from PIL import Image
import numpy as np
import pdf2image
import pytesseract
import Constants

class HFAv3Reader:
    """Extraction algorithm for HFAv3 reports.
    
    Attributes:
        patientInfoRegex: Regular expressions for patient information fields.
        resultInfoRegex: Regular expressions for test result information fields.
        patternRegex: Regular expression for visual field test pattern.
        fieldLocations: Locations of various information fields.
        ageLocation: Locations of the 'age' field. Separated since numbers have to be treated differently.
        numdB_pattern: Regular expressions for numeric dB graph values, after preprocessing.
        numdB_aux: An auxiliary image used to enhance accuracy. See readNum for more information
    """
    def __init__(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        self.patientInfoRegex = {
            "Name": re.compile("Patient:\s*(.*)\s*"),
            "Birth": re.compile("Date of Birth:\s*(.*)\s*"),
            "Gender": re.compile("Gender:\s*(.*)"),
            "ID": re.compile("Patient ID:\s*(.*)"),
            #"FIXMON": re.compile("Fixation Monitor: (.*)"),
            #"FIXTAR": re.compile("Fixation Target: (.*)"),
        }
        self.resultInfoRegex = {
            "GHT": re.compile("GHT.*:(.*)"),
            "VFI": re.compile("VFI.*:(.*)"),
            "MD": re.compile("MD.*:(.*)dB"),
            "MDp": re.compile("MD.*(P\s*<\s*.*%)"),
            "PSD": re.compile("PSD.*:(.*)dB"),
            "PSDp": re.compile("PSD.*(P\s*<\s*.*%)"),
        }
        self.patternRegex = re.compile("24-2|30-2|10-2")
        self.fieldLocations = {
            "FIXLOS": (400, 465, 650, 495),
            "FPR": (400, 495, 650, 525),
            "Duration": (400, 550, 650, 585),
            "FNR": (400, 525, 650, 555),
            "Fovea": (400, 590, 650, 620),
            "Stimulus": (1000, 405, 1250, 435),
            "Date": (1380, 405, 1650, 435),
            "Background": (1000, 435, 1250, 465),
            "Time": (1380, 435, 1650, 465),
            "Strategy": (1000, 465, 1250, 495),
        }
        self.ageLocation = (1380, 465, 1430, 495)
        self.values = {}
        self.numdB_pattern = re.compile('FIELD\s*(\S*)\s*FIELD')
        self.numdB_aux = Image.open("numdB_aux.png")
    def pdf_to_img(self, pdf_file):
        """Converts a .pdf file to an Image

        Args:
            pdf_file (str): The path to the file

        Returns:
            List: The pages of the pdf file
        """
        return pdf2image.convert_from_path(pdf_file, poppler_path= Constants.POPPLER_PATH, use_cropbox= False)

    def ocr_num(self, image):
        """Extracts the text from a preprocessed image of a numeric dB graph value.

        Due to the limitations of Pytesseract, different configurations were needed for short numerical values.

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(image, config= "--psm 7 -c tessedit_char_whitelist=FIELD-<0123456789")
        return text

    def ocr_core(self, file):
        """Extracts the text from an image.

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(file)
        return text

    def readImage(self, dir, filename):
        """Extracts the information from an VFT report

        We assumed that all information fields will be in the same relative location for all reports.
        The method first resizes the image to the same size as our test data. Secondly, several parts
        of the image are cropped and passed to the OCR engine to extract the information. Finally, the 
        information are combined into a VFTReport object, which will be returned by the method.

        Note:
            Short numeric values, such as the patient's age, and values in numeric dB graphs are treated
            differently than normal strings. See readNum for how we processes these values

        Args:
            dir (str): The directory leading to the file.
            filename (str): The name of the file.

        Returns:
            VFTReport: The VFT report in the image.
        """
        filepath = os.path.join(dir, filename)
        if filename.endswith(".Pdf") or filename.endswith(".pdf"):
            images = self.pdf_to_img(filepath)
            img = images[0]
        else:
            img = Image.open(filepath)
        #Resize image
        img =img.resize((1655, 2340))
        arr = np.array(img)

        #Crop regions of interests
        sensGraph = img.crop((361, 622, 852, 1115))
        MDGraph = img.crop((190, 1090, 518, 1416))
        PSDGraph = img.crop((700, 1090, 1028, 1416))
        resultInfo = img.crop((1100, 1250, 1600, 1550))
        eyeLabel = img.crop((200, 320, 255, 380))
        patientInfo = img.crop((0, 0, 910, 230))    
        patternInfo = img.crop((910, 320, 1650, 380))
        
        #Extract text from cropped regions
        self.values["Pattern"] = self.patternRegex.search(self.ocr_core(patternInfo)).group(0)
        patientInfoText = self.ocr_core(patientInfo)
        resultInfoText = self.ocr_core(resultInfo)
        print(patientInfoText)
        print(resultInfoText)
        
        #Extract information from raw text using regular expressions
        for k, v in self.patientInfoRegex.items():
            try:
                self.values[k] = v.search(patientInfoText).group(1).strip()
            except AttributeError:
                self.values[k] = ""
        for k, v in self.resultInfoRegex.items():
            try:
                self.values[k] = v.search(resultInfoText).group(1).strip()
            except AttributeError:
                self.values[k] = ""
        for k, v in self.fieldLocations.items(): 
            fieldImg = img.crop(v)
            self.values[k] = self.ocr_core(fieldImg).strip()

        self.values["Age"] = self.readNum(img.crop(self.ageLocation))

        eyeLabel = eyeLabel.convert("1")
        eye = self.ocr_core(eyeLabel)
        if "os" in eye.lower():
            eye = "Left"
        elif "od" in eye.lower():
            eye= "Right"
        else:
            eye = ""
        
        sensGraph_arr = np.array(sensGraph)
        MDGraph_arr = np.array(MDGraph)         
        PSDGraph_arr = np.array(PSDGraph)

        #FIXLOS and FIXTST gets special treatment due to FIXTST needing to be interpreted from Fixation Losses
        try:
            FIXLOS, FIXTST = self.values["FIXLOS"].split("/")
        except ValueError:
            FIXLOS = self.values["FIXLOS"]
            FIXTST = ""
        return VFTReport(filename,self.values["Name"], eye, self.values["Date"] + " " + self.values["Time"], self.values["Age"], self.values["Birth"], self.values["ID"], FIXLOS, FIXTST, self.values["FNR"], self.values["FPR"], self.values["Duration"],self.values["GHT"], self.values["VFI"], self.values["MD"], self.values["MDp"], self.values["PSD"], self.values["PSDp"],  self.values["Pattern"], self.values["Strategy"], self.values["Stimulus"], self.values["Background"], self.values["Fovea"] ,self.image2data(sensGraph_arr), self.image2data(MDGraph_arr), self.image2data(PSDGraph_arr), 0)

    def image2data(self, image:np.array):
        """Converts an image of a numeric dB graph to its representation inside the application.

        During our development, we noticed that the accuracy of the OCR engine was very poor
        for the numeric dB graphs. Therefore special treatment was needed to enhance the accuracy.

        The method first remove the axis from the graphs. Then it splits the image to a 10 x 10 grid.
        Then for each cell in the grid, the number in the cell is read.

        Args:
            image (np.array): The image of the numeric dB graph

        Returns:
            List[List[str]]: A 10 x 10 matrix containing the values
        """
        #Crops the axis from the image
        image[(floor(image.shape[1]/2)-6):(floor(image.shape[1]/2)+6),:] = 255
        image[:, (floor(image.shape[0]/2)-6):(floor(image.shape[0]/2)+6)] = 255
        
        index = 0
        #Initialize an empty array
        arr = [[0 for i in range(10)] for j in range(10)]

        for i in range(10):
            for j in range(10):
                #Crops a region in the graph
                val_img = Image.fromarray(image[floor(i * image.shape[0] / 10):floor((i+1) * image.shape[0] / 10),floor(j * image.shape[1] / 10):floor((j+1) * image.shape[1] / 10)])
                arr[i][j] = self.readNum(val_img)
        for i in arr:
            print(i)
        print("\n"*3)

        return arr
    def readNum(self, numImg):
        """Reads a short number from an image

        From our experimentation, we found out that Pytesseract performs very poorly on short numerical strings,
        especially negative numbers. The main idea of this method was that Pytesseract performs better on longer strings.

        The method first combine the image of the number with the auxiliary image, located in numdB_aux.png. Then 
        the combined image is passed to the OCR engine to extract the text. Finally, the number is filtered from 
        the text using regular expressions

        Args:
            numImg (Image): The image of a number

        Returns:
            str: The number inside the image
        """
        numImg.resize((50, 50))
        images = [self.numdB_aux.copy(), numImg, self.numdB_aux.copy()]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height), color="white")
        
        x_offset = 0
        for im in images:
            y_offset = floor((50 - im.height)/2)
            new_im.paste(im, (x_offset,y_offset))
            x_offset += im.size[0]

        match = self.numdB_pattern.search(self.ocr_num(new_im))
        if match and match.group(1) != "-":
            num = match.group(1)
        else:
            num = ""
        return num

    def grid(self, image):
        """Debugging tool. Shows a 10 x 10 grid on an image

        Args:
            image (Any): The input image
        """
        for i in range(10):
            image[floor(image.shape[1]/10 * i) ,:] = 0
            image[:,floor(image.shape[0]/10 * i)] = 0
            
        Image.fromarray(image).show()