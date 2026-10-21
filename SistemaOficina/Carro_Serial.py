from dataclasses import asdict, dataclass
import json

@dataclass
class Carro_Serial:
    def __init__(self, modelo, cor, placa, ano, marca):
        self.modelo = modelo
        self.cor = cor
        self.placa = placa
        self.ano = ano
        self.marca = marca

    def para_dict(self) -> dict:
        return asdict(self)
        
    def para_json(self) -> dict:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict) -> "Carro_Serial":
        return cls(**dados)