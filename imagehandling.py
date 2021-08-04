

class ImageHandler:

    def __init__(self):
        self.img_separator = None
        self.original_image = None
        self.treated_image = None

    def get_clean_image2(self, dirty_image):
        def funclimp(p):
            if p > 175:
                return 255
            else:
                return p

        return Image.eval(dirty_image, funclimp)

    def get_concat_h(self, input_imglist):
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

        def putsymbol(sourceimage):  # hay que pensar en otra alternativa
            fnt = ImageFont.truetype("arial.ttf", 15)
            if self.img_separator is None:
                self.img_separator = Image.new('L', (15, sourceimage.height), 255)
                d2 = ImageDraw.Draw(self.img_separator)
                advance = 1
                for linea in range(154):
                    d2.text((2, advance), "+", font=fnt, fill=0)
                    advance = advance + 18
            return merge([self.get_clean_image2(sourceimage), self.img_separator])

        for i, img in enumerate(input_imglist):
            input_imglist[i] = putsymbol(img)

        return merge(input_imglist)

    def reorderimage(self):
        #timestr = time.strftime("%Y%m%d-%H%M%S")
        height_img = self.original_image.height
        width_img = self.original_image.width
        imagen_nombre = self.original_image.crop((10, 0, 500, height_img))
        imagen_rut = self.original_image.crop((720, 0, 830, height_img))
        imagen_sexo = self.original_image.crop((835, 0, 915, height_img))
        imagen_domicilio = self.original_image.crop((920, 0, width_img, height_img))
        self.treated_image = self.get_concat_h([imagen_rut, imagen_nombre, imagen_sexo, imagen_domicilio])
        #self.treated_image.save(timestr + '.png')

    def treat_image(self, input_image):
        self.original_image = input_image
        self.reorderimage()
        return self.treated_image
