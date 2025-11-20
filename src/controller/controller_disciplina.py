from model.conexao import conectar

def cadastrar_disciplina():
    print("\n=== CADASTRAR DISCIPLINA ===")
    nome = input("Nome da disciplina: ")
    descricao = input("Descrição: ")
    
    from controller.controller_curso import listar_cursos
    listar_cursos()
    
    try:
        id_curso = int(input("ID do curso: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO disciplina (nome, descricao, id_curso) VALUES (%s, %s, %s)",
            (nome, descricao, id_curso)
        )
        conexao.commit()
        print("✅ Disciplina cadastrada com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao cadastrar disciplina:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_disciplinas():
    print("\n=== LISTA DE DISCIPLINAS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT d.id, d.nome, d.descricao, c.nome as curso 
            FROM disciplina d 
            JOIN curso c ON d.id_curso = c.id 
            ORDER BY d.id
        """)
        disciplinas = cursor.fetchall()
        if not disciplinas:
            print("Nenhuma disciplina encontrada.")
        else:
            for d in disciplinas:
                print(f"[{d[0]}] {d[1]} - {d[2]} (Curso: {d[3]})")
    except Exception as e:
        print("❌ Erro ao listar disciplinas:", e)
    finally:
        cursor.close()
        conexao.close()

def atualizar_disciplina():
    print("\n=== ATUALIZAR DISCIPLINA ===")
    listar_disciplinas()
    
    try:
        id_disc = int(input("ID da disciplina a atualizar: "))
        novo_nome = input("Novo nome: ")
        nova_descricao = input("Nova descrição: ")
        novo_id_curso = int(input("Novo ID do curso: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE disciplina SET nome = %s, descricao = %s, id_curso = %s WHERE id = %s",
            (novo_nome, nova_descricao, novo_id_curso, id_disc)
        )
        conexao.commit()
        print("✅ Disciplina atualizada com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao atualizar:", e)
    finally:
        cursor.close()
        conexao.close()

def excluir_disciplina():
    print("\n=== EXCLUIR DISCIPLINA ===")
    listar_disciplinas()
    
    try:
        id_disc = int(input("ID da disciplina para excluir: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = %s", (id_disc,))
        conexao.commit()
        print("✅ Disciplina excluída com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao excluir:", e)
    finally:
        cursor.close()
        conexao.close()