from model.conexao import conectar

def cadastrar_curso():
    print("\n=== CADASTRAR CURSO ===")
    nome = input("Nome do curso: ")
    descricao = input("Descrição: ")

    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO curso (nome, descricao) VALUES (%s, %s)",
            (nome, descricao)
        )
        conexao.commit()
        print("✅ Curso cadastrado com sucesso!")
    except Exception as e:
        print("❌ Erro ao cadastrar curso:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_cursos():
    print("\n=== LISTA DE CURSOS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, descricao FROM curso ORDER BY id")
        cursos = cursor.fetchall()
        if not cursos:
            print("Nenhum curso encontrado.")
        else:
            for c in cursos:
                print(f"[{c[0]}] {c[1]} - {c[2]}")
    except Exception as e:
        print("❌ Erro ao listar cursos:", e)
    finally:
        cursor.close()
        conexao.close()

def atualizar_curso():
    print("\n=== ATUALIZAR CURSO ===")
    listar_cursos()
    
    try:
        id_curso = int(input("ID do curso a atualizar: "))
        novo_nome = input("Novo nome: ")
        nova_descricao = input("Nova descrição: ")

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE curso SET nome = %s, descricao = %s WHERE id = %s",
            (novo_nome, nova_descricao, id_curso)
        )
        conexao.commit()
        print("✅ Curso atualizado com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao atualizar:", e)
    finally:
        cursor.close()
        conexao.close()

def excluir_curso():
    print("\n=== EXCLUIR CURSO ===")
    listar_cursos()
    
    try:
        id_curso = int(input("ID do curso para excluir: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM curso WHERE id = %s", (id_curso,))
        conexao.commit()
        print("✅ Curso excluído com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao excluir:", e)
    finally:
        cursor.close()
        conexao.close()