from dataclasses import asdict, dataclass
import json

@dataclass
class Cliente_Serial:
    def __init__(self, cpf=None, nome=None, telefone=None, endereco=None):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco


    def para_dict(self) -> dict:
        return asdict(self)
    
    def para_json(self) -> dict:
            return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def de_dict(cls, dados: dict) -> "Cliente_Serial":
         return cls(**dados)
