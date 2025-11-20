# =========================
# app.py — Parte 1
# Sistema de Gestão de Notas (versão final, sem hash)
# =========================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from model.conexao import conectar
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "segredo123")

# -------------------------
# Helpers de DB
# -------------------------
def query_fetchall(sql, params=()):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()

def query_fetchone(sql, params=()):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()

def execute(sql, params=()):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
    finally:
        conn.close()

def ensure_login():
    return "usuario" in session

def tipo_usuario():
    return session["usuario"]["tipo"] if "usuario" in session else None

# -------------------------
# LOGIN / LOGOUT
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        row = query_fetchone("SELECT id, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))
        if row:
            id_u, nome, senha_db, tipo = row
            if senha == senha_db:
                session.clear()
                session["usuario"] = {"id": id_u, "nome": nome, "tipo": tipo}
                if tipo == "administrador":
                    return redirect(url_for("home_admin"))
                elif tipo == "professor":
                    return redirect(url_for("home_professor"))
                else:
                    return redirect(url_for("home_aluno"))
            else:
                flash("Senha incorreta.", "danger")
        else:
            flash("Usuário não encontrado.", "danger")
    return render_template("login.html", titulo="Login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------
# HOME
# -------------------------
@app.route("/")
def index():
    if not ensure_login():
        return redirect(url_for("login"))
    tipo = tipo_usuario()
    if tipo == "administrador":
        return redirect(url_for("home_admin"))
    elif tipo == "professor":
        return redirect(url_for("home_professor"))
    else:
        return redirect(url_for("home_aluno"))

@app.route("/home/admin")
def home_admin():
    if not ensure_login():
        return redirect(url_for("login"))
    return render_template("home_admin.html", titulo="Painel Admin")

@app.route("/home/professor")
def home_professor():
    if not ensure_login():
        return redirect(url_for("login"))
    return render_template("home_professor.html", titulo="Painel Professor")

@app.route("/home/aluno")
def home_aluno():
    if not ensure_login():
        return redirect(url_for("login"))
    return render_template("home_aluno.html", titulo="Painel Aluno")

# -------------------------
# CRUD — USUÁRIOS
# -------------------------
@app.route("/usuarios")
def usuarios():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("SELECT id, nome, email, tipo_usuario FROM usuario ORDER BY id")
    return render_template("usuarios.html", usuarios=data, titulo="Usuários")

@app.route("/usuarios/novo", methods=["GET", "POST"])
def usuario_novo():
    if not ensure_login():
        return redirect(url_for("login"))
    # permitir somente admin para criar outros admins? aqui permitimos admin e professor criar alunos/usuarios
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        tipo = request.form.get("tipo_usuario")
        execute("INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)",
                (nome, email, senha, tipo))
        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for("usuarios"))
    return render_template("usuario_form.html", titulo="Novo Usuário", usuario_obj=None)

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def usuario_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))
    row = query_fetchone("SELECT id, nome, email, tipo_usuario FROM usuario WHERE id = %s", (id,))
    if not row:
        flash("Usuário não encontrado.", "warning")
        return redirect(url_for("usuarios"))
    usuario_obj = {"id": row[0], "nome": row[1], "email": row[2], "tipo_usuario": row[3]}
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        tipo = request.form.get("tipo_usuario")
        execute("UPDATE usuario SET nome=%s, email=%s, tipo_usuario=%s WHERE id=%s", (nome, email, tipo, id))
        flash("Usuário atualizado.", "success")
        return redirect(url_for("usuarios"))
    return render_template("usuario_form.html", titulo="Editar Usuário", usuario_obj=usuario_obj)

@app.route("/usuarios/excluir/<int:id>", methods=["POST"])
def usuario_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    execute("DELETE FROM usuario WHERE id = %s", (id,))
    flash("Usuário excluído.", "success")
    return redirect(url_for("usuarios"))
# =========================
# app.py — Parte 2 (continuação)
# =========================

