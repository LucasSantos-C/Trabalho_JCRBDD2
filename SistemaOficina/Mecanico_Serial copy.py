from dataclasses import asdict, classmethod
import json

class PecaCarro_Serial:
    def __init__(self, id_peca, peca_carro, qtdpeca):
        self.id_peca = id_peca
        self.peca_carro = peca_carro
        self.qtdpeca = qtdpeca

    def para_dict(self) -> dict:
        return asdict(self)
        
    def para_json(self) -> dict:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict) -> "PecaCarro_Serial":
        return cls(**dados)