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
import Constants
class HFAv2Reader:
    """Extraction algorithm for HFAv3 reports.
    
    Attributes:
        patterns: Regular expressions for filtering information from raw text
        numdB_pattern: Regular expressions for numeric dB graph values, after preprocessing.
        numdB_aux: An auxiliary image used to enhance accuracy. See readNum for more information
    """
    def __init__(self) -> None:
        #TODO: Find a way to set the path for pytesseract
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        
        self.patterns = {
            "Eye": re.compile("Eye: (.*)"),
            "Name": re.compile("Name:\s*(.*)\s*DOB:"),
            "Birth": re.compile("DOB:\s*(.*)"),
            "Gender": re.compile("Gender:\s*(.*)"),
            "ID": re.compile("Patient ID:\s*(.*)"),
            #"FIXMON": re.compile("Fixation Monitor: (.*)"),
            #"FIXTAR": re.compile("Fixation Target: (.*)"),
            "FIXLOS": re.compile("Fixation Losses:\s*(.*)\s*Strategy:"),
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
        """Converts a .pdf file to an Image

        Args:
            pdf_file (str): The path to the file

        Returns:
            List: The pages of the pdf file
        """
        return pdf2image.convert_from_path(pdf_file,dpi = 500, poppler_path= Constants.POPPLER_PATH)

    def ocr_num(self, image):
        """Extracts the text from a preprocessed image of a numeric dB graph value

        Due to the limitations of Pytesseract, different configurations were needed for short numerical values.

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(image, config= "--psm 7 -c tessedit_char_whitelist=FIELD-<0123456789")
        return text

    def ocr_core(self, file):
        """Extracts the text from an image

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(file)
        return text
    def ocr_main_graph(self, image):
        """Extracts the text from a preprocessed image of the main numeric dB graph values

        Due to the limitations of Pytesseract, different configurations were needed for short numerical values.

        Args:
            image (Image): The input image

        Returns:
            str: The text inside the image
        """
        text = pytesseract.image_to_string(image, config= "--psm 7 -c tessedit_char_whitelist=FIELD-<0123456789 CONFIGFILE=VFTgraph")
        return text
    
    def readImage(self, dir, filename):
        """Extracts the information from an VFT report

        We assumed that all information fields will be in the same relative location for all reports.
        The method first resizes the image to the same size as our test data. Secondly, several parts
        of the image are cropped and passed to the OCR engine to extract the information. Thirdly,
        several parts of the image were deleted, leaving only the text at the top of the report, which will
        also be passed to the OCR engine. Finally, the information are combined into a VFTReport object, 
        which will be returned by the method.

        Note:
            Short numeric values, such as the patient's age, and values in numeric dB graphs are treated
            differently than normal strings. See readNum for how we processes these values.

        Args:
            dir (str): The directory leading to the file.
            filename (str): The name of the file.

        Returns:
            VFTReport: The VFT report in the image.
        """
        file = os.path.join(dir, filename)
        
        if filename.endswith(".Pdf") or filename.endswith(".pdf"):
            images = self.pdf_to_img(file)
            img = images[0]
        else:
            img = Image.open(file)    
        #Resize image
        img = img.resize((4250, 5500))
        arr = np.array(img)
        #Crop graphs
        sensGraph = img.crop((1038, 1050, 2232, 2463))
        MDGraph = img.crop((633,2383, 1455, 3292))
        PSDGraph = img.crop((1866, 2383, 2658, 3292))
        resultInfo = img.crop((2660, 2660, 4000, 3500))

        #Delete axis from sensitivity graph, as it is different than the 2 remaining graphs
        sensGraph_arr = np.array(sensGraph)
        sensGraph_arr[683:738, :] = 255
        sensGraph_arr[:, 583:625] = 255
        sensGraph = Image.fromarray(sensGraph_arr)
        
        MDGraph_arr = np.array(MDGraph)
        PSDGraph_arr = np.array(PSDGraph)
        #Delete unnecessary parts of the VFT report 
        arr[1050:1800, 1038:] = 255
        arr[1800:, :] = 255
        cropped = Image.fromarray(arr)

        #Extract the text from the cropped images
        main_text = self.ocr_core(cropped)
        print(main_text)
        
        test_result_text = self.ocr_core(resultInfo)
        print(test_result_text)
        fulltext = main_text + "\n" + test_result_text
        #Filter information using regex
        for k, v in self.patterns.items():
            match = v.search(fulltext)
            if match:
                self.values[k] = match.group(1)
            else:
                self.values[k] = ""
        #FIXLOS and FIXTST gets special treatment due to FIXTST needing to be interpreted from Fixation Losses
        try:
            FIXLOS, FIXTST = self.values["FIXLOS"].split("/")
        except ValueError:
            FIXLOS = self.values["FIXLOS"]
            FIXTST = ""
        return VFTReport(filename,self.values["Name"], self.values["Eye"], self.values["Date"] + " " + self.values["Time"], self.values["Age"], self.values["Birth"], self.values["ID"], FIXLOS, FIXTST, self.values["FNR"], self.values["FPR"], self.values["Duration"],self.values["GHT"], self.values["VFI"], self.values["MD"], self.values["MDp"], self.values["PSD"], self.values["PSDp"],  self.values["Pattern"], self.values["Strategy"], self.values["Stimulus"], self.values["Background"], self.values["Fovea"] ,self.HFAv2mainGraph2data(sensGraph_arr), self.image2data(MDGraph_arr), self.image2data(PSDGraph_arr), 0)


    def image2data(self, image):
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
        #Removes the axis
        image[(floor(image.shape[0]/2)-6):(floor(image.shape[0]/2)+6),:] = 255
        image[:, (floor(image.shape[1]/2)-6):(floor(image.shape[1]/2)+6)] = 255
        

        arr = [[0 for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                #Crops a region
                cell = image[floor(i * image.shape[0] / 10):floor((i+1) * image.shape[0] / 10),floor(j * image.shape[1] / 10):floor((j+1) * image.shape[1] / 10)]
                val_img = Image.fromarray(cell)
                #Combines the image with the auxiliary image
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
                #Extracts the text from combined image
                val = self.ocr_num(new_im)
                #Retrieves the value
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
        """Converts an image of the numeric dB graph to its representation inside the application.

        For HFAv2 formats, the main numeric dB graph required additional preprocessing to achieve
        a relatively acceptable accuracy.

        The image needs to have its axis removed beforehand. Next, the image was split into the upper
        and lower halves. Next, each half was split into a 10 x 19 grid. This was to ensure that the number
        fills the majority of each cell, to enhance the accuracy of Pytesseract. After the values were extracted
        from each cell, the values from both half were combined and condensed into a 10 x 10 matrix. 

        Note:
            Overall, the accuracy of the algorithm when processing this graph were lower as 
            compared to graphs from HFAv3 reports.
            Furthermore, the character '<0' were consistently misread during our own testing,
            due to the font in which the reports were written. The number reading method as 
            seen in HFAv3Reader did not seem to improve the accuracy significantly.
            

        Args:
            image (np.array): The image of the numeric dB graph

        Returns:
            List[List[str]]: A 10 x 10 matrix containing the values
        """
        pattern = re.compile("\S*")

        result = [["" for i in range(10)] for j in range(10)]       
        #Processes the upper half
        for i in range(10):
            for j in range(19):
                if i % 2 == 1 and j%2 == 0:
                    #Crops a region
                    cell = image[floor(i * image.shape[0] / 20):floor((i+1) * image.shape[0] / 20),floor(j * image.shape[1] / 20+image.shape[1] / 40):floor((j+1) * image.shape[1] / 20 + image.shape[1] / 40)]
                    cell_img = Image.fromarray(cell)
                    #Preprocess the image of the number
                    enhancer = ImageEnhance.Sharpness(cell_img)
                    cell_img = enhancer.enhance(3)
                    cell_img = cell_img.convert("1")
                    #Extract the text
                    val = self.ocr_main_graph(cell_img)
                    #Retrieve the value
                    match = pattern.search(val)

                    if match:
                        result[int((i-1)/2)][int(j/2)]  = match.group(0)
                    else:
                        result[int((i-1)/2)][int(j/2)]  = ''
                   
                else:
                    continue
        #Processes the lower half
        for i in range(10, 20):
            for j in range(19):
                if i % 2 == 0 and j % 2 == 0:
                    #Crops a region
                    cell = image[floor(i * image.shape[0] / 20):floor((i+1) * image.shape[0] / 20),floor(j * image.shape[1] / 20+image.shape[1] / 40):floor((j+1) * image.shape[1] / 20 + image.shape[1] / 40)]
                    cell_img = Image.fromarray(cell)
                    #Preprocess the image of the number
                    enhancer = ImageEnhance.Sharpness(cell_img)
                    cell_img = enhancer.enhance(3)
                    cell_img = cell_img.convert("1")
                    #Extract the text
                    val = self.ocr_main_graph(cell_img)
                    #Retrieve the value
                    match = pattern.search(val)

                    if match:
                        result[int((i-1)/2)+1][int(j/2)]  = match.group(0)
                    else:
                        result[int((i-1)/2)+1][int(j/2)]  = ''
                else:
                    continue
        for i in result:
            print(i)
        print("\n"*3)
        return result

    def grid(self, image):
        """Debugging tool. Shows a 10 x 10 grid on an image

        Args:
            image (Any): The input image
        """
        for i in range(20):
            image[floor(image.shape[0]/20 * i) ,:] = 0
            image[:,floor(image.shape[1]/40 + image.shape[1]/20 * i)] = 0
            
        Image.fromarray(image).show()
