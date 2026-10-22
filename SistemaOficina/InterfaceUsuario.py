from Controlador import Controlador

class InterfaceUsuario:
    def __init__(self, controlador=None):
        self.controlador = controlador or Controlador()
    
    def inicio(self):
       menu = {
           "1": ("Clientes", self.menu_cliente),
           "2": ("Carros", self.menu_carro),
           "3": ("Mecanicos", self.menu_mecanico),
           "4": ("Peças", self.menu_peca),
           "5": ("Atendimentos", self.menu_atendimento),
       }
       self._loop("OFICINA", menu)
       print("Encerrando o sistema...")
       
#   =================   MENUS   ================= 

    def menu_cliente(self):
        self._loop("CLIENTES", {
            "1": ("Cadastrar", self._cadastrar_cliente),
            "2": ("Listar", self._exibir(self._controlador.listar_cliente())),
            "3": ("Buscar por CPF", self._buscar_cliente),
            "4": ("Atualizar", self._atualizar_cliente),
            "5": ("Deletar", self._deletar_cliente), 
        }, voltar = True)

    def menu_carro(self):
        self._loop("CARROS", {
            "1": ("Cadastrar", self._cadastrar_carro),
            "2": ("Listar", self._exibir(self._controlador.listar_carro())),
            "3": ("Buscar por placa", self._buscar_carro),
            "4": ("Atualizar", self._atualizar_carro),
            "5": ("Associar peça ao carro", self._associar_carro),
            "6": ("Listar peças ao carro", self._listar_peca_cliente), 
        }, voltar = True)

    def menu_mecanico(self):
        self._loop("MECANICOS", {
            "1": ("Cadastrar", self._cadastrar_mecanico),
            "2": ("Listar", self._exibir(self._controlador.listar_mecanico())),
            "3": ("Buscar por ID", self._buscar_mecanico),
            "4": ("Atualizar", self._atualizar_mecanico),
        }, voltar = True)

    def menu_peca(self):
        self._loop("PEÇAS", {
            "1": ("Cadastrar peça", self._cadastrar_peca),
            "2": ("Listar", self._exibir(self._controlador.listar_peca())),
            "3": ("Buscar por ID", self._buscar_peca),
            "4": ("Definir quantidade em estoque", self._atualizar_estoque),
            "5": ("Adicionar ao estoque", self._adicionar_estoque), 
        }, voltar = True)

    def menu_atendimento(self):
        self._loop("ATENDIMENTOS", {
            "1": ("Registrar atendimento", self._registrar_atendimento),
            "2": ("Listar", self._exibir(self._controlador.listar_atendimentos())),
            "3": ("Buscar detalhes por ID", self._buscar_atendimentos),
            "4": ("Atualizar status", self._atualizar_status),
            "5": ("Consultar histórico", self._consultar_historico), 
        }, voltar = True)
       
#   =================  CLIENTES  ================= 

    def _cadastrar_clientes(self):
        cliente = self.controlador.cadastrar_cliente(
            cpf = self._ler_texto("CPF: "),
            nome = self._ler_texto("Nome: "),
            telefone = self._ler_opcional("Telefone (opcional): "),
            endereco = self._ler_opcional("Endereço (opcional): "),
        )
        print(f"Cliente: {self._exibir(cliente)} Cadastrado com sucesso...")

    def _buscar_cliente(self):
        self._exibir(self.controlador.buscar_cliente(self._ler_texto("CPF: ")))

    def _atualizar_cliente(self):
        cliente = self.controlador.atualizar_cliente(
            cpf=self._ler_texto("CPF do cliente: "),
            nome=self._ler_texto("Novo nome: "),
            telefone=self._ler_opcional("Novo telefone (opcional): "),
            endereco=self._ler_opcional("Novo endereço (opcional): "),
        )
        print("Cliente atualizado:")
        self._exibir(cliente)
 
    def _excluir_cliente(self):
        cpf = self._ler_texto("CPF do cliente: ")
        if self._confirmar("Confirma a exclusão?"):
            self.controlador.excluir_cliente(cpf)
            print("Cliente excluído.")
 
# ================= CARROS =================

    def _cadastrar_carro(self):
        carro = self.controlador.cadastrar_carro(
            placa=self._ler_texto("Placa: "),
            modelo=self._ler_texto("Modelo: "),
            cor=self._ler_opcional("Cor (opcional): "),
            ano=self._ler_opcional("Ano (opcional): "),
            marca=self._ler_opcional("Marca (opcional): "),
        )
        print("Carro cadastrado:")
        self._exibir(carro)
 
    def _buscar_carro(self):
        self._exibir(self.controlador.buscar_carro(self._ler_texto("Placa: ")))
 
    def _atualizar_carro(self):
        carro = self.controlador.atualizar_carro(
            placa=self._ler_texto("Placa do carro: "),
            modelo=self._ler_texto("Novo modelo: "),
            cor=self._ler_opcional("Nova cor (opcional): "),
            ano=self._ler_opcional("Novo ano (opcional): "),
            marca=self._ler_opcional("Nova marca (opcional): "),
        )
        print("Carro atualizado:")
        self._exibir(carro)
 
    def _associar_peca(self):
        placa = self._ler_texto("Placa do carro: ")
        id_peca = self._ler_int("ID da peça: ")
        qtd = self._ler_int("Quantidade utilizada: ")
        pecas = self.controlador.associar_peca_ao_carro(id_peca, placa, qtd)
        print("Peças do carro após a associação:")
        self._exibir(pecas)
 
    def _listar_pecas_do_carro(self):
        self._exibir(
            self.controlador.listar_pecas_do_carro(self._ler_texto("Placa do carro: "))
        )
 
