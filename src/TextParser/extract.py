import pytesseract
from PIL import Image


def ocr(file_to_ocr):
    im = Image.open(file_to_ocr)
    txt = pytesseract.image_to_string(im)
    return txt
