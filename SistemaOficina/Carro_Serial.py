from dataclasses import asdict, dataclass
import json

@dataclass
class Carro_Serial:
    placa: str = None
    modelo: str = None
    cor: str = None
    ano: int = None
    marca: str = None

    def para_dict(self):
        return asdict(self)
        
    def para_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict):
        return cls(**dados)
