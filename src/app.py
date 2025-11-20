# =====================================
# app.py — Sistema de Gestão de Notas
# COMPLETO — SEM CRIPTOGRAFIA
# =====================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from model.conexao import conectar
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "segredo123")


# =====================================
# Funções auxiliares para o banco
# =====================================

def query_fetchall(sql, params=()):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        conn.close()


def query_fetchone(sql, params=()):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        data = cur.fetchone()
        cur.close()
        return data
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
    if "usuario" not in session:
        return False
    return True


# =====================================
# LOGIN / LOGOUT
# =====================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        user = query_fetchone(
            "SELECT id, nome, senha, tipo_usuario FROM usuario WHERE email = %s",
            (email,)
        )

        if user:
            if senha == user[2]:  # comparação direta sem hash
                session["usuario"] = {
                    "id": user[0],
                    "nome": user[1],
                    "tipo": user[3]
                }

                if user[3] == "administrador":
                    return redirect(url_for("home_admin"))
                elif user[3] == "professor":
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


# =====================================
# HOME DE CADA TIPO DE USUÁRIO
# =====================================

@app.route("/")
def index():
    if not ensure_login():
        return redirect(url_for("login"))

    tipo = session["usuario"]["tipo"]

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
    return render_template("home_admin.html", titulo="Painel Administrativo")


@app.route("/home/professor")
def home_professor():
    if not ensure_login():
        return redirect(url_for("login"))
    return render_template("home_professor.html", titulo="Painel do Professor")


@app.route("/home/aluno")
def home_aluno():
    if not ensure_login():
        return redirect(url_for("login"))
    return render_template("home_aluno.html", titulo="Painel do Aluno")


# =====================================
# CRUD — USUÁRIOS
# =====================================

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

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo_usuario"]

        execute(
            "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)",
            (nome, email, senha, tipo)
        )

        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("usuarios"))

    return render_template("usuario_form.html", titulo="Novo Usuário", usuario_obj=None)


@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def usuario_editar(id):
    if not ensure_login():
        return redirect(url_for("login"))

    user = query_fetchone("SELECT id, nome, email, tipo_usuario FROM usuario WHERE id = %s", (id,))

    if not user:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("usuarios"))

    usuario_obj = {
        "id": user[0],
        "nome": user[1],
        "email": user[2],
        "tipo_usuario": user[3]
    }

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        tipo = request.form["tipo_usuario"]

        execute(
            "UPDATE usuario SET nome=%s, email=%s, tipo_usuario=%s WHERE id=%s",
            (nome, email, tipo, id)
        )

        flash("Usuário atualizado!", "success")
        return redirect(url_for("usuarios"))

    return render_template("usuario_form.html", titulo="Editar Usuário", usuario_obj=usuario_obj)


@app.route("/usuarios/excluir/<int:id>", methods=["POST"])
def usuario_excluir(id):
    if not ensure_login():
        return redirect(url_for("login"))

    execute("DELETE FROM usuario WHERE id = %s", (id,))
    flash("Usuário excluído!", "success")
    return redirect(url_for("usuarios"))


# =====================================
# CRUD — CURSOS
# =====================================

@app.route("/cursos")
def cursos():
    if not ensure_login():
        return redirect(url_for("login"))

    data = query_fetchall("SELECT id, nome, descricao FROM curso ORDER BY id")

    return render_template("cursos.html", cursos=data, titulo="Cursos")


@app.route("/cursos/novo", methods=["GET", "POST"])
def curso_novo():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        execute("INSERT INTO curso (nome, descricao) VALUES (%s, %s)", (nome, descricao))
        flash("Curso cadastrado!", "success")
        return redirect(url_for("cursos"))

    return render_template("curso_form.html", titulo="Novo Curso", curso_obj=None)


@app.route("/cursos/editar/<int:id>", methods=["GET", "POST"])
def curso_editar(id):
    curso = query_fetchone("SELECT id, nome, descricao FROM curso WHERE id = %s", (id,))

    if not curso:
        flash("Curso não encontrado!", "danger")
        return redirect(url_for("cursos"))

    curso_obj = {"id": curso[0], "nome": curso[1], "descricao": curso[2]}

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        execute("UPDATE curso SET nome=%s, descricao=%s WHERE id=%s", (nome, descricao, id))
        flash("Curso atualizado!", "success")
        return redirect(url_for("cursos"))

    return render_template("curso_form.html", titulo="Editar Curso", curso_obj=curso_obj)


@app.route("/cursos/excluir/<int:id>", methods=["POST"])
def curso_excluir(id):
    execute("DELETE FROM curso WHERE id = %s", (id,))
    flash("Curso excluído!", "success")
    return redirect(url_for("cursos"))


# =====================================
# CRUD — DISCIPLINAS
# =====================================

