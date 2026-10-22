from dataclasses import asdict, dataclass
import json

@dataclass
class Cliente_Serial:
    cpf: str = None
    nome: str = None
    telefone: str = None
    endereco: str = None

    def para_dict(self) -> dict:
        return asdict(self)
    
    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_dict(cls, dados: dict) -> "Cliente_Serial":
        return cls(**dados)