# -------------------------
# CRUD — CURSOS
# -------------------------
@app.route("/cursos")
def cursos():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("SELECT id, nome, descricao FROM curso ORDER BY id")
    return render_template("cursos.html", cursos=data, titulo="Cursos")

@app.route("/cursos/novo", methods=["GET", "POST"])
def curso_novo():
    if not ensure_login():
        return redirect(url_for("login"))
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        execute("INSERT INTO curso (nome, descricao) VALUES (%s, %s)", (nome, descricao))
        flash("Curso cadastrado.", "success")
        return redirect(url_for("cursos"))
    return render_template("curso_form.html", titulo="Novo Curso", curso_obj=None)

@app.route("/cursos/editar/<int:id>", methods=["GET", "POST"])
def curso_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))
    row = query_fetchone("SELECT id, nome, descricao FROM curso WHERE id = %s", (id,))
    if not row:
        flash("Curso não encontrado.", "warning")
        return redirect(url_for("cursos"))
    curso_obj = {"id": row[0], "nome": row[1], "descricao": row[2]}
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        execute("UPDATE curso SET nome=%s, descricao=%s WHERE id=%s", (nome, descricao, id))
        flash("Curso atualizado.", "success")
        return redirect(url_for("cursos"))
    return render_template("curso_form.html", titulo="Editar Curso", curso_obj=curso_obj)

@app.route("/cursos/excluir/<int:id>", methods=["POST"])
def curso_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    execute("DELETE FROM curso WHERE id = %s", (id,))
    flash("Curso excluído.", "success")
    return redirect(url_for("cursos"))

# -------------------------
# CRUD — DISCIPLINAS
# -------------------------
@app.route("/disciplinas")
def disciplinas():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("""
        SELECT d.id, d.nome, d.descricao, c.nome as curso, d.id_curso
        FROM disciplina d
        LEFT JOIN curso c ON c.id = d.id_curso
        ORDER BY d.id
    """)
    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")
    return render_template("disciplinas.html", disciplinas=data, cursos=cursos, titulo="Disciplinas")

@app.route("/disciplinas/novo", methods=["GET", "POST"])
def disciplina_nova():
    if not ensure_login():
        return redirect(url_for("login"))
    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        id_curso = request.form.get("id_curso")
        execute("INSERT INTO disciplina (nome, descricao, id_curso) VALUES (%s, %s, %s)", (nome, descricao, id_curso))
        flash("Disciplina criada.", "success")
        return redirect(url_for("disciplinas"))
    return render_template("disciplina_form.html", titulo="Nova Disciplina", cursos=cursos, disciplina_obj=None)

@app.route("/disciplinas/editar/<int:id>", methods=["GET", "POST"])
def disciplina_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))
    row = query_fetchone("SELECT id, nome, descricao, id_curso FROM disciplina WHERE id = %s", (id,))
    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")
    if not row:
        flash("Disciplina não encontrada.", "warning")
        return redirect(url_for("disciplinas"))
    disciplina_obj = {"id": row[0], "nome": row[1], "descricao": row[2], "id_curso": row[3]}
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        id_curso = request.form.get("id_curso")
        execute("UPDATE disciplina SET nome=%s, descricao=%s, id_curso=%s WHERE id=%s", (nome, descricao, id_curso, id))
        flash("Disciplina atualizada.", "success")
        return redirect(url_for("disciplinas"))
    return render_template("disciplina_form.html", titulo="Editar Disciplina", cursos=cursos, disciplina_obj=disciplina_obj)

@app.route("/disciplinas/excluir/<int:id>", methods=["POST"])
def disciplina_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    execute("DELETE FROM disciplina WHERE id = %s", (id,))
    flash("Disciplina excluída.", "success")
    return redirect(url_for("disciplinas"))