@app.route("/disciplinas")
def disciplinas():
    if not ensure_login():
        return redirect(url_for("login"))

    data = query_fetchall("""
        SELECT d.id, d.nome, d.descricao, c.nome AS curso
        FROM disciplina d
        JOIN curso c ON c.id = d.id_curso
        ORDER BY d.id
    """)

    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")

    return render_template("disciplinas.html", disciplinas=data, cursos=cursos, titulo="Disciplinas")


@app.route("/disciplinas/novo", methods=["GET", "POST"])
def disciplina_nova():
    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        curso_id = request.form["id_curso"]

        execute(
            "INSERT INTO disciplina (nome, descricao, id_curso) VALUES (%s, %s, %s)",
            (nome, descricao, curso_id)
        )

        flash("Disciplina criada!", "success")
        return redirect(url_for("disciplinas"))

    return render_template("disciplina_form.html", titulo="Nova Disciplina", disciplina_obj=None, cursos=cursos)


@app.route("/disciplinas/editar/<int:id>", methods=["GET", "POST"])
def disciplina_editar(id):
    disciplina = query_fetchone(
        "SELECT id, nome, descricao, id_curso FROM disciplina WHERE id = %s",
        (id,)
    )

    cursos = query_fetchall("SELECT id, nome FROM curso ORDER BY id")

    if not disciplina:
        flash("Disciplina não encontrada!", "danger")
        return redirect(url_for("disciplinas"))

    disciplina_obj = {
        "id": disciplina[0],
        "nome": disciplina[1],
        "descricao": disciplina[2],
        "id_curso": disciplina[3],
    }

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        curso_id = request.form["id_curso"]

        execute(
            "UPDATE disciplina SET nome=%s, descricao=%s, id_curso=%s WHERE id=%s",
            (nome, descricao, curso_id, id)
        )

        flash("Disciplina atualizada!", "success")
        return redirect(url_for("disciplinas"))

    return render_template("disciplina_form.html", titulo="Editar Disciplina", disciplina_obj=disciplina_obj, cursos=cursos)


@app.route("/disciplinas/excluir/<int:id>", methods=["POST"])
def disciplina_excluir(id):
    execute("DELETE FROM disciplina WHERE id = %s", (id,))
    flash("Disciplina excluída!", "success")
    return redirect(url_for("disciplinas"))


# =====================================
# CRUD — TURMAS
# =====================================

@app.route("/turmas")
def turmas():
    if not ensure_login():
        return redirect(url_for("login"))

    data = query_fetchall("""
        SELECT t.id, t.nome, d.nome, u.nome
        FROM turma t
        JOIN disciplina d ON d.id = t.id_disciplina
        LEFT JOIN usuario u ON u.id = t.id_professor
        ORDER BY t.id
    """)

    disciplinas = query_fetchall("SELECT id, nome FROM disciplina")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario='professor'")

    return render_template("turmas.html", turmas=data, disciplinas=disciplinas, professores=professores, titulo="Turmas")


@app.route("/turmas/novo", methods=["GET", "POST"])
def turma_nova():
    disciplinas = query_fetchall("SELECT id, nome FROM disciplina")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario='professor'")

    if request.method == "POST":
        nome = request.form["nome"]
        disciplina_id = request.form["id_disciplina"]
        professor_id = request.form.get("id_professor") or None

        execute(
            "INSERT INTO turma (nome, id_disciplina, id_professor) VALUES (%s, %s, %s)",
            (nome, disciplina_id, professor_id)
        )

        flash("Turma criada!", "success")
        return redirect(url_for("turmas"))

    return render_template("turma_form.html", titulo="Nova Turma", turma_obj=None, disciplinas=disciplinas, professores=professores)


@app.route("/turmas/editar/<int:id>", methods=["GET", "POST"])
def turma_editar(id):
    turma = query_fetchone(
        "SELECT id, nome, id_disciplina, id_professor FROM turma WHERE id = %s",
        (id,)
    )

    disciplinas = query_fetchall("SELECT id, nome FROM disciplina")
    professores = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario='professor'")

    if not turma:
        flash("Turma não encontrada!", "danger")
        return redirect(url_for("turmas"))

    turma_obj = {
        "id": turma[0],
        "nome": turma[1],
        "id_disciplina": turma[2],
        "id_professor": turma[3],
    }

    if request.method == "POST":
        nome = request.form["nome"]
        disciplina_id = request.form["id_disciplina"]
        professor_id = request.form.get("id_professor") or None

        execute(
            "UPDATE turma SET nome=%s, id_disciplina=%s, id_professor=%s WHERE id=%s",
            (nome, disciplina_id, professor_id, id)
        )

        flash("Turma atualizada!", "success")
        return redirect(url_for("turmas"))

    return render_template("turma_form.html", titulo="Editar Turma", turma_obj=turma_obj, disciplinas=disciplinas, professores=professores)


