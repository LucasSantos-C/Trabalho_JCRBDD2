from dataclasses import asdict, dataclass
import json

@dataclass
class Carro_Serial:
    modelo: str = None
    cor: str = None
    placa: str = None
    ano: int = None
    marca: str = None

    def para_dict(self) -> dict:
        return asdict(self)
        
    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict) -> "Carro_Serial":
        return cls(**dados)
