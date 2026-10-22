from dataclasses import asdict, dataclass
import json

@dataclass
class Mecanico_Serial:
    def __init__(self, id, nome, telefone, especialidade):
        self.id = id
        self.nome = nome
        self.telefone = telefone
<<<<<<< HEAD:SistemaOficina/Mecanico_Serial copy.py
        self.especilidade = especialidade
=======
        self.especialidade = especialidade
>>>>>>> e27347e81f2350821c7457913e646e512e495dbb:SistemaOficina/Mecanico_Serial.py

    def para_dict(self) -> dict:
        return asdict(self)
        
    def para_json(self) -> dict:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def de_dict(cls, dados: dict) -> "Mecanico_Serial":
        return cls(**dados)
