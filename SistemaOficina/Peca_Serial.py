class Peca_Serial:
    def __init__(self,tipo=None, id=0, modelo=None, qtd=0):
        self.tipo = tipo
        self.id = id
        self.modelo = modelo
        self.qtd = qtd

    def getTipo(self):
        return self.tipo

    def getId(self):
        return self.id

    def getModelo(self):
        return self.modelo

    def getQtd(self):
        return self.qtd