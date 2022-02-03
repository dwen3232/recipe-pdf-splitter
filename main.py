import os
import sys
from tqdm import tqdm
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from pytesseract import image_to_string

input_dir_path = Path("./inputs")
output_dir_path = Path("./outputs")

if __name__ == '__main__':
    # get all file paths in input directory
    input_file_paths = [f for f in input_dir_path.iterdir() if f.is_file() and f.suffix == ".pdf"]
    if not input_file_paths:
        sys.exit("'inputs' directory empty")
    for file_path in input_file_paths:
        with open(file_path, 'rb') as in_stream:
            print(f"Splitting {file_path}...")

            # make directory for this pdf
            output_pages_path = output_dir_path / str(file_path.stem)
            if not output_pages_path.is_dir():
                os.mkdir(output_pages_path)

            # initialize pdf reader and PIL images for ocr
            pdf = PdfFileReader(in_stream)
            pdf_images = convert_from_path(file_path)

            # create new pdf for each page
            for i in tqdm(range(pdf.getNumPages())):
                # use tesseract ocr to find top-level line
                page_image = pdf_images[i]
                ocr_string = image_to_string(page_image, lang='eng')

                # strip first line of whitespace and replace backslashes
                page_name = ocr_string.strip().split('\n')[0].replace('/', '|')

                # to guarantee that recipes aren't overwritten, and that duplicates are saved
                if (output_pages_path / f"{page_name}.pdf").exists():
                    version = 2
                    while (output_pages_path / f"{page_name}v{version}.pdf").exists():
                        version += 1
                    page_name = f"{page_name}v{version}"

                # write to output directory
                writer = PdfFileWriter()
                writer.addPage(pdf.getPage(i))
                with open(output_pages_path / f"{page_name}.pdf", "wb") as out_stream:
                    writer.write(out_stream)

    sys.exit("Finished split with no errors")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
