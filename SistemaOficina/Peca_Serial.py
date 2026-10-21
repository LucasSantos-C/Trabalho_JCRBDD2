from dataclasses import dataclass, asdict
import json

class Peca_Serial:
    def __init__(self,tipo=None, id=0, modelo=None, qtd=0):
        self.tipo = tipo
        self.id = id
        self.modelo = modelo
        self.qtd = qtd

    def para_dict(self) -> dict:
        return asdict(self)

    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_dict(cls, dados: dict) -> "Peca_Serial":
        return cls(**dados)
    