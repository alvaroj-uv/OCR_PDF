import fitz
import pytesseract
import io
from PIL import Image, ImageDraw, ImageFont
#import easyocr
#import numpy as np
import time
from pytesseract import Output
import cv2

class OCRHandler:
    def __init__(self):
 #       self.reader = easyocr.Reader(['es'])
        pass

    def get_text_from_image(self,img):
  #      return self.reader.readtext(np.array(img), detail = 0)
        return pytesseract.image_to_string(img, lang='spa',config='--psm 4 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+.')




class PdfHandler:
    def __init__(self,input_pdf_file):
        self.input_pdf=input_pdf_file
        self.original_image = None
        self.pix = None
        self.doc = fitz.open(self.input_pdf)

    def get_image_from_page(self,num_page):
        zoom_x = 3.0  # horizontal zoom
        zoom_y = 3.0  # vertical zoom
        self.pix = self.doc.loadPage(num_page).getPixmap(matrix=fitz.Matrix(zoom_x, zoom_y), colorspace=fitz.csGRAY,
                             clip=fitz.IRect(15, 78, 535, 590), alpha=False, annots=False)
        return Image.open(io.BytesIO(self.pix.getPNGdata()))


class Outputhandler:
    def __init__(self):
        self.filename='output.txt'
        self.file =open(self.filename, "w+", encoding='utf-8')
        pass
    def write(self,textohoja):
        self.file.write(textohoja.replace('\n\n', '\n').replace('\x0C', ''))

    def __del__(self):
        self.file.close()

class ImageHandler:

    def __init__(self):
        self.img_separator=None
        self.original_image=None
        self.treated_image=None

    def get_clean_image2(self,dirty_image):
        def funclimp(p):
            if p > 175:
                return 255
            else:
                return p

        return Image.eval(dirty_image, funclimp)

    def get_concat_h(self,input_imglist):
        def merge(imgmergelist):
            new_width = 0
            for img_for_merge in imgmergelist:
                new_width = new_width + img_for_merge.width
            dst = Image.new('L', (new_width, imgmergelist[0].height))
            paste_width = 0
            for img_for_merge in imgmergelist:
                if paste_width == 0:
                    dst.paste(img_for_merge, (0, 0))
                else:
                    dst.paste(img_for_merge, (paste_width, 0))
                paste_width = paste_width + img_for_merge.width
            return dst

        def putsymbol(sourceimage): #hay que pensar en otra alternativa
            fnt = ImageFont.truetype("arial.ttf", 15)
            if self.img_separator is None:
                self.img_separator = Image.new('L', (15, sourceimage.height), 255)
                d2 = ImageDraw.Draw(self.img_separator)
                advance = 1
                for linea in range(154):
                    d2.text((2, advance), "+", font=fnt, fill=0)
                    advance = advance + 18
            return merge([self.get_clean_image2(sourceimage), self.img_separator])

        for i,img in enumerate(input_imglist):
            input_imglist[i]=putsymbol(img)

        return merge(input_imglist)

    def reorderimage(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.get_clean_image2(self.original_image).save(timestr+'ori.clea.png')
        img = cv2.imread(timestr+'ori.clea.png')
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(timestr+'cuadro.ori.clea.png',img)




        height_img = self.original_image.height
        width_img = self.original_image.width
        imagen_nombre = self.original_image.crop((10, 0, 500, height_img))
        imagen_rut = self.original_image.crop((720, 0, 830, height_img))
        imagen_sexo =self.original_image.crop((835, 0, 915, height_img))
        imagen_domicilio = self.original_image.crop((920, 0, width_img, height_img))
        self.treated_image = self.get_concat_h([imagen_rut, imagen_nombre, imagen_sexo,imagen_domicilio])
        self.treated_image.save(timestr+'.png')

    def treat_image(self,input_image):
        self.original_image=input_image
        self.reorderimage()
        return self.treated_image


class PdfToFile:
    def __init__(self, inputpdffile, hojas):
        self.pdffile = inputpdffile
        self.numhojas = hojas
        self.imagehandler=ImageHandler()
        self.OCR=OCRHandler()
        self.PDF=PdfHandler(self.pdffile)
        self.File=Outputhandler()

    def process(self):

        for hoja in range(0, self.numhojas):
            imagen_hoja=self.PDF.get_image_from_page(hoja)
            imagen_hoja_tratada=self.imagehandler.treat_image(imagen_hoja)
            texto_hoja =self.OCR.get_text_from_image(imagen_hoja_tratada)
            self.File.write(texto_hoja)
            print('Hoja'+str(hoja))


prueba = PdfToFile('A05109.pdf',2)
prueba.process()
