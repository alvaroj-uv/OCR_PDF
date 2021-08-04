from PDFhandling import ImageHandler,OCRHandler,EasyOCR,PdfHandler,Outputhandler

class PdfToFile:
    def __init__(self, inputpdffile, hojas):
        self.pdffile = inputpdffile
        self.numhojas = hojas
        self.imagehandler = ImageHandler()
        self.OCR = EasyOCR()
        self.PDF = PdfHandler(self.pdffile)
        self.File = Outputhandler()

    def process(self):
        for hoja in range(0, self.numhojas):
            imagen_hoja = self.PDF.get_image_from_page(hoja)
            imagen_hoja_tratada = self.imagehandler.treat_image(imagen_hoja)
            self.OCR.get_text_from_image(imagen_hoja_tratada)
            self.File.write(self.OCR)
            print('Hoja' + str(hoja))


prueba = PdfToFile('A02103.pdf',2)
prueba.process()