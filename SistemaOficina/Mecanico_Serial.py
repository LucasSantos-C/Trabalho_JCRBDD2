from dataclasses import asdict, dataclass
import json

@dataclass
class Mecanico_Serial:
    id: int = None
    nome: str = None
    telefone: str = None
    especialidade: str = None

    def para_dict(self) -> dict:
        return asdict(self)
        
    def para_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict) -> "Mecanico_Serial":
        return cls(**dados)
