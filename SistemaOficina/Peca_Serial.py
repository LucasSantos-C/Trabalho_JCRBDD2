from dataclasses import asdict, dataclass
import json

@dataclass
class Peca_Serial:
    id: int = 0
    tipo: str = None
    modelo: str = None
    qtd: int = 0

    def para_dict(self):
        return asdict(self)

    def para_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_dict(cls, dados: dict):
        return cls(**dados)
