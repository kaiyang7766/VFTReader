import math
from math import floor
from models.VFTReport import VFTReport
import os
import re
import cv2
from PIL import Image
import numpy as np
import pdf2image
import pytesseract
import Constants
from tensorflow.keras.models import model_from_json

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")

class HFAv2Reader:
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
        self.patientInfoRegex = {
            "Name": re.compile("Name:\s*(.*)\s*DOB:"),
            "Birth": re.compile("DOB:\s*(.*)"),
            "Gender": re.compile("Gender:\s*(.*)"),
            "ID": re.compile("Patient ID:\s*(.*)"),
            #"FIXMON": re.compile("Fixation Monitor: (.*)"),
            #"FIXTAR": re.compile("Fixation Target: (.*)"),
        }
        self.resultInfoRegex = {
            "GHT": re.compile("GHT\s*\n*(.*)"),
            "VFI": re.compile("VFI\s*(.*)"),
            "MD": re.compile("MD\s*(.*)dB"),
            "MDp": re.compile("MD\s*.*(P\s*<\s*.*%)"),
            "PSD": re.compile("PSD\s*(.*)dB"),
            "PSDp": re.compile("PSD\s*.*(P\s*<\s*.*%)"),
        }
        self.patternRegex = re.compile("24-2|30-2|10-2")
        self.fieldLocations = {
            "FIXLOS": (460,434,598,475),
            "FPR": (490,485,568,527),
            "Duration": (421,595,530,632),
            "FNR": (484,538,583,584),
            "Fovea": (314,677,400,721),
            "Stimulus": (986,323,1132,367),
            "Date": (1907,325,2125,367),
            "Background": (1034,380,1196,422),
            "Time": (1915,382,2075,424),
            "Strategy": (985,434,1165,473),
        }
        self.ageLocation = (1901,436,1977,475)
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
        img =img.resize((2400, 3180))
        thresh = 200
        fn = lambda x : 255 if x > thresh else 0
        img = img.convert('L').point(fn)
        arr = np.array(img)

        #Crop regions of interests
        sensGraph = img.crop((550, 615, 1270, 1365))
        MDGraph = img.crop((305, 1370, 795, 1910))
        PSDGraph = img.crop((1038, 1370, 1525, 1910))
        resultInfo = img.crop((1614, 1560, 2045, 1916))
        eyeLabel = img.crop((1787, 80, 1884, 121))
        patientInfo = img.crop((220, 136, 2104, 229))    
        patternInfo = img.crop((202, 247, 653, 286))
        
        #Extract text from cropped regions
        try:
            self.values["Pattern"] = self.patternRegex.search(self.ocr_core(patternInfo)).group(0)
        except:
            self.values["Pattern"] = self.patternRegex.search(self.ocr_core(patternInfo))
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

        #eyeLabel = eyeLabel.convert("1")
        eye = self.ocr_core(eyeLabel)
        #if "os" in eye.lower():
        #    eye = "Left"
        #elif "od" in eye.lower():
        #    eye= "Right"
        #else:
        #    eye = ""
        
        sensGraph_arr = np.array(sensGraph)
        #remove axis
        sensGraph_arr[(floor(sensGraph_arr.shape[0]/2)-9):(floor(sensGraph_arr.shape[0]/2)+18),:] = 255
        sensGraph_arr[:, (floor(sensGraph_arr.shape[1]/2)-6):(floor(sensGraph_arr.shape[1]/2)+8)] = 255
        #special points whitening
        sensGraph_arr[350:370,120:130]=255
        sensGraph_arr[350:370,588:598]=255
        sensGraph_arr[350:370,700:730]=255
        MDGraph_arr = np.array(MDGraph)         
        PSDGraph_arr = np.array(PSDGraph)

        #FIXLOS and FIXTST gets special treatment due to FIXTST needing to be interpreted from Fixation Losses
        try:
            FIXLOS, FIXTST = self.values["FIXLOS"].split("/")
        except ValueError:
            FIXLOS = self.values["FIXLOS"]
            FIXTST = ""
        return VFTReport(filename,self.values["Name"], eye, self.values["Date"] + " " + self.values["Time"], self.values["Age"], self.values["Birth"], self.values["ID"], FIXLOS, FIXTST, self.values["FNR"], self.values["FPR"], self.values["Duration"],self.values["GHT"], self.values["VFI"], self.values["MD"], self.values["MDp"], self.values["PSD"], self.values["PSDp"],  self.values["Pattern"], self.values["Strategy"], self.values["Stimulus"], self.values["Background"], self.values["Fovea"] ,self.graph2data(sensGraph_arr,sens=True), self.graph2data(MDGraph_arr), self.graph2data(PSDGraph_arr), 0)

    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), int(height))

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            if int(h * r) <28:
                dim=(int(width),int(height))
            else:
                dim = (int(width), int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def sharpen(self,img:np.array):
        kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]])
        return cv2.filter2D(src=img, ddepth=-2, kernel=kernel)

    def rotate90clockwise(self,img:np.array):
        n=len(img)
        for y in range(n):
            for x in range(y):
                img[y][x],img[x][y]=img[x][y],img[y][x]
        for i in range(n):
            img[i]=img[i][::-1]
        return img

    def inversepixel(self,img:np.array):
        n=len(img)
        for y in range(n):
            for x in range(n):
                if img[y][x]==0:
                    img[y][x]=True
                else:
                    img[y][x]=False
        return img

    def findcontour(self,img:np.array,sens=False):
        n=len(img)
        if sens==False:
            dim=[]
            temp=[]
            width=0
            for y in range(n):
                if any(img[y]):
                    if width==0:
                        temp.append(y-1)
                    width+=1
                elif width>0:
                    if width<10:
                        temp.append(width+1)
                        width=0
                        dim.append(temp)
                        temp=[]
                    else:
                        width=math.ceil(width/2)
                        temp.append(width+1)
                        x,w=temp
                        dim.append(temp)
                        dim.append([x+w,w])
                        width=0
                        temp=[]
            return dim
        else:
            dim=[]
            temp=[]
            width=0
            for y in range(n):
                if any(img[y]):
                    if width==0:
                        temp.append(y-1)
                    width+=1
                elif width>0:
                    if width<6:
                        temp.append(width+1)
                        width=0
                        dim.append(temp)
                        temp=[]
                    else:
                        width=math.ceil(width/2)
                        temp.append(width+1)
                        x,w=temp
                        dim.append(temp)
                        dim.append([x+w,w])
                        width=0
                        temp=[]
            return dim

    def cnn_read(self,image,model,sens):
        img_arr=np.array(image)
        img_arr=self.image_resize(img_arr,28,28)
        img_arr=img_arr[:28]
        #make 3px border top bottom and 2px border left right white
        img_arr[0]=img_arr[1]=img_arr[2]=img_arr[25]=img_arr[26]=img_arr[27]=255 #top bottom
        for y in img_arr: #left right
            y[0]=y[1]=y[26]=y[27]=255

        sharp_img=self.sharpen(img_arr)
        rotate_img=self.rotate90clockwise(sharp_img)
        inverse_img=self.inversepixel(rotate_img)
        cnts=self.findcontour(inverse_img,sens)

        string=''
        for c in cnts:
            #white background
            wb=np.ones((28,28))*255
            #find the bounding area
            x,w=c
            #paste region of interest
            wb[:,x:x+w]=img_arr[:,x:x+w]
            wb=wb.astype('float32')
            wb/=255
            wb=wb.reshape(-1,28,28,1)
            #predict the pasted image
            result=np.argmax(model.predict(wb))
            if result==10:
                result='-'
            if result==11:
                result='<'
            string+=str(result)
        if string=='':
            return
        
        #return int(float(string))
        try:
            return int(string)
        except:
            return string

    def graph2data(self,image:np.array,sens=False):
        #Initialize an empty array
        arr = [[0 for i in range(10)] for j in range(10)]

        for i in range(10):
            for j in range(10):
                #Crops a region in the graph
                val_img = Image.fromarray(image[floor(i * image.shape[0] / 10):floor((i+1) * image.shape[0] / 10),floor(j * image.shape[1] / 10):floor((j+1) * image.shape[1] / 10)])
                #print(plt.imshow(val_img,cmap='gray'))
                arr[i][j] = self.cnn_read(val_img,loaded_model,sens)
    #     for i in arr:
    #         print(i)
    #     print("\n"*3)

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