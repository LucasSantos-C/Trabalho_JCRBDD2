import sqlite3

class ObjetoAcessaDados:
    def __init__(self, nome_banco="oficina_mecanica.db"):
        self.nome_banco = nome_banco
        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(self.nome_banco)
        conexao.row_factory = sqlite3.Row
        return conexao

    def executar_sql(self, sql, parametros=()):
        try:
            with self.conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(sql, parametros)
                conexao.commit()
                if sql.strip().upper().startswith("SELECT"):
                    return [dict(row) for row in cursor.fetchall()]
                return True
        except sqlite3.Error as erro:
            print(f"Erro ao executar SQL: {erro}")
            return False

    def criar_tabelas(self):
        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS cliente (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                telefone TEXT,
                endereco TEXT
            );""")
        
        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS carro (
                placa TEXT PRIMARY KEY,
                modelo TEXT,
                cor TEXT,
                ano INTEGER,
                marca TEXT
            );""")
        
        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS mecanico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                especialidade TEXT
            );""")
        
        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS peca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                modelo TEXT,
                qtd INTEGER
            );""")

        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS peca_carro (
                id_peca INTEGER,
                placa_carro TEXT,
                qtdpeca INTEGER,
                PRIMARY KEY (id_peca, placa_carro),
                FOREIGN KEY(id_peca) REFERENCES peca(id),
                FOREIGN KEY(placa_carro) REFERENCES carro(placa)
            );""")
        
        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS atendimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT,
                id_mecanico INTEGER,
                placa_carro TEXT,
                cpf_cliente TEXT,
                FOREIGN KEY (id_mecanico) REFERENCES mecanico(id),
                FOREIGN KEY (placa_carro) REFERENCES carro(placa),
                FOREIGN KEY (cpf_cliente) REFERENCES cliente(cpf)
            );""")

        self.executar_sql("""
            CREATE TABLE IF NOT EXISTS historico_atendimento (
                id_atendimento INTEGER,
                data_abertura TEXT,
                data_fechamento TEXT,
                desc_atendimento TEXT,
                FOREIGN KEY (id_atendimento) REFERENCES atendimento(id)
            );""")

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

    def get_pecas_do_carro(self, placa_carro):
        sql = """
            SELECT p.id, p.tipo, p.modelo, pc.qtdpeca 
            FROM peca_carro pc
            JOIN peca p ON pc.id_peca = p.id
            WHERE pc.placa_carro = ?
        """
        return self.executar_sql(sql, (placa_carro,))
