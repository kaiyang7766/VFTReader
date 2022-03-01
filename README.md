# VFTReader

Welcome to Visual Field Test reader! The application can be used to automatically extract information from images of VFT reports, as well as viewing
and editing them manually.

The main application is located at 'launcher.py'. For a version that is independent from the Python interpreter, run the application located at 'dist/launcher/launcher.exe'

Documentations are located at 'docs'. For the main documentation page, please open 'docs/build/html/index.html'. Several diagrams are located at 'docs/diagrams' to aid you in
understanding the structure of the project.

<!-- Due to time constraint, and the author's proficiency at the time, the application can only function with a strict format for VFT reports. The folder 'docs/sample images' contains a few '_template.png' files, which shows the locations that the application will look for information. The folder also contains several '_sample.png' files, which are
reports that have been resized to the correct size. The "docs/test data" directory contains test reports that the program was able to perform relatively accurate on. You may preprocess your data such that all information fields in your data are in the same relative location as the fields in the test reports. -->

## Mechanisms of VFTReader
The conventional alphabet wordings are read by using the pre-built Python library pytesseract. However, it is challenging to read an axis of graph like below:

![axisgraphraw](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/axisgraphraw.PNG)

The raw axis of graph is cleaned and preprocessed by the following steps:
1) Removing the x-axis and y-axis.
2) Removing noise symbols such as triangles.
3) Adding a 10x10 grid to separate the individual groups of digits.

Now the resultant graph will look like this:

![axisgraphcleaned](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/axisgraphcleaned.PNG)

A CNN model will be used to read the digits and symbols within each grid.

## Convolutional Neural Network (CNN) Strategy
Each grid can either contain digits or a null value. A CNN model is trained (see section below on how this model is trained) to recognize the digits and symbols from each grid.

Taking a look at one specific grid value:

![gridnumber27](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/gridnumber27.PNG)

The model should give us the number 27, but the CNN model is only trained on recognizing single digit or symbol, thus image contouring should be applied to seperate the digits. The strategies to do so are as follow:
### 1) As the image is rather blurry, image sharpening is first applied to the digits:
```
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
```
This will produce a sharper image as below:

![gridnumber27sharpend](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/gridnumber27sharpened.PNG)

Sharpen image allows the method later to detect the digit separation easier using pixel threshold value. Note that the conventional Canny edge detection which involves blurring the image first does not work well here due to distance of digits being too close to each other. You can have a read at the Canny edge detection [here](https://www.thepythoncode.com/article/contour-detection-opencv-python).

### 2) With the sharpened image, digit separation can be achieved by 3 steps:
a) Rotate the entire image clockwise by 90 degrees：
```
def rotate90clockwise(img:np.array):
    n=len(img)
    for y in range(n):
        for x in range(y):
            img[y][x],img[x][y]=img[x][y],img[y][x]
    for i in range(n):
        img[i]=img[i][::-1]
    return img
```
b) Convert the pixel values to Boolean inversely, such that 255=False, 0=True:
```
def inversepixel(img:np.array):
    n=len(img)
    for y in range(n):
        for x in range(n):
            if img[y][x]==0:
                img[y][x]=True
            else:
                img[y][x]=False
    return img
```
c) Find the contour by identifying the width of each dimension found based on the Boolean values converted previously:
```
def findcontour(img:np.array,sens=False):
    n=len(img)
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
            else: #if width is wrongly assigned to value of 6 or larger, force the width to divide by 2 as we know single digit width will not be larger than 6
                width=math.ceil(width/2)
                temp.append(width+1)
                x,w=temp
                dim.append(temp)
                dim.append([x+w,w])
                width=0
                temp=[]
    return dim
```
### 3) Drawing the width found in a rectangle, the image separation is found as below:
![gridnumber27separated](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/gridnumber27separated.PNG)

The CNN model can now predict the individual digit based on the separation indicated by the red rectangles.

## Convolutional Neural Network (CNN) Training
As the digits font used in VFT Reports are Arial, the data used to train the CNN model is Arial font from 0 to 9 with symbols like negative sign "-" and "<".

ImageDataGenerator is used to create 200,000 more data with different rotation, width shift, height shift, shear and zoom:
![ImageDataGenerator](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/ImageDataGenerator.PNG)

The keras CNN model is built with 8 layers as follow:

![kerasmodel](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/kerasmodel.PNG)

The model is compiled with adam optimizer, with loss calculation using CategoricalCrossentropy as each digit is treated as a category.

The model is trained with batch size of 128 and epochs of 10, the resulting prediction accuracy is up to 99.58%:
![trainingaccuracy](https://raw.githubusercontent.com/kaiyang7766/VFTReader/main/docs/readmepics/trainingaccuracy.PNG)

# Acknowledgement

This project is jointly created by the previous intern [Luong-Minh-Quang](https://github.com/Luong-Minh-Quang/) and myself. All files within 'poppler-0.68.0_x86' and 'Tesseract-OCR' are external frameworks, and not the author's original work.
