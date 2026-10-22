import sqlite3

class ObjetoAcessaDados:
    def __init__(self, nome_banco="oficina_mecanica.db"):
        self.nome_banco = nome_banco
        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(self.nome_banco)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")  # <--- Adicionar esta linha
        return conexao

    def executar_sql(self, sql, parametros=()):
        try:
            with self.conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(sql, parametros)
                conexao.commit()
            if sql.strip().upper().startswith("SELECT"):
                return [dict(row) for row in cursor.fetchall()]
            return cursor.lastrowid if sql.lstrip().upper().startswith("INSERT") else True
        except sqlite3.Error as erro:
            print(f"Erro ao executar SQL: {erro}")
            return False

    def criar_tabelas(self):
        try:
            with self.conectar() as conexao:
                conexao.executescript("""
                    CREATE TABLE IF NOT EXISTS cliente (
                        cpf TEXT PRIMARY KEY,
                        nome TEXT NOT NULL,
                        telefone TEXT,
                        endereco TEXT
                    );
                    
                    CREATE TABLE IF NOT EXISTS carro (
                        placa TEXT PRIMARY KEY,
                        modelo TEXT,
                        cor TEXT,
                        ano INTEGER,
                        marca TEXT
                    );
                    
                    CREATE TABLE IF NOT EXISTS mecanico (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        telefone TEXT,
                        especialidade TEXT
                    );
                    
                    CREATE TABLE IF NOT EXISTS peca (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tipo TEXT,
                        modelo TEXT,
                        qtd INTEGER
                    );

                    CREATE TABLE IF NOT EXISTS peca_carro (
                        id_peca INTEGER,
                        placa_carro TEXT,
                        qtdpeca INTEGER,
                        PRIMARY KEY (id_peca, placa_carro),
                        FOREIGN KEY (id_peca) REFERENCES peca(id),
                        FOREIGN KEY (placa_carro) REFERENCES carro(placa)
                    );
                    
                    CREATE TABLE IF NOT EXISTS atendimento (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        status TEXT,
                        id_mecanico INTEGER,
                        placa_carro TEXT,
                        cpf_cliente TEXT,
                        FOREIGN KEY (id_mecanico) REFERENCES mecanico(id),
                        FOREIGN KEY (placa_carro) REFERENCES carro(placa),
                        FOREIGN KEY (cpf_cliente) REFERENCES cliente(cpf)
                    );

                    CREATE TABLE IF NOT EXISTS historico_atendimento (
                        id_atendimento INTEGER,
                        data_abertura TEXT,
                        data_fechamento TEXT,
                        desc_atendimento TEXT,
                        FOREIGN KEY (id_atendimento) REFERENCES atendimento(id)
                    );
                """)
        except sqlite3.Error as erro:
            print(f"Erro ao criar tabelas: {erro}")

    def set(self, tabela, dados):
        colunas = ", ".join(dados.keys())
        placeholders = ", ".join([":" + k for k in dados.keys()])
        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
        return self.executar_sql(sql, dados)

    def update(self, tabela, dados, condicao_coluna):
        if condicao_coluna not in dados:
            return False
            
        sets = ", ".join([f"{k} = :{k}" for k in dados.keys() if k != condicao_coluna])
        sql = f"UPDATE {tabela} SET {sets} WHERE {condicao_coluna} = :{condicao_coluna}"
        return self.executar_sql(sql, dados)

    def delete(self, tabela, coluna_id, valor_id):
        sql = f"DELETE FROM {tabela} WHERE {coluna_id} = ?"
        return self.executar_sql(sql, (valor_id,))

    def get_todos(self, tabela):
        sql = f"SELECT * FROM {tabela}"
        return self.executar_sql(sql)

    def get_por_coluna(self, tabela, coluna_criterio, valor_criterio):
        sql = f"SELECT * FROM {tabela} WHERE {coluna_criterio} = ?"
        resultado = self.executar_sql(sql, (valor_criterio,))
        return resultado if resultado else False

    def listar_clientes(self):
        sql = "SELECT cpf, nome, telefone, endereco FROM cliente ORDER BY nome"
        return self.executar_sql(sql)

    def listar_carros(self):
        sql = "SELECT placa, modelo, cor, ano, marca FROM carro ORDER BY placa"
        return self.executar_sql(sql)

    def listar_mecanicos(self):
        sql = "SELECT id, nome, telefone, especialidade FROM mecanico ORDER BY nome"
        return self.executar_sql(sql)

    def listar_pecas(self):
        sql = "SELECT id, tipo, modelo, qtd FROM peca ORDER BY tipo, modelo"
        return self.executar_sql(sql)

    def listar_atendimentos(self):
        sql = """
            SELECT a.id, a.status, a.id_mecanico, m.nome AS nome_mecanico,
                   a.placa_carro, c.modelo AS modelo_carro,
                   a.cpf_cliente, cl.nome AS nome_cliente
            FROM atendimento AS a
            LEFT JOIN mecanico AS m ON m.id = a.id_mecanico
            LEFT JOIN carro AS c ON c.placa = a.placa_carro
            LEFT JOIN cliente AS cl ON cl.cpf = a.cpf_cliente
            ORDER BY a.id DESC
        """
        return self.executar_sql(sql)

    def buscar_historico_atendimento(self, id_atendimento):
        sql = """
            SELECT id_atendimento, data_abertura, data_fechamento, desc_atendimento
            FROM historico_atendimento
            WHERE id_atendimento = ?
            ORDER BY data_abertura DESC
        """
        return self.executar_sql(sql, (id_atendimento,))

    def get_pecas_do_carro(self, placa_carro):
        sql = """
            SELECT p.id, p.tipo, p.modelo, pc.qtdpeca 
            FROM peca_carro pc
            JOIN peca p ON pc.id_peca = p.id
            WHERE pc.placa_carro = ?
        """
        return self.executar_sql(sql, (placa_carro,))

    def get_detalhes_atendimento(self, id_atendimento):
        sql = """
            SELECT 
                atendimento.id AS id_atendimento,
                atendimento.status,
                cliente.nome AS nome_cliente,
                cliente.telefone AS telefone_cliente,
                carro.placa,
                carro.marca,
                carro.modelo,
                mecanico.nome AS nome_mecanico,
                mecanico.especialidade AS especialidade_mecanico,
                historico_atendimento.data_abertura,
                historico_atendimento.data_fechamento,
                historico_atendimento.desc_atendimento
            FROM atendimento
            JOIN cliente ON atendimento.cpf_cliente = cliente.cpf
            JOIN carro ON atendimento.placa_carro = carro.placa
            JOIN mecanico ON atendimento.id_mecanico = mecanico.id
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE atendimento.id = ?
        """
        resultado = self.executar_sql(sql, (id_atendimento,))
        return resultado[0] if resultado else False

    def get_historico_por_cliente(self, cpf_cliente):
        sql = """
            SELECT 
                carro.placa,
                carro.marca,
                carro.modelo,
                atendimento.id AS id_atendimento,
                atendimento.status,
                mecanico.nome AS nome_mecanico,
                historico_atendimento.data_abertura,
                historico_atendimento.data_fechamento,
                historico_atendimento.desc_atendimento
            FROM cliente
            JOIN atendimento ON cliente.cpf = atendimento.cpf_cliente
            JOIN carro ON atendimento.placa_carro = carro.placa
            JOIN mecanico ON atendimento.id_mecanico = mecanico.id
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE cliente.cpf = ?
            ORDER BY historico_atendimento.data_abertura DESC
        """
        return self.executar_sql(sql, (cpf_cliente,))

    def get_historico_por_carro(self, placa_carro):
        sql = """
            SELECT 
                carro.placa,
                carro.marca,
                carro.modelo,
                atendimento.id AS id_atendimento,
                atendimento.status,
                cliente.nome AS nome_cliente,
                mecanico.nome AS nome_mecanico,
                historico_atendimento.data_abertura,
                historico_atendimento.data_fechamento,
                historico_atendimento.desc_atendimento
            FROM carro
            JOIN atendimento ON carro.placa = atendimento.placa_carro
            JOIN cliente ON atendimento.cpf_cliente = cliente.cpf
            JOIN mecanico ON atendimento.id_mecanico = mecanico.id
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE carro.placa = ?
            ORDER BY historico_atendimento.data_abertura DESC
        """
        return self.executar_sql(sql, (placa_carro,))

    def get_historico_por_mecanico(self, id_mecanico):
        sql = """
            SELECT 
                mecanico.id AS id_mecanico,
                mecanico.nome AS nome_mecanico,
                atendimento.id AS id_atendimento,
                atendimento.status,
                carro.placa,
                carro.modelo AS modelo_carro,
                cliente.nome AS nome_cliente,
                historico_atendimento.data_abertura,
                historico_atendimento.data_fechamento,
                historico_atendimento.desc_atendimento
            FROM mecanico
            JOIN atendimento ON mecanico.id = atendimento.id_mecanico
            JOIN carro ON atendimento.placa_carro = carro.placa
            JOIN cliente ON atendimento.cpf_cliente = cliente.cpf
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE mecanico.id = ?
            ORDER BY historico_atendimento.data_abertura DESC
        """
        return self.executar_sql(sql, (id_mecanico,))

    def get_historico_por_peca(self, id_peca):
        sql = """
            SELECT 
                peca.id AS id_peca,
                peca.tipo AS tipo_peca,
                peca.modelo AS modelo_peca,
                peca_carro.qtdpeca,
                carro.placa,
                carro.modelo AS modelo_carro,
                atendimento.id AS id_atendimento,
                atendimento.status,
                cliente.nome AS nome_cliente,
                historico_atendimento.data_abertura,
                historico_atendimento.desc_atendimento
            FROM peca
            JOIN peca_carro ON peca.id = peca_carro.id_peca
            JOIN carro ON peca_carro.placa_carro = carro.placa
            JOIN atendimento ON carro.placa = atendimento.placa_carro
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE peca.id = ?
            ORDER BY historico_atendimento.data_abertura DESC
        """
        return self.executar_sql(sql, (id_peca,))

    def get_historico_por_status(self, status_atendimento):
        sql = """
            SELECT 
                atendimento.id AS id_atendimento,
                atendimento.status,
                carro.placa,
                carro.modelo AS modelo_carro,
                cliente.nome AS nome_cliente,
                mecanico.nome AS nome_mecanico,
                historico_atendimento.data_abertura,
                historico_atendimento.data_fechamento,
                historico_atendimento.desc_atendimento
            FROM atendimento
            JOIN carro ON atendimento.placa_carro = carro.placa
            JOIN cliente ON atendimento.cpf_cliente = cliente.cpf
            JOIN mecanico ON atendimento.id_mecanico = mecanico.id
            LEFT JOIN historico_atendimento ON atendimento.id = historico_atendimento.id_atendimento
            WHERE atendimento.status = ?
            ORDER BY historico_atendimento.data_abertura DESC
        """
        return self.executar_sql(sql, (status_atendimento,))
