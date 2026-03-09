alunos = {}
contadores_curso = {}

def gerar_matricula(curso):
    curso = curso.upper()
    if curso not in contadores_curso:
        contadores_curso[curso] = 1
    else:
        contadores_curso[curso] += 1
    
    return f"{curso}{contadores_curso[curso]}"

def criar_aluno():
    print("\n Cadastrando novo aluno")
    nome = input("Nome do aluno: ")
    email = input("Email: ")
    
    cursos_validos = ["GES", "GEC", "GET", "GEA", "GEP"]

    while True:
        curso = input("Curso (GES, GEC, GET, GEA, GEP): ").upper()
        
        if curso in cursos_validos:
            break
        else:
            print(f"Erro: Curso inválido. Por favor, digite um dos válidos: {', '.join(cursos_validos)}")
    
    matricula = gerar_matricula(curso)
    
    aluno = {
        "nome": nome,
        "email": email,
        "curso": curso,
        "matricula": matricula
    }
    
    alunos[matricula] = aluno
    print(f"Aluno {nome} cadastrado com sucesso!")

def mostrar_alunos():
    print("\n Lista de Alunos")
    if not alunos:
        print("Nenhum aluno cadastrado")
        return
    
    for mat, dados in alunos.items():
        print(f"Matrícula: {mat} | Nome: {dados['nome']} | Curso: {dados['curso']} | Email: {dados['email']}")

def atualizar_aluno():
    print("\n Atualizar Informações do Aluno")
    matricula = input("Digite a matrícula do aluno que deseja alterar: ").upper()
    
    if matricula in alunos:
        print(f"Editando: {alunos[matricula]['nome']}")
        alunos[matricula]['nome'] = input("Novo Nome: ")
        alunos[matricula]['email'] = input("Novo Email: ")
        print("Dados atualizados com sucesso!")
    else:
        print("Matrícula não encontrada")

def deletar_aluno():
    print("\n Deletar Aluno")
    matricula = input("Digite a matrícula do aluno que deseja remover: ").upper()
    
    if matricula in alunos:
        removido = alunos.pop(matricula)
        print(f"Aluno {removido['nome']} removido com sucesso")
    else:
        print("Matrícula não encontrada")

def menu():
    while True:
        print("\n SISTEMA ACADEMICO")
        print("1. Cadastrar Aluno")
        print("2. Listar Alunos")
        print("3. Atualizar Aluno")
        print("4. Deletar Aluno")
        print("5. Sair")
        
        opcao = input("Escolha uma opcao: ")
        
        if opcao == '1':
            criar_aluno()
        elif opcao == '2':
            mostrar_alunos()
        elif opcao == '3':
            atualizar_aluno()
        elif opcao == '4':
            deletar_aluno()
        elif opcao == '5':
            print("Encerrando programa")
            break
        else:
            print("Opção inválida! Tente novamente")

if __name__ == "__main__":
    menu()