from dataclasses import asdict, dataclass
import json

@dataclass
class Peca_Serial:
    tipo: str = None
    id: int = 0
    modelo: str = None
    qtd: int = 0

    def para_dict(self) -> dict:
        return asdict(self)

    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_dict(cls, dados: dict) -> "Peca_Serial":
        return cls(**dados)
