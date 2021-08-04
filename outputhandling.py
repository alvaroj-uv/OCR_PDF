class Outputhandler:
    def __init__(self):
        self.filename = 'output.txt'
        self.file = open(self.filename, "w+", encoding='utf-8')
        pass

    def write(self, procesador):
        if isinstance(procesador, EasyOCR):
            for ele in procesador.textohoja:
                self.file.write(ele + '\n')
        else:
            self.file.write(procesador.textohoja.replace('\n\n', '\n').replace('\x0C', ''))

    def __del__(self):
        self.file.close()