"""Contains several constants that will be used inside the application

    Attributes:
        PROJECT_NAME: The name of the project. Will be used for the name of the main application window.
        LOG_WINDOW_NAME: The name of the logs window.
        MAIN_WINDOW_GEOMETRY: The size of the main application window.
        LOG_WINDOW_GEOMETRY: The size of the logs window.
        POPPLER_PATH: Path to poppler, an external framework for processing .pdf files.
        PYTESSERACT_PATH: Path to tesseract, an external OCR engine for extracting data from images.


"""

PROJECT_NAME = " VFTReader"
LOG_WINDOW_NAME = "Logs"
POPPLER_PATH = "poppler-0.68.0_x86/poppler-0.68.0/bin"
PYTESSERACT_PATH  = "Tesseract-OCR/tesseract.exe"
MAIN_WINDOW_GEOMETRY = "1000x600+200+200"
LOG_WINDOW_GEOMETRY = "500x200+800+400"