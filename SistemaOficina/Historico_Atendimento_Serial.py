from dataclasses import asdict, dataclass
import json

@dataclass
class Historico_Atendimento_Serial:
    id_atendimento: int = None
    data_abertura: str = None
    data_fechamento: str = None
    desc_atendimento: str = None

    def para_dict(self):
        return asdict(self)
            
    def para_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)
        
    @classmethod
    def de_dict(cls, dados: dict):
        return cls(**dados)
