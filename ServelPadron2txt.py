import fitz
import pytesseract
import io
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np
import time


class PdfHandler:
    def __init__(self, input_pdf_file):
        self.input_pdf = input_pdf_file
        self.original_image = None
        self.pix = None
        self.doc = fitz.open(self.input_pdf)

    def get_image_from_page(self, num_page):
        zoom_x = 3.0  # horizontal zoom
        zoom_y = 3.0  # vertical zoom
        self.pix = self.doc.loadPage(num_page).getPixmap(matrix=fitz.Matrix(zoom_x, zoom_y), colorspace=fitz.csGRAY,
                                                         clip=fitz.IRect(15, 78, 535, 590), alpha=False, annots=False)
        return Image.open(io.BytesIO(self.pix.getPNGdata()))








