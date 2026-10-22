from dataclasses import asdict, dataclass
import json

@dataclass
class PecaCarro_Serial:
    id_peca: int = None
    peca_carro: str = None
    qtdpeca: int = 0

    def para_dict(self):
        return asdict(self)
        
    def para_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict):
        return cls(**dados)