# -------------------------
# CRUD — TURMAS
# -------------------------
@app.route("/turmas")
def turmas():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("""
        SELECT t.id, t.nome, d.nome as disciplina, u.nome as professor, t.id_disciplina, t.id_professor
        FROM turma t
        LEFT JOIN disciplina d ON d.id = t.id_disciplina
        LEFT JOIN usuario u ON u.id = t.id_professor
        ORDER BY t.id
    """)
    disciplinas = query_fetchall("SELECT id, nome FROM disciplina ORDER BY id")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario = 'professor' ORDER BY id")
    return render_template("turmas.html", turmas=data, disciplinas=disciplinas, professores=professores, titulo="Turmas")

@app.route("/turmas/novo", methods=["GET", "POST"])
def turma_nova():
    if not ensure_login():
        return redirect(url_for("login"))
    
    # Somente administradores podem criar novas turmas
    if tipo_usuario() != 'administrador':
        flash("Somente administradores podem criar novas turmas.", "danger")
        return redirect(url_for("turmas"))
    disciplinas = query_fetchall("SELECT id, nome FROM disciplina ORDER BY id")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario = 'professor' ORDER BY id")
    if request.method == "POST":
        nome = request.form.get("nome")
        id_disciplina = request.form.get("id_disciplina")
        id_professor = request.form.get("id_professor") or None
        execute("INSERT INTO turma (nome, id_disciplina, id_professor) VALUES (%s, %s, %s)", (nome, id_disciplina, id_professor))
        flash("Turma criada.", "success")
        return redirect(url_for("turmas"))
    return render_template("turma_form.html", titulo="Nova Turma", disciplinas=disciplinas, professores=professores, turma_obj=None)

@app.route("/turmas/editar/<int:id>", methods=["GET", "POST"])
def turma_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))
    # bloquear alunos
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem editar turmas.", "danger")
        return redirect(url_for("turmas"))
    turma = query_fetchone("SELECT id, nome, id_disciplina, id_professor FROM turma WHERE id = %s", (id,))
    if not turma:
        flash("Turma não encontrada.", "warning")
        return redirect(url_for("turmas"))
    disciplinas = query_fetchall("SELECT id, nome FROM disciplina ORDER BY id")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario = 'professor' ORDER BY id")
    turma_obj = {"id": turma[0], "nome": turma[1], "id_disciplina": turma[2], "id_professor": turma[3]}
    if request.method == "POST":
        nome = request.form.get("nome")
        id_disciplina = request.form.get("id_disciplina")
        id_professor = request.form.get("id_professor") or None
        execute("UPDATE turma SET nome=%s, id_disciplina=%s, id_professor=%s WHERE id=%s", (nome, id_disciplina, id_professor, id))
        flash("Turma atualizada.", "success")
        return redirect(url_for("turmas"))
    return render_template("turma_form.html", titulo="Editar Turma", turma_obj=turma_obj, disciplinas=disciplinas, professores=professores)

@app.route("/turmas/excluir/<int:id>", methods=["POST"])
def turma_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem excluir turmas.", "danger")
        return redirect(url_for("turmas"))
    execute("DELETE FROM turma WHERE id = %s", (id,))
    flash("Turma excluída.", "success")
    return redirect(url_for("turmas"))

# -------------------------
# CRUD — MATRÍCULAS
# -------------------------
@app.route("/matriculas")
def matriculas():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("""
        SELECT m.id, u.nome as aluno, t.nome as turma, d.nome as disciplina, m.id_aluno, m.id_turma
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        JOIN disciplina d ON d.id = t.id_disciplina
        ORDER BY m.id
    """)
    alunos = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario = 'aluno' ORDER BY id")
    turmas = query_fetchall("SELECT id, nome FROM turma ORDER BY id")
    return render_template("matriculas.html", matriculas=data, alunos=alunos, turmas=turmas, titulo="Matrículas")

@app.route("/matriculas/novo", methods=["GET", "POST"])
def matricula_nova():
    if not ensure_login():
        return redirect(url_for("login"))
    # bloquear alunos
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem cadastrar matrículas.", "danger")
        return redirect(url_for("matriculas"))
    alunos = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario = 'aluno' ORDER BY id")
    turmas = query_fetchall("SELECT id, nome FROM turma ORDER BY id")
    if request.method == "POST":
        id_aluno = request.form.get("id_aluno")
        id_turma = request.form.get("id_turma")
        execute("INSERT INTO matricula (id_aluno, id_turma) VALUES (%s, %s)", (id_aluno, id_turma))
        flash("Matrícula criada.", "success")
        return redirect(url_for("matriculas"))
    return render_template("matricula_form.html", titulo="Nova Matrícula", alunos=alunos, turmas=turmas)

