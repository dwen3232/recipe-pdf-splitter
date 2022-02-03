### Recipe PDF Splitter
Simple hack for splitting a large PDF of recipes that I made for my girlfriend.  PyPDF2 is used to read, split, and write the PDF pages; Tesseract OCR is used to extract the recipe name, so that the new PDF is properly named.  Currently, does not handle multi-page recipes.
To use, first install the python dependencies
```
pip install -r requirements.txt
```
Next, on Ubuntu, install the pytesseract dependencies
```
sudo apt-get install -y tesseract-ocr
```
Refer to https://pypi.org/project/pytesseract/ for more detailed instructions
