
import pytesseract
from PIL import Image
import pdf2image
#TODO: Find a way to set the path for pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
def pdf_to_img(pdf_file):
    #TODO: Same for poppler
    return pdf2image.convert_from_path(pdf_file, poppler_path= "C:/Users/HP - PC/Downloads/poppler-0.68.0_x86/poppler-0.68.0/bin")


def ocr_core(file):
    text = pytesseract.image_to_string(file)
    return text


def print_pages(pdf_file):
    images = pdf_to_img(pdf_file)
    for pg, img in enumerate(images):
        print(ocr_core(img))

print_pages("C:/Users/HP - PC/VFTReader/094_R16_20200129_100357_OD_86017011_SFA_R1625-PROMPT_094.Pdf")