from model.conexao import conectar

def criar_admin_padrao():
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE email = 'admin@admin.com'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)",
                ("Administrador", "admin@admin.com", "admin123", "administrador")
            )
            conexao.commit()
            print("✅ Admin padrão criado: admin@admin.com / admin123")
    except Exception as e:
        print("❌ Erro ao criar admin:", e)
    finally:
        cursor.close()
        conexao.close()

def login():
    print("\n=== LOGIN ===")
    email = input("Email: ")
    senha = input("Senha: ")

    conexao = conectar()
    if not conexao:
        return None
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario and usuario[2] == senha:
            print(f"✅ Login realizado! Bem-vindo(a), {usuario[1]}")
            return {"id": usuario[0], "nome": usuario[1], "tipo": usuario[3]}
        else:
            print("❌ Email ou senha incorretos.")
            return None
    except Exception as e:
        print("❌ Erro no login:", e)
        return None
    finally:
        cursor.close()
        conexao.close()

def cadastrar_usuario():
    print("\n=== CADASTRAR USUÁRIO ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    tipo = input("Tipo (aluno/professor/administrador): ")

    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)",
            (nome, email, senha, tipo)
        )
        conexao.commit()
        print("✅ Usuário cadastrado com sucesso!")
    except Exception as e:
        print("❌ Erro ao cadastrar usuário:", e)
    finally:
        cursor.close()
        conexao.close()

def listar_usuarios():
    print("\n=== LISTA DE USUÁRIOS ===")
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, email, tipo_usuario FROM usuario ORDER BY id")
        usuarios = cursor.fetchall()
        if not usuarios:
            print("Nenhum usuário encontrado.")
        else:
            for u in usuarios:
                print(f"[{u[0]}] {u[1]} ({u[2]}) - {u[3]}")
    except Exception as e:
        print("❌ Erro ao listar usuários:", e)
    finally:
        cursor.close()
        conexao.close()

def atualizar_usuario():
    print("\n=== ATUALIZAR USUÁRIO ===")
    listar_usuarios()
    
    try:
        id_user = int(input("ID do usuário a atualizar: "))
        novo_nome = input("Novo nome: ")
        novo_email = input("Novo email: ")
        nova_senha = input("Nova senha: ")
        novo_tipo = input("Novo tipo (aluno/professor/administrador): ")

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE usuario SET nome = %s, email = %s, senha = %s, tipo_usuario = %s WHERE id = %s",
            (novo_nome, novo_email, nova_senha, novo_tipo, id_user)
        )
        conexao.commit()
        print("✅ Usuário atualizado com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao atualizar:", e)
    finally:
        cursor.close()
        conexao.close()

def excluir_usuario():
    print("\n=== EXCLUIR USUÁRIO ===")
    listar_usuarios()
    
    try:
        id_user = int(input("ID do usuário para excluir: "))

        conexao = conectar()
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id_user,))
        conexao.commit()
        print("✅ Usuário excluído com sucesso!")
    except ValueError:
        print("❌ ID deve ser um número!")
    except Exception as e:
        print("❌ Erro ao excluir:", e)
    finally:
        cursor.close()
        conexao.close()