# ================= MECÂNICOS =================

    def _cadastrar_mecanico(self):
        mecanico = self.controlador.cadastrar_mecanico(
            nome=self._ler_texto("Nome: "),
            telefone=self._ler_opcional("Telefone (opcional): "),
            especialidade=self._ler_opcional("Especialidade (opcional): "),
        )
        print("Mecânico cadastrado:")
        self._exibir(mecanico)
 
    def _buscar_mecanico(self):
        self._exibir(self.controlador.buscar_mecanico(self._ler_int("ID do mecânico: ")))
 
    def _atualizar_mecanico(self):
        mecanico = self.controlador.atualizar_mecanico(
            id_mecanico=self._ler_int("ID do mecânico: "),
            nome=self._ler_texto("Novo nome: "),
            telefone=self._ler_opcional("Novo telefone (opcional): "),
            especialidade=self._ler_opcional("Nova especialidade (opcional): "),
        )
        print("Mecânico atualizado:")
        self._exibir(mecanico)
 
# ================= PEÇAS =================

    def _cadastrar_peca(self):
        peca = self.controlador.cadastrar_peca(
            tipo=self._ler_texto("Tipo da peça: "),
            modelo=self._ler_opcional("Modelo (opcional): "),
            qtd=self._ler_int("Quantidade inicial em estoque: "),
        )
        print("Peça cadastrada:")
        self._exibir(peca)
 
    def _buscar_peca(self):
        self._exibir(self.controlador.buscar_peca(self._ler_int("ID da peça: ")))
 
    def _atualizar_estoque(self):
        peca = self.controlador.atualizar_estoque(
            self._ler_int("ID da peça: "),
            self._ler_int("Nova quantidade em estoque: "),
        )
        print("Estoque atualizado:")
        self._exibir(peca)
 
    def _adicionar_estoque(self):
        peca = self.controlador.adicionar_ao_estoque(
            self._ler_int("ID da peça: "),
            self._ler_int("Quantidade a adicionar: "),
        )
        print("Estoque atualizado:")
        self._exibir(peca)
 
# ================= ATENDIMENTOS =================

    def _registrar_atendimento(self):
        status = self._escolher_status()
        atendimento = self.controlador.registrar_atendimento(
            status=status,
            id_mecanico=self._ler_int("ID do mecânico: "),
            placa_carro=self._ler_texto("Placa do carro: "),
            cpf_cliente=self._ler_texto("CPF do cliente: "),
            desc_atendimento=self._ler_opcional("Descrição do serviço (opcional): ") or "",
        )
        print("Atendimento registrado:")
        self._exibir(atendimento)
 
    def _buscar_atendimento(self):
        self._exibir(
            self.controlador.buscar_atendimento(self._ler_int("ID do atendimento: "))
        )
 
    def _atualizar_status(self):
        id_atd = self._ler_int("ID do atendimento: ")
        status = self._escolher_status()
        finalizar = self._confirmar("Registrar data de fechamento agora?")
        atendimento = self.controlador.atualizar_status_atendimento(
            id_atd, status, finalizar=finalizar
        )
        print("Atendimento atualizado:")
        self._exibir(atendimento)
 
    def _consultar_historico(self):
        self._exibir(
            self.controlador.buscar_historico_atendimento(
                self._ler_int("ID do atendimento: ")
            )
        )
 
    def _escolher_status(self):
        print("Status disponíveis:")
        for i, s in enumerate(self.STATUS_ATENDIMENTO, start=1):
            print(f"  {i} - {s}")
        while True:
            indice = self._ler_int("Escolha o status: ")
            if 1 <= indice <= len(self.STATUS_ATENDIMENTO):
                return self.STATUS_ATENDIMENTO[indice - 1]
            print("Opção inválida.")
 
# ================= INFRAESTRUTURA DE MENU =================

    def _loop(self, titulo, opcoes, voltar=False):
        while True:
            print(f"==========================")
            print(f"         {titulo} ")
            print(f"==========================")
            for chave, (nome, _) in opcoes.items():
                print(f"{chave} - {nome}")
            print("0 - " + ("Voltar" if voltar else "Sair"))
 
            escolha = input("Opção: ").strip()
            if escolha == "0":
                return
            if escolha in opcoes:
                self._executar(opcoes[escolha][1])
            else:
                print("Opção inválida.")
 
    def _executar(self, acao):
        """Executa uma ação e converte qualquer erro em mensagem amigável."""
        try:
            acao()
        except ValueError as erro:  # regras de negócio do Controlador
            print(f"Aviso: {erro}")
        except Exception as erro:  # falhas inesperadas (BD etc.)
            print(f"Erro inesperado: {erro}")
 
# ================= EXIBIÇÃO =================

    @staticmethod
    def _exibir(resultado):
        if not resultado:
            print("Nenhum registro encontrado.")
        elif isinstance(resultado, (list, tuple)):
            for item in resultado:
                print(" -", dict(item) if hasattr(item, "keys") else item)
        else:
            print(dict(resultado) if hasattr(resultado, "keys") else resultado)
 
# ================= LEITURA DE ENTRADA =================

    @staticmethod
    def _ler_texto(msg):
        while True:
            valor = input(msg).strip()
            if valor:
                return valor
            print("O campo não pode ficar vazio.")
 
    @staticmethod
    def _ler_opcional(msg):
        valor = input(msg).strip()
        return valor or None
 
    @staticmethod
    def _ler_int(msg):
        while True:
            try:
                return int(input(msg).strip())
            except ValueError:
                print("Digite um número inteiro válido.")
 
    @staticmethod
    def _confirmar(msg):
        return input(f"{msg} (s/n): ").strip().lower() == "s"