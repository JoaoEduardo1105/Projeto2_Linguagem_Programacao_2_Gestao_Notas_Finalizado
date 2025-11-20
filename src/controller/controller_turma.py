from model.conexao import conectar

def cadastrar_turma():
    print("\n=== CADASTRAR TURMA ===")
    nome = input("Nome da turma: ")
    
    from controller.controller_disciplina import listar_disciplinas
    from controller.controller_usuario import listar_usuarios
    
    print("\n--- Disciplinas disponíveis ---")
    listar_disciplinas()
    print("\n--- Professores disponíveis ---")
    # Listar apenas professores
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome FROM usuario WHERE tipo_usuario = 'professor'")
        professores = cursor.fetchall()
        for p in professores:
            print(f"[{p[0]}] {p[1]}")
    except Exception as e:
        print("❌ Erro ao listar professores:", e)
        return
    finally:
        cursor.close()
        conexao.close()
    
    try:
        id_disciplina = int(input("ID da disciplina: "))
        id_professor = int(input("ID do professor: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO turma (nome, id_disciplina, id_professor) VALUES (%s, %s, %s)",
            (nome, id_disciplina, id_professor)
        )
        conexao.commit()
        print("✅ Turma cadastrada com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao cadastrar turma:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_turmas():
    print("\n=== LISTA DE TURMAS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT t.id, t.nome, d.nome as disciplina, u.nome as professor
            FROM turma t
            JOIN disciplina d ON t.id_disciplina = d.id
            JOIN usuario u ON t.id_professor = u.id
            ORDER BY t.id
        """)
        turmas = cursor.fetchall()
        if not turmas:
            print("Nenhuma turma encontrada.")
        else:
            for t in turmas:
                print(f"[{t[0]}] {t[1]} - {t[2]} (Prof: {t[3]})")
    except Exception as e:
        print("❌ Erro ao listar turmas:", e)
    finally:
        cursor.close()
        conexao.close()

def atualizar_turma():
    print("\n=== ATUALIZAR TURMA ===")
    listar_turmas()
    
    try:
        id_turma = int(input("ID da turma a atualizar: "))
        novo_nome = input("Novo nome: ")
        novo_id_disciplina = int(input("Novo ID da disciplina: "))
        novo_id_professor = int(input("Novo ID do professor: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE turma SET nome = %s, id_disciplina = %s, id_professor = %s WHERE id = %s",
            (novo_nome, novo_id_disciplina, novo_id_professor, id_turma)
        )
        conexao.commit()
        print("✅ Turma atualizada com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao atualizar:", e)
    finally:
        cursor.close()
        conexao.close()

def excluir_turma():
    print("\n=== EXCLUIR TURMA ===")
    listar_turmas()
    
    try:
        id_turma = int(input("ID da turma para excluir: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM turma WHERE id = %s", (id_turma,))
        conexao.commit()
        print("✅ Turma excluída com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao excluir:", e)
    finally:
        cursor.close()
        conexao.close()