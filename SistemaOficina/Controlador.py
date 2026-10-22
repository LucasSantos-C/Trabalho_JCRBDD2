from datetime import datetime
import sqlite3

from ObjetoAcessaDados import ObjetoAcessaDados


class Controlador:
    """
    Controlador do Sistema de Oficina Mecânica.

    Responsabilidades:
    - receber dados da interface;
    - validar dados básicos;
    - chamar o acesso a dados;
    - devolver resultados em formato de dicionário/lista.

    Este arquivo deve ficar na mesma pasta de ObjetoAcessaDados.py.
    """

    def __init__(self, acesso_dados=None):
        self.bd = acesso_dados or ObjetoAcessaDados()

    # ---------- Métodos internos ----------

    def _executar(self, sql, parametros=(), consulta=False):
        """Executa SQL parametrizado usando a conexão do ObjetoAcessaDados."""
        try:
            with self.bd.conectar() as conexao:
                # Ativa as chaves estrangeiras nesta conexão.
                conexao.execute("PRAGMA foreign_keys = ON")
                cursor = conexao.execute(sql, parametros)
                if consulta:
                    return [dict(linha) for linha in cursor.fetchall()]
                conexao.commit()
                return cursor.lastrowid if sql.lstrip().upper().startswith("INSERT") else True
        except sqlite3.IntegrityError as erro:
            raise ValueError(f"Operação não permitida pelo banco de dados: {erro}") from erro
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao acessar o banco de dados: {erro}") from erro

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
        self._executar(
            "INSERT INTO cliente (cpf, nome, telefone, endereco) VALUES (?, ?, ?, ?)",
            (cpf.strip(), nome.strip(), telefone, endereco),
        )
        return self.buscar_cliente(cpf.strip())

    def listar_clientes(self):
        return self._executar(
            "SELECT cpf, nome, telefone, endereco FROM cliente ORDER BY nome",
            consulta=True,
        )

    def buscar_cliente(self, cpf):
        resultado = self._executar(
            "SELECT cpf, nome, telefone, endereco FROM cliente WHERE cpf = ?",
            (cpf,),
            consulta=True,
        )
        return resultado[0] if resultado else None

    def atualizar_cliente(self, cpf, nome, telefone=None, endereco=None):
        self._exigir(cpf, "CPF")
        self._exigir(nome, "nome")
        resultado = self._executar(
            "UPDATE cliente SET nome = ?, telefone = ?, endereco = ? WHERE cpf = ?",
            (nome.strip(), telefone, endereco, cpf.strip()),
        )
        if not resultado:
            raise ValueError("Cliente não encontrado.")
        return self.buscar_cliente(cpf.strip())

    def excluir_cliente(self, cpf):
        self._executar("DELETE FROM cliente WHERE cpf = ?", (cpf,))
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
        self._executar(
            "INSERT INTO carro (placa, modelo, cor, ano, marca) VALUES (?, ?, ?, ?, ?)",
            (placa.strip().upper(), modelo.strip(), cor, ano, marca),
        )
        return self.buscar_carro(placa.strip().upper())

    def listar_carros(self):
        return self._executar(
            "SELECT placa, modelo, cor, ano, marca FROM carro ORDER BY placa",
            consulta=True,
        )

    def buscar_carro(self, placa):
        resultado = self._executar(
            "SELECT placa, modelo, cor, ano, marca FROM carro WHERE placa = ?",
            (placa.strip().upper(),),
            consulta=True,
        )
        return resultado[0] if resultado else None

    def atualizar_carro(self, placa, modelo, cor=None, ano=None, marca=None):
        self._exigir(placa, "placa")
        self._exigir(modelo, "modelo")
        if ano not in (None, ""):
            try:
                ano = int(ano)
            except (TypeError, ValueError) as erro:
                raise ValueError("O ano deve ser um número inteiro.") from erro
        placa = placa.strip().upper()
        self._executar(
            "UPDATE carro SET modelo = ?, cor = ?, ano = ?, marca = ? WHERE placa = ?",
            (modelo.strip(), cor, ano, marca, placa),
        )
        if not self.buscar_carro(placa):
            raise ValueError("Carro não encontrado.")
        return self.buscar_carro(placa)

    # ---------- Mecânicos ----------

    def cadastrar_mecanico(self, nome, telefone=None, especialidade=None):
        self._exigir(nome, "nome")
        identificador = self._executar(
            "INSERT INTO mecanico (nome, telefone, especialidade) VALUES (?, ?, ?)",
            (nome.strip(), telefone, especialidade),
        )
        return self.buscar_mecanico(identificador)

    def listar_mecanicos(self):
        return self._executar(
            "SELECT id, nome, telefone, especialidade FROM mecanico ORDER BY nome",
            consulta=True,
        )

    def buscar_mecanico(self, id_mecanico):
        resultado = self._executar(
            "SELECT id, nome, telefone, especialidade FROM mecanico WHERE id = ?",
            (id_mecanico,),
            consulta=True,
        )
        return resultado[0] if resultado else None

    def atualizar_mecanico(self, id_mecanico, nome, telefone=None, especialidade=None):
        self._exigir(nome, "nome")
        self._executar(
            "UPDATE mecanico SET nome = ?, telefone = ?, especialidade = ? WHERE id = ?",
            (nome.strip(), telefone, especialidade, id_mecanico),
        )
        mecanico = self.buscar_mecanico(id_mecanico)
        if not mecanico:
            raise ValueError("Mecânico não encontrado.")
        return mecanico

    # ---------- Peças e estoque ----------

    def cadastrar_peca(self, tipo, modelo=None, qtd=0):
        self._exigir(tipo, "tipo")
        qtd = self._validar_quantidade(qtd, "quantidade")
        identificador = self._executar(
            "INSERT INTO peca (tipo, modelo, qtd) VALUES (?, ?, ?)",
            (tipo.strip(), modelo, qtd),
        )
        return self.buscar_peca(identificador)

    def listar_pecas(self):
        return self._executar(
            "SELECT id, tipo, modelo, qtd FROM peca ORDER BY tipo, modelo",
            consulta=True,
        )

    def buscar_peca(self, id_peca):
        resultado = self._executar(
            "SELECT id, tipo, modelo, qtd FROM peca WHERE id = ?",
            (id_peca,),
            consulta=True,
        )
        return resultado[0] if resultado else None

    def atualizar_estoque(self, id_peca, quantidade):
        """Define a quantidade disponível em estoque."""
        quantidade = self._validar_quantidade(quantidade, "quantidade")
        self._executar(
            "UPDATE peca SET qtd = ? WHERE id = ?",
            (quantidade, id_peca),
        )
        peca = self.buscar_peca(id_peca)
        if not peca:
            raise ValueError("Peça não encontrada.")
        return peca

    def adicionar_ao_estoque(self, id_peca, quantidade):
        """Acrescenta unidades ao estoque atual."""
        quantidade = self._validar_quantidade(
            quantidade, "quantidade a adicionar", permitir_zero=False
        )
        self._executar(
            "UPDATE peca SET qtd = qtd + ? WHERE id = ?",
            (quantidade, id_peca),
        )
        peca = self.buscar_peca(id_peca)
        if not peca:
            raise ValueError("Peça não encontrada.")
        return peca

    # ---------- Peças associadas a carros ----------

    def associar_peca_ao_carro(self, id_peca, placa_carro, quantidade):
        quantidade = self._validar_quantidade(
            quantidade, "quantidade", permitir_zero=False
        )
        self._exigir(placa_carro, "placa do carro")
        self._executar(
            """
            INSERT INTO peca_carro (id_peca, placa_carro, qtdpeca)
            VALUES (?, ?, ?)
            ON CONFLICT(id_peca, placa_carro)
            DO UPDATE SET qtdpeca = excluded.qtdpeca
            """,
            (id_peca, placa_carro.strip().upper(), quantidade),
        )
        return self.listar_pecas_do_carro(placa_carro)

    def listar_pecas_do_carro(self, placa_carro):
        return self._executar(
            """
            SELECT p.id, p.tipo, p.modelo, pc.qtdpeca
            FROM peca_carro AS pc
            JOIN peca AS p ON p.id = pc.id_peca
            WHERE pc.placa_carro = ?
            ORDER BY p.tipo, p.modelo
            """,
            (placa_carro.strip().upper(),),
            consulta=True,
        )

    # ---------- Atendimentos e histórico ----------

    def registrar_atendimento(
        self, status, id_mecanico, placa_carro, cpf_cliente,
        desc_atendimento="", data_abertura=None
    ):
        self._exigir(status, "status")
        self._exigir(placa_carro, "placa do carro")
        self._exigir(cpf_cliente, "CPF do cliente")

        # Confere se os registros relacionados existem antes de criar o atendimento.
        if not self.buscar_mecanico(id_mecanico):
            raise ValueError("Mecânico não encontrado.")
        if not self.buscar_carro(placa_carro):
            raise ValueError("Carro não encontrado.")
        if not self.buscar_cliente(cpf_cliente):
            raise ValueError("Cliente não encontrado.")

        data_abertura = data_abertura or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_atendimento = self._executar(
            """
            INSERT INTO atendimento (status, id_mecanico, placa_carro, cpf_cliente)
            VALUES (?, ?, ?, ?)
            """,
            (status, id_mecanico, placa_carro.strip().upper(), cpf_cliente.strip()),
        )
        self._executar(
            """
            INSERT INTO historico_atendimento
                (id_atendimento, data_abertura, data_fechamento, desc_atendimento)
            VALUES (?, ?, ?, ?)
            """,
            (id_atendimento, data_abertura, None, desc_atendimento),
        )
        return self.buscar_atendimento(id_atendimento)

    def listar_atendimentos(self):
        return self._executar(
            """
            SELECT a.id, a.status, a.id_mecanico, m.nome AS nome_mecanico,
                   a.placa_carro, c.modelo AS modelo_carro,
                   a.cpf_cliente, cl.nome AS nome_cliente
            FROM atendimento AS a
            LEFT JOIN mecanico AS m ON m.id = a.id_mecanico
            LEFT JOIN carro AS c ON c.placa = a.placa_carro
            LEFT JOIN cliente AS cl ON cl.cpf = a.cpf_cliente
            ORDER BY a.id DESC
            """,
            consulta=True,
        )

    def buscar_atendimento(self, id_atendimento):
        resultado = self._executar(
            """
            SELECT a.id, a.status, a.id_mecanico, m.nome AS nome_mecanico,
                   a.placa_carro, c.modelo AS modelo_carro,
                   a.cpf_cliente, cl.nome AS nome_cliente,
                   h.data_abertura, h.data_fechamento, h.desc_atendimento
            FROM atendimento AS a
            LEFT JOIN mecanico AS m ON m.id = a.id_mecanico
            LEFT JOIN carro AS c ON c.placa = a.placa_carro
            LEFT JOIN cliente AS cl ON cl.cpf = a.cpf_cliente
            LEFT JOIN historico_atendimento AS h ON h.id_atendimento = a.id
            WHERE a.id = ?
            """,
            (id_atendimento,),
            consulta=True,
        )
        return resultado[0] if resultado else None

    def atualizar_status_atendimento(self, id_atendimento, status, finalizar=False):
        self._exigir(status, "status")
        if not self.buscar_atendimento(id_atendimento):
            raise ValueError("Atendimento não encontrado.")

        self._executar(
            "UPDATE atendimento SET status = ? WHERE id = ?",
            (status, id_atendimento),
        )
        if finalizar:
            data_fechamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._executar(
                """
                UPDATE historico_atendimento
                SET data_fechamento = ?
                WHERE id_atendimento = ?
                """,
                (data_fechamento, id_atendimento),
            )
        return self.buscar_atendimento(id_atendimento)

    def buscar_historico_atendimento(self, id_atendimento):
        return self._executar(
            """
            SELECT id_atendimento, data_abertura, data_fechamento, desc_atendimento
            FROM historico_atendimento
            WHERE id_atendimento = ?
            ORDER BY data_abertura DESC
            """,
            (id_atendimento,),
            consulta=True,
          )