@app.route("/matriculas/excluir/<int:id>", methods=["POST"])
def matricula_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem excluir matrículas.", "danger")
        return redirect(url_for("matriculas"))
    execute("DELETE FROM matricula WHERE id = %s", (id,))
    flash("Matrícula excluída.", "success")
    return redirect(url_for("matriculas"))

# -------------------------
# CRUD — NOTAS
# -------------------------
@app.route("/notas")
def notas():
    if not ensure_login():
        return redirect(url_for("login"))
    data = query_fetchall("""
        SELECT n.id, u.nome as aluno, d.nome as disciplina, n.nota1, n.nota2, n.nota_final, n.media, n.id_matricula
        FROM nota n
        JOIN matricula m ON m.id = n.id_matricula
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        JOIN disciplina d ON d.id = t.id_disciplina
        ORDER BY n.id
    """)
    matriculas = query_fetchall("""
        SELECT m.id, u.nome || ' - ' || t.nome as descricao
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)
    return render_template("notas.html", notas=data, matriculas=matriculas, titulo="Notas")

@app.route("/notas/novo", methods=["GET", "POST"])
def nota_nova():
    if not ensure_login():
        return redirect(url_for("login"))
    # bloquear alunos
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem lançar notas.", "danger")
        return redirect(url_for("notas"))
    matriculas = query_fetchall("""
        SELECT m.id, u.nome || ' - ' || t.nome as descricao
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)
    if request.method == "POST":
        id_matricula = request.form.get("id_matricula")
        nota1 = request.form.get("nota1") or None
        nota2 = request.form.get("nota2") or None
        nota_final = request.form.get("nota_final") or None
        execute("INSERT INTO nota (id_matricula, nota1, nota2, nota_final) VALUES (%s, %s, %s, %s)",
                (id_matricula, nota1, nota2, nota_final))
        flash("Nota lançada.", "success")
        return redirect(url_for("notas"))
    return render_template("nota_form.html", titulo="Lançar Nota", matriculas=matriculas, nota_obj=None)

@app.route("/notas/editar/<int:id>", methods=["GET", "POST"])
def nota_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))
    # bloquear alunos para editar
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem editar notas.", "danger")
        return redirect(url_for("notas"))
    row = query_fetchone("SELECT id, id_matricula, nota1, nota2, nota_final FROM nota WHERE id = %s", (id,))
    if not row:
        flash("Nota não encontrada.", "warning")
        return redirect(url_for("notas"))
    nota_obj = {"id": row[0], "id_matricula": row[1], "nota1": row[2], "nota2": row[3], "nota_final": row[4]}
    matriculas = query_fetchall("""
        SELECT m.id, u.nome || ' - ' || t.nome as descricao
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)
    if request.method == "POST":
        nota1 = request.form.get("nota1") or None
        nota2 = request.form.get("nota2") or None
        nota_final = request.form.get("nota_final") or None
        execute("UPDATE nota SET nota1=%s, nota2=%s, nota_final=%s WHERE id=%s", (nota1, nota2, nota_final, id))
        flash("Nota atualizada.", "success")
        return redirect(url_for("notas"))
    return render_template("nota_form.html", titulo="Editar Nota", matriculas=matriculas, nota_obj=nota_obj)

@app.route("/notas/excluir/<int:id>", methods=["POST"])
def nota_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))
    if tipo_usuario() == 'aluno':
        flash("Alunos não podem excluir notas.", "danger")
        return redirect(url_for("notas"))
    execute("DELETE FROM nota WHERE id = %s", (id,))
    flash("Nota excluída.", "success")
    return redirect(url_for("notas"))

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
