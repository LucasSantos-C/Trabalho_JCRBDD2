from datetime import datetime
from ObjetoAcessaDados import ObjetoAcessaDados
from Cliente_Serial import Cliente_Serial
from Carro_Serial import Carro_Serial
from Mecanico_Serial import Mecanico_Serial
from Peca_Serial import Peca_Serial
from PecaCarro_Serial import PecaCarro_Serial
from Historico_Atendimento_Serial import Historico_Atendimento_Serial


class Controlador:
    def __init__(self, acesso_dados=None):
        self.bd = acesso_dados or ObjetoAcessaDados()

    @staticmethod
    def _exigir(valor, campo):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ValueError(f"O campo '{campo}' é obrigatório.")

    @staticmethod
    def _validar_quantidade(valor, campo="quantidade", permitir_zero=True):
        try:
            numero = int(valor)
        except (TypeError, ValueError) as erro:
            raise ValueError(f"'{campo}' deve ser um número inteiro.") from erro
        minimo = 0 if permitir_zero else 1
        if numero < minimo:
            raise ValueError(f"'{campo}' deve ser maior ou igual a {minimo}.")
        return numero

    # ---------- Clientes ----------
    def cadastrar_cliente(self, cpf, nome, telefone=None, endereco=None):
        self._exigir(cpf, "CPF")
        self._exigir(nome, "nome")
        self.bd.set(
            "cliente",
            {
                "cpf": cpf.strip(),
                "nome": nome.strip(),
                "telefone": telefone,
                "endereco": endereco,
            },
        )
        return self.buscar_cliente(cpf.strip())

    def listar_clientes(self):
        return [Cliente_Serial.de_dict(c) for c in self.bd.listar_clientes()]

    def buscar_cliente(self, cpf):
        resultado = self.bd.get_por_coluna("cliente", "cpf", cpf)
        return Cliente_Serial.de_dict(resultado[0]) if resultado else None

    def atualizar_cliente(self, cpf, nome, telefone=None, endereco=None):
        self._exigir(cpf, "CPF")
        self._exigir(nome, "nome")
        sucesso = self.bd.update(
            "cliente",
            {
                "cpf": cpf.strip(),
                "nome": nome.strip(),
                "telefone": telefone,
                "endereco": endereco,
            },
            "cpf",
        )
        if not sucesso:
            raise ValueError("Cliente não encontrado.")
        return self.buscar_cliente(cpf.strip())

    def excluir_cliente(self, cpf):
        self.bd.delete("cliente", "cpf", cpf)
        return True

    # ---------- Carros ----------
    def cadastrar_carro(self, placa, modelo, cor=None, ano=None, marca=None):
        self._exigir(placa, "placa")
        self._exigir(modelo, "modelo")
        if ano not in (None, ""):
            try:
                ano = int(ano)
            except (TypeError, ValueError) as erro:
                raise ValueError("O ano deve ser um número inteiro.") from erro
        placa = placa.strip().upper()
        self.bd.set(
            "carro",
            {
                "placa": placa,
                "modelo": modelo.strip(),
                "cor": cor,
                "ano": ano,
                "marca": marca,
            },
        )
        return self.buscar_carro(placa)

    def listar_carros(self):
        return [Carro_Serial.de_dict(c) for c in self.bd.listar_carros()]

    def buscar_carro(self, placa):
        resultado = self.bd.get_por_coluna("carro", "placa", placa.strip().upper())
        return Carro_Serial.de_dict(resultado[0]) if resultado else None

    def atualizar_carro(self, placa, modelo, cor=None, ano=None, marca=None):
        self._exigir(placa, "placa")
        self._exigir(modelo, "modelo")
        if ano not in (None, ""):
            try:
                ano = int(ano)
            except (TypeError, ValueError) as erro:
                raise ValueError("O ano deve ser um número inteiro.") from erro
        placa = placa.strip().upper()
        self.bd.update(
            "carro",
            {
                "placa": placa,
                "modelo": modelo.strip(),
                "cor": cor,
                "ano": ano,
                "marca": marca,
            },
            "placa",
        )
        carro = self.buscar_carro(placa)
        if not carro:
            raise ValueError("Carro não encontrado.")
        return carro

    def excluir_carro(self, placa):
        self._exigir(placa, "placa")
        self.bd.delete("carro", "placa", placa.strip().upper())
        return True

    # ---------- Mecânicos ----------
    def cadastrar_mecanico(self, nome, telefone=None, especialidade=None):
        self._exigir(nome, "nome")
        self.bd.set(
            "mecanico",
            {
                "nome": nome.strip(),
                "telefone": telefone,
                "especialidade": especialidade,
            },
        )
        resultado = self.bd.executar_sql(
            "SELECT id FROM mecanico WHERE nome = ? ORDER BY id DESC LIMIT 1",
            (nome.strip(),),
        )
        identificador = resultado[0]["id"] if resultado else None
        return self.buscar_mecanico(identificador)
        
    def listar_mecanicos(self):
        return [Mecanico_Serial.de_dict(m) for m in self.bd.listar_mecanicos()]

    def buscar_mecanico(self, id_mecanico):
        resultado = self.bd.get_por_coluna("mecanico", "id", id_mecanico)
        return Mecanico_Serial.de_dict(resultado[0]) if resultado else None

    def atualizar_mecanico(self, id_mecanico, nome, telefone=None, especialidade=None):
        self._exigir(nome, "nome")
        self.bd.update(
            "mecanico",
            {
                "id": id_mecanico,
                "nome": nome.strip(),
                "telefone": telefone,
                "especialidade": especialidade,
            },
            "id",
        )
        mecanico = self.buscar_mecanico(id_mecanico)
        if not mecanico:
            raise ValueError("Mecânico não encontrado.")
        return mecanico

    def excluir_mecanico(self, id_mecanico):
        self._exigir(id_mecanico, "ID do mecânico")
        self.bd.delete("mecanico", "id", id_mecanico)
        return True

    # ---------- Peças e estoque ----------
    def cadastrar_peca(self, tipo, modelo=None, qtd=0):
        self._exigir(tipo, "tipo")
        qtd = self._validar_quantidade(qtd, "quantidade")
        self.bd.set(
            "peca", {"tipo": tipo.strip(), "modelo": modelo, "qtd": qtd}
        )
        resultado = self.bd.executar_sql(
            "SELECT id FROM peca WHERE tipo = ? ORDER BY id DESC LIMIT 1",
            (tipo.strip(),),
        )
        identificador = resultado[0]["id"] if resultado else None
        return self.buscar_peca(identificador)

    def listar_pecas(self):
        return [Peca_Serial.de_dict(p) for p in self.bd.listar_pecas()]

    def buscar_peca(self, id_peca):
        resultado = self.bd.get_por_coluna("peca", "id", id_peca)
        return Peca_Serial.de_dict(resultado[0]) if resultado else None

    def atualizar_estoque(self, id_peca, quantidade):
        quantidade = self._validar_quantidade(quantidade, "quantidade")
        self.bd.update("peca", {"id": id_peca, "qtd": quantidade}, "id")
        peca = self.buscar_peca(id_peca)
        if not peca:
            raise ValueError("Peça não encontrada.")
        return peca

    def adicionar_ao_estoque(self, id_peca, quantidade):
        quantidade = self._validar_quantidade(
            quantidade, "quantidade a adicionar", permitir_zero=False
        )
        self.bd.executar_sql(
            "UPDATE peca SET qtd = qtd + ? WHERE id = ?",
            (quantidade, id_peca),
        )
        peca = self.buscar_peca(id_peca)
        if not peca:
            raise ValueError("Peça não encontrada.")
        return peca

    def excluir_peca(self, id_peca):
        self._exigir(id_peca, "ID da peça")
        self.bd.delete("peca", "id", id_peca)
        return True

    # ---------- Peças associadas a carros ----------
    def associar_peca_ao_carro(self, id_peca, placa_carro, quantidade):
        quantidade = self._validar_quantidade(
            quantidade, "quantidade", permitir_zero=False
        )
        self._exigir(placa_carro, "placa do carro")
        placa = placa_carro.strip().upper()
        sql = """
            INSERT INTO peca_carro (id_peca, placa_carro, qtdpeca)
            VALUES (?, ?, ?)
            ON CONFLICT(id_peca, placa_carro)
            DO UPDATE SET qtdpeca = excluded.qtdpeca
        """
        self.bd.executar_sql(sql, (id_peca, placa, quantidade))
        return self.listar_pecas_do_carro(placa)

    def listar_pecas_do_carro(self, placa_carro):
        dados = self.bd.get_pecas_do_carro(placa_carro.strip().upper())
        return [
            PecaCarro_Serial(
                id_peca=p["id"],
                peca_carro=placa_carro.strip().upper(),
                qtdpeca=p["qtdpeca"]
            ) for p in dados
        ]

    # ---------- Atendimentos e histórico ----------
    def registrar_atendimento(
        self, status, id_mecanico, placa_carro, cpf_cliente,
        desc_atendimento="", data_abertura=None
    ):
        self._exigir(status, "status")
        self._exigir(placa_carro, "placa do carro")
        self._exigir(cpf_cliente, "CPF do cliente")

        if not self.buscar_mecanico(id_mecanico):
            raise ValueError("Mecânico não encontrado.")
        if not self.buscar_carro(placa_carro):
            raise ValueError("Carro não encontrado.")
        if not self.buscar_cliente(cpf_cliente):
            raise ValueError("Cliente não encontrado.")

        data_abertura = data_abertura or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        placa = placa_carro.strip().upper()
        cpf = cpf_cliente.strip()

        self.bd.set(
            "atendimento",
            {
                "status": status,
                "id_mecanico": id_mecanico,
                "placa_carro": placa,
                "cpf_cliente": cpf,
            },
        )
        resultado = self.bd.executar_sql(
            "SELECT id FROM atendimento WHERE id_mecanico = ? AND placa_carro = ? AND cpf_cliente = ? ORDER BY id DESC LIMIT 1",
            (id_mecanico, placa, cpf),
        )
        id_atendimento = resultado[0]["id"] if resultado else None

        self.bd.set(
            "historico_atendimento",
            {
                "id_atendimento": id_atendimento,
                "data_abertura": data_abertura,
                "data_fechamento": None,
                "desc_atendimento": desc_atendimento,
            },
        )
        return self.buscar_atendimento(id_atendimento)

    def listar_atendimentos(self):
        return self.bd.listar_atendimentos()

    def buscar_atendimento(self, id_atendimento):
        return self.bd.get_detalhes_atendimento(id_atendimento)

    def atualizar_status_atendimento(self, id_atendimento, status, finalizar=False):
        self._exigir(status, "status")
        if not self.buscar_atendimento(id_atendimento):
            raise ValueError("Atendimento não encontrado.")

        self.bd.update(
            "atendimento", {"id": id_atendimento, "status": status}, "id"
        )
        if finalizar:
            data_fechamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.bd.update(
                "historico_atendimento",
                {
                    "id_atendimento": id_atendimento,
                    "data_fechamento": data_fechamento,
                },
                "id_atendimento",
            )
        return self.buscar_atendimento(id_atendimento)

    def buscar_historico_atendimento(self, id_atendimento):
        dados = self.bd.buscar_historico_atendimento(id_atendimento)
        return [Historico_Atendimento_Serial.de_dict(h) for h in dados]

    def buscar_historico_por_cliente(self, cpf_cliente):
        self._exigir(cpf_cliente, "CPF do cliente")
        return self.bd.get_historico_por_cliente(cpf_cliente.strip())

    def buscar_historico_por_carro(self, placa_carro):
        self._exigir(placa_carro, "placa do carro")
        return self.bd.get_historico_por_carro(placa_carro.strip().upper())

    def buscar_historico_por_mecanico(self, id_mecanico):
        self._exigir(id_mecanico, "ID do mecânico")
        return self.bd.get_historico_por_mecanico(id_mecanico)

    def buscar_historico_por_peca(self, id_peca):
        self._exigir(id_peca, "ID da peça")
        return self.bd.get_historico_por_peca(id_peca)

    def buscar_historico_por_status(self, status):
        self._exigir(status, "status")
        return self.bd.get_historico_por_status(status)
