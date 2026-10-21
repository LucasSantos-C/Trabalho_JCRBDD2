from dataclasses import asdict, classmethod
import json

class Mecanico_Serial:
    def __init__(self, data_abertura, data_fechamento, id_atendimento, desc_atendimento):
        self.data_abertura = data_abertura
        self.data_fechamento = data_fechamento
        self.id_atendimento = id_atendimento
        self.desc_atendimento = desc_atendimento

    def para_dict(self) -> dict:
        return asdict(self)
            
    def para_json(self) -> dict:
        return json.dumps(asdict(self), ensure_ascii=False)
        
    @classmethod
    def de_dict(cls, dados: dict) -> "Mecanico_Serial":
        return cls(**dados)