# VFTReader

Welcome to Visual Field Test reader! The application can be used to automatically extract information from images of VFT reports, as well as viewing
and editing them manually.

The main application is located at 'launcher.py'. For a version that is independent from the Python interpreter, run the application located at 'dist/launcher/launcher.exe'

Documentations are located at 'docs'. For the main documentation page, please open 'docs/build/html/index.html'. Several diagrams are located at 'docs/diagrams' to aid you in
understanding the structure of the project.

Due to time constraint, and the author's proficiency at the time, the application can only function with a strict format for VFT reports. The folder 'docs/sample images' contains a few '_template.png' files, which shows the locations that the application will look for information. The folder also contains several '_sample.png' files, which are
reports that have been resized to the correct size. The "docs/test data" directory contains test reports that the program was able to perform relatively accurate on. You may preprocess your data such that all information fields in your data are in the same relative location as the fields in the test reports.

# Acknowledgement

All files within 'poppler-0.68.0_x86' and 'Tesseract-OCR' are external frameworks, and not the author's original work.
