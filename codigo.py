import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO = os.path.join(BASE_DIR, 'arquivo_alunos.txt')
listar_alunos = []
alunos_id = 1


def salvar_alunos():
    with open(NOME_ARQUIVO, 'w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=['id', 'nome', 'disciplina', 'nota'])
        escritor.writeheader()
        for aluno in listar_alunos:
            escritor.writerow({
                'id': aluno['id'],
                'nome': aluno['nome'],
                'disciplina': aluno['disciplina'],
                'nota': f"{aluno['nota']:.2f}"
            })


def carregar_alunos():
    global listar_alunos, alunos_id
    listar_alunos = []
    alunos_id = 1

    if not os.path.exists(NOME_ARQUIVO):
        salvar_alunos()
        return

    with open(NOME_ARQUIVO, 'r', encoding='utf-8', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            try:
                aluno_id = int(linha['id'])
                nota = float(linha['nota'])
            except (ValueError, KeyError, TypeError):
                continue

            aluno = {
                'id': aluno_id,
                'nome': linha['nome'].title(),
                'disciplina': linha['disciplina'].title(),
                'nota': nota
            }
            listar_alunos.append(aluno)
            alunos_id = max(alunos_id, aluno_id + 1)

    if not listar_alunos:
        salvar_alunos()

# FUNÇÕES AUXILIARES DE VALIDAÇÃO

def obter_string(prompt):
    while True:
        entrada = input(prompt).strip()
        if entrada:
            return entrada.title()
        print("\033[1;31mErro: O campo não pode ser vazio.\033[0m")

def obter_float(prompt):
    while True:
        entrada = input(prompt).strip().replace(',', '.')
        if not entrada:
            print('\033[1;31mErro: O campo não pode ser vazio.\033[0m')
            continue
        try:
            nota = float(entrada)
            if nota >= 0:
                return nota
            print("\033[1;31mErro: A nota deve ser positiva.\033[0m")
        except ValueError:
            print("\033[1;31mErro: Digite um número decimal válido (ex: 30.60).\033[0m")

def obter_inteiro(prompt):
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            print('\033[1;31mErro: O campo não pode ser vazio.\033[0m')
            continue
        try:
            valor = int(entrada)
            if valor >= 0:
                return valor
            print("\033[1;31mErro: O valor deve ser positivo.\033[0m")
        except ValueError:
            print("\033[1;31mErro: Digite um número inteiro válido.\033[0m")

def encontrar_aluno(identificador):
    if isinstance(identificador, int):
        for aluno in listar_alunos:
            if aluno['id'] == identificador:
                return aluno

    elif isinstance(identificador, str):
        for aluno in listar_alunos:
            if aluno['nome'] == identificador:
                return aluno
    return None

# Função para apagar aluno
def apagar_aluno():
    global listar_alunos

    print("\n--- REMOVER ALUNO ---")
    aluno_id = obter_inteiro('Insira a ID de identificação do aluno: ')

    for aluno in listar_alunos:
        if aluno['id'] == aluno_id:
            listar_alunos.remove(aluno)
            salvar_alunos()
            print(f'Aluno com ID {aluno_id} removido com sucesso!')
            break
    else:
        print('Aluno não encontrado.')

# Cadastrar alunos

def cadastrar_aluno():
    global alunos_id, listar_alunos
    print("\n--- CADASTRO DE NOVO ALUNO ---")

    nome = obter_string("Digite o nome do aluno: ")
    disciplina = obter_string("Digite a disciplina do aluno: ")
    nota = obter_float("Digite a nota do aluno: ")

    aluno = {
        "id": alunos_id,
        "nome": nome,
        "disciplina": disciplina,
        "nota": nota
    }

    listar_alunos.append(aluno)
    alunos_id += 1
    salvar_alunos()
    print("Aluno cadastrado com sucesso!")

# Limpar o terminal no em multiplataforma (Windows, Linux e macOs)
carregar_alunos()
os.system('cls' if os.name == 'nt' else 'clear')    

# Funções Principais do Sistema

def menu():
    while True:
        print("\n" + "="*23)
        print("Sistema de Notas")
        print('1 - Cadastrar Aluno')
        print('2 - Listar Alunos')
        print('3 - Remover Aluno')
        print('4 - Atualizar Nota')
        print('5 - Buscar Aluno')
        print('0 - Sair')
        print("-" * 23)

        escolha = input(" Escolha uma opção: ").strip()
        if escolha.isdigit():
            opcao = int(escolha)
            if 0 <= opcao <= 5:
                return opcao
            print("\033[31m Opção inválida. Escolha um número entre 0 e 5.\033[0m")
        else:
            print("\033[31m Entrada inválida. Digite o número da opção.\033[0m")

# Função para listar alunos

def listar():
    if not listar_alunos:
        print("\n A lista de alunos está vazia.")
        return

    print("\033[7;34m\n---  LISTA DE ALUNOS ---\033[0m")
    alunos_ordenados = sorted(listar_alunos, key=lambda c: c['nome'])
    print("\033[34mID | NOME             | DISCIPLINA           | NOTA\033[0m")
    print("-" * 80)
    for aluno in alunos_ordenados:
        print(f"{aluno['id']:<2} | {aluno['nome']:<18} | {aluno['disciplina']:<20} | {aluno['nota']:.2f}")
    print("-" * 80)
    print(f"\033[34mTotal de Alunos: {len(listar_alunos)}\033[0m") 

# Função para atualizar nota do aluno

def atualizar_nota():
    print("\n--- Atualizar nota do aluno ---")

    id_busca = obter_inteiro("Digite a ID do aluno: ")

    notas_para_atualizar = encontrar_aluno(id_busca)

    if not notas_para_atualizar:
        print("\033[1;31m Erro: Aluno não encontrado.\033[0m")
        return

    print(f"Aluno encontrado: {notas_para_atualizar['nome']}")
    
    nova_nota = obter_float("Digite a nova nota do aluno: ")
    notas_para_atualizar['nota'] = nova_nota
    salvar_alunos()
    print("Nota atualizada com sucesso!")

# Função para buscar aluno

def buscar_aluno():
    print("\n--- Buscar aluno ---")
    termo = input("Digite o nome ou ID do aluno: ").strip()
    if not termo:
        print("\033[1;31mErro: O campo não pode ser vazio.\033[0m")
        return

    aluno = None
    if termo.isdigit():
        aluno = encontrar_aluno(int(termo))
    else:
        aluno = encontrar_aluno(termo.title())

    if aluno:
        print("\nAluno encontrado:")
        print(f"ID: {aluno['id']}")
        print(f"Nome: {aluno['nome']}")
        print(f"Disciplina: {aluno['disciplina']}")
        print(f"Nota: {aluno['nota']:.2f}")
    else:
        print("\033[1;31mAluno não encontrado.\033[0m")


def main():
    while True:
        opcao = menu()

        if opcao == 1:
            cadastrar_aluno()
        elif opcao == 2:
            listar()
        elif opcao == 3:
            apagar_aluno()
        elif opcao == 4:
            atualizar_nota()
        elif opcao == 5:
            buscar_aluno()
        elif opcao == 0:
            print("\nSaindo do sistema. Até logo!")
            break

        input("\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()