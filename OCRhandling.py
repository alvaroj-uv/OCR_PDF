import pytesseract
import easyocr
import numpy as np

class OCRHandler:
    def __init__(self):
        pass

    def get_text_from_image(self, img):
        pass


class TesseractOCR(OCRHandler):
    def get_text_from_image(self, img):
        self.textohoja = pytesseract.image_to_string(img, lang='spa',
                                                     config='--psm 4 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+.')


class EasyOCR(OCRHandler):
    def __init__(self):
        self.reader = easyocr.Reader(['es'])

    def get_text_from_image(self, img):
        self.textohoja = self.reader.readtext(np.array(img), detail=0)