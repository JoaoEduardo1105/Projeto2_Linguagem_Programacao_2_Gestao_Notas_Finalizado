from model.conexao import conectar

def lancar_nota():
    print("\n=== LANÇAR NOTA ===")
    
    from controller.controller_matricula import listar_matriculas
    listar_matriculas()
    
    try:
        id_matricula = int(input("ID da matrícula: "))
        nota1 = float(input("Nota 1: "))
        nota2 = float(input("Nota 2: "))
        nota_final = float(input("Nota Final: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        
        # Verificar se já existe nota para esta matrícula
        cursor.execute("SELECT id FROM nota WHERE id_matricula = %s", (id_matricula,))
        nota_existente = cursor.fetchone()
        
        if nota_existente:
            # Atualizar nota existente
            cursor.execute("""
                UPDATE nota SET nota1 = %s, nota2 = %s, nota_final = %s 
                WHERE id_matricula = %s
            """, (nota1, nota2, nota_final, id_matricula))
        else:
            # Inserir nova nota
            cursor.execute("""
                INSERT INTO nota (id_matricula, nota1, nota2, nota_final) 
                VALUES (%s, %s, %s, %s)
            """, (id_matricula, nota1, nota2, nota_final))
        
        conexao.commit()
        print("✅ Nota lançada/atualizada com sucesso!")
    except ValueError:
        print("❌ Valores devem ser números!")
    except Exception as e:
        print("❌ Erro ao lançar nota:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_notas():
    print("\n=== LISTA DE NOTAS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT n.id, u.nome as aluno, d.nome as disciplina, 
                   n.nota1, n.nota2, n.nota_final, n.media
            FROM nota n
            JOIN matricula m ON n.id_matricula = m.id
            JOIN usuario u ON m.id_aluno = u.id
            JOIN turma t ON m.id_turma = t.id
            JOIN disciplina d ON t.id_disciplina = d.id
            ORDER BY u.nome, d.nome
        """)
        notas = cursor.fetchall()
        if not notas:
            print("Nenhuma nota encontrada.")
        else:
            for n in notas:
                status = "✅ APROVADO" if n[6] >= 6.0 else "❌ REPROVADO"
                print(f"[{n[0]}] {n[1]} - {n[2]}: N1={n[3]}, N2={n[4]}, NF={n[5]}, MÉDIA={n[6]:.2f} - {status}")
    except Exception as e:
        print("❌ Erro ao listar notas:", e)
    finally:
        cursor.close()
        conexao.close()

def consultar_notas_aluno():
    """Consulta notas de qualquer aluno (para professores)"""
    print("\n=== CONSULTAR NOTAS DO ALUNO ===")
    email = input("Email do aluno: ")

    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT u.nome as aluno, d.nome as disciplina, 
                   n.nota1, n.nota2, n.nota_final, n.media
            FROM nota n
            JOIN matricula m ON n.id_matricula = m.id
            JOIN usuario u ON m.id_aluno = u.id
            JOIN turma t ON m.id_turma = t.id
            JOIN disciplina d ON t.id_disciplina = d.id
            WHERE u.email = %s
            ORDER BY d.nome
        """, (email,))
        
        notas = cursor.fetchall()
        if not notas:
            print("Nenhuma nota encontrada para este aluno.")
        else:
            print(f"\n📊 NOTAS DE {notas[0][0].upper()}:")
            for n in notas:
                status = "✅ APROVADO" if n[5] >= 6.0 else "❌ REPROVADO"
                print(f"  📚 {n[1]}: N1={n[2]}, N2={n[3]}, NF={n[4]}, MÉDIA={n[5]:.2f} - {status}")
                
    except Exception as e:
        print("❌ Erro ao consultar notas:", e)
    finally:
        cursor.close()
        conexao.close()

def consultar_notas_aluno_logado(aluno_id):
    """Consulta notas do aluno logado (sem precisar digitar email)"""
    print(f"\n=== CONSULTANDO SUAS NOTAS ===")
    
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT u.nome as aluno, d.nome as disciplina, 
                   n.nota1, n.nota2, n.nota_final, n.media
            FROM nota n
            JOIN matricula m ON n.id_matricula = m.id
            JOIN usuario u ON m.id_aluno = u.id
            JOIN turma t ON m.id_turma = t.id
            JOIN disciplina d ON t.id_disciplina = d.id
            WHERE u.id = %s
            ORDER BY d.nome
        """, (aluno_id,))
        
        notas = cursor.fetchall()
        if not notas:
            print("📭 Você não tem notas lançadas ainda.")
        else:
            print(f"\n📊 SUAS NOTAS:")
            for n in notas:
                status = "✅ APROVADO" if n[5] >= 6.0 else "❌ REPROVADO"
                print(f"  📚 {n[1]}:")
                print(f"     N1: {n[2]} | N2: {n[3]} | NF: {n[4]}")
                print(f"     MÉDIA: {n[5]:.2f} - {status}")
            print(f"\n📈 Total de disciplinas: {len(notas)}")
                
    except Exception as e:
        print(f"❌ Erro ao consultar notas: {e}")
    finally:
        cursor.close()
        conexao.close()