@app.route("/turmas/excluir/<int:id>", methods=["POST"])
def turma_excluir(id):
    execute("DELETE FROM turma WHERE id = %s", (id,))
    flash("Turma excluída!", "success")
    return redirect(url_for("turmas"))


# =====================================
# CRUD — MATRÍCULAS
# =====================================

@app.route("/matriculas")
def matriculas():
    if not ensure_login():
        return redirect(url_for("login"))

    data = query_fetchall("""
        SELECT m.id, u.nome, t.nome, d.nome
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        JOIN disciplina d ON d.id = t.id_disciplina
        ORDER BY m.id
    """)

    alunos = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario='aluno'")
    turmas = query_fetchall("SELECT id, nome FROM turma")

    return render_template("matriculas.html", matriculas=data, alunos=alunos, turmas=turmas, titulo="Matrículas")


@app.route("/matriculas/novo", methods=["GET", "POST"])
def matricula_nova():
    alunos = query_fetchall("SELECT id, nome FROM usuario WHERE tipo_usuario='aluno'")
    turmas = query_fetchall("SELECT id, nome FROM turma")

    if request.method == "POST":
        aluno = request.form["id_aluno"]
        turma = request.form["id_turma"]

        execute("INSERT INTO matricula (id_aluno, id_turma) VALUES (%s, %s)", (aluno, turma))

        flash("Matrícula realizada!", "success")
        return redirect(url_for("matriculas"))

    return render_template("matricula_form.html", titulo="Nova Matrícula", alunos=alunos, turmas=turmas)


@app.route("/matriculas/excluir/<int:id>", methods=["POST"])
def matricula_excluir(id):
    execute("DELETE FROM matricula WHERE id = %s", (id,))
    flash("Matrícula excluída!", "success")
    return redirect(url_for("matriculas"))


# =====================================
# CRUD — NOTAS
# =====================================

@app.route("/notas")
def notas():
    if not ensure_login():
        return redirect(url_for("login"))

    data = query_fetchall("""
        SELECT 
            n.id,
            u.nome AS aluno,
            d.nome AS disciplina,
            n.nota1,
            n.nota2,
            n.nota_final,
            n.media
        FROM nota n
        JOIN matricula m ON m.id = n.id_matricula
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        JOIN disciplina d ON d.id = t.id_disciplina
        ORDER BY n.id
    """)

    matriculas = query_fetchall("""
        SELECT 
            m.id,
            u.nome || ' - ' || t.nome
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)

    return render_template("notas.html", notas=data, matriculas=matriculas, titulo="Notas")


@app.route("/notas/novo", methods=["GET", "POST"])
def nota_nova():
    matriculas = query_fetchall("""
        SELECT 
            m.id,
            u.nome || ' - ' || t.nome
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)

    if request.method == "POST":
        matricula = request.form["id_matricula"]
        n1 = request.form.get("nota1")
        n2 = request.form.get("nota2")
        nf = request.form.get("nota_final")

        execute(
            "INSERT INTO nota (id_matricula, nota1, nota2, nota_final) VALUES (%s, %s, %s, %s)",
            (matricula, n1, n2, nf)
        )

        flash("Nota lançada!", "success")
        return redirect(url_for("notas"))

    return render_template("nota_form.html", titulo="Nova Nota", matriculas=matriculas, nota_obj=None)


@app.route("/notas/editar/<int:id>", methods=["GET", "POST"])
def nota_editar(id):
    nota = query_fetchone(
        "SELECT id, id_matricula, nota1, nota2, nota_final FROM nota WHERE id = %s",
        (id,)
    )

    if not nota:
        flash("Nota não encontrada!", "danger")
        return redirect(url_for("notas"))

    nota_obj = {
        "id": nota[0],
        "id_matricula": nota[1],
        "nota1": nota[2],
        "nota2": nota[3],
        "nota_final": nota[4],
    }

    matriculas = query_fetchall("""
        SELECT 
            m.id,
            u.nome || ' - ' || t.nome
        FROM matricula m
        JOIN usuario u ON u.id = m.id_aluno
        JOIN turma t ON t.id = m.id_turma
        ORDER BY m.id
    """)

    if request.method == "POST":
        n1 = request.form.get("nota1")
        n2 = request.form.get("nota2")
        nf = request.form.get("nota_final")

        execute(
            "UPDATE nota SET nota1=%s, nota2=%s, nota_final=%s WHERE id=%s",
            (n1, n2, nf, id)
        )

        flash("Nota atualizada!", "success")
        return redirect(url_for("notas"))

    return render_template("nota_form.html", titulo="Editar Nota", matriculas=matriculas, nota_obj=nota_obj)


@app.route("/notas/excluir/<int:id>", methods=["POST"])
def nota_excluir(id):
    execute("DELETE FROM nota WHERE id = %s", (id,))
    flash("Nota excluída!", "success")
    return redirect(url_for("notas"))


# =====================================
# EXECUTAR A APLICAÇÃO
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
