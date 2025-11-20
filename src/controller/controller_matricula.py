from model.conexao import conectar

def cadastrar_matricula():
    print("\n=== CADASTRAR MATRÍCULA ===")
    
    from controller.controller_usuario import listar_usuarios
    from controller.controller_turma import listar_turmas
    
    print("\n--- Alunos disponíveis ---")
    # Listar apenas alunos
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome FROM usuario WHERE tipo_usuario = 'aluno'")
        alunos = cursor.fetchall()
        for a in alunos:
            print(f"[{a[0]}] {a[1]}")
    except Exception as e:
        print("❌ Erro ao listar alunos:", e)
        return
    finally:
        cursor.close()
        conexao.close()
    
    print("\n--- Turmas disponíveis ---")
    listar_turmas()
    
    try:
        id_aluno = int(input("ID do aluno: "))
        id_turma = int(input("ID da turma: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO matricula (id_aluno, id_turma) VALUES (%s, %s)",
            (id_aluno, id_turma)
        )
        conexao.commit()
        print("✅ Matrícula realizada com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao realizar matrícula:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_matriculas():
    print("\n=== LISTA DE MATRÍCULAS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT m.id, u.nome as aluno, t.nome as turma, d.nome as disciplina, m.data_matricula
            FROM matricula m
            JOIN usuario u ON m.id_aluno = u.id
            JOIN turma t ON m.id_turma = t.id
            JOIN disciplina d ON t.id_disciplina = d.id
            ORDER BY m.id
        """)
        matriculas = cursor.fetchall()
        if not matriculas:
            print("Nenhuma matrícula encontrada.")
        else:
            for m in matriculas:
                print(f"[{m[0]}] {m[1]} - {m[2]} ({m[3]}) - {m[4]}")
    except Exception as e:
        print("❌ Erro ao listar matrículas:", e)
    finally:
        cursor.close()
        conexao.close()

def excluir_matricula():
    print("\n=== EXCLUIR MATRÍCULA ===")
    listar_matriculas()
    
    try:
        id_matricula = int(input("ID da matrícula para excluir: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM matricula WHERE id = %s", (id_matricula,))
        conexao.commit()
        print("✅ Matrícula excluída com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao excluir:", e)
    finally:
        cursor.close()
        conexao.close()