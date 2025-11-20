# 🎓 Sistema de Gestão de Notas  
Projeto final da disciplina de **Linguagem de Programação 2**, utilizando **Python + Flask**, **PostgreSQL**, HTML/CSS e o padrão **MVC**.

Este sistema permite gerenciar **usuários, cursos, disciplinas, turmas, matrículas e notas**, seguindo regras de acesso baseadas no tipo do usuário.

---

## 📌 Funcionalidades

### 👨‍💼 Administrador
- Gerenciar usuários  
- Gerenciar cursos  
- Gerenciar disciplinas  
- Gerenciar turmas  
- Gerenciar matrículas  
- Visualizar notas  

### 👨‍🏫 Professor
- Visualizar suas próprias turmas  
- Lançar notas  
- Editar notas  
- Visualizar alunos e matrículas  
- Sem permissão para criar cursos/disciplinas/turmas  

### 🎓 Aluno
- Visualizar suas matrículas  
- Visualizar suas notas  
- Sem permissões de edição  

---

## 🏗 Arquitetura (MVC)

projeto_gestao_notas/
│
├── src/
│ ├── app.py # Arquivo principal Flask
│ ├── model/
│ │ └── conexao.py # Conexão com PostgreSQL
│ ├── templates/ # Views HTML (Jinja2)
│ └── static/
│ └── style.css # CSS do frontend
│
├── database/
│ └── Banco_de_dados.sql # Script completo do banco
│
├── .env # Variáveis de ambiente (não subir no GitHub)
├── .env.example # Modelo de .env para outros usuários
├── README.md # Documentação
└── Dependencias.txt # Bibliotecas necessárias


---

## 🛠 Tecnologias utilizadas

- **Python 3**
- **Flask** (backend)
- **Jinja2** (templating)
- **HTML5 / CSS3**
- **PostgreSQL**
- **psycopg2** (driver)
- **python-dotenv** (variáveis de ambiente)
- Padrão **MVC**

---

## 🧰 Como instalar e rodar o projeto

### 1️⃣ Instale as dependências

No terminal, dentro da pasta do projeto:

```bash
python -m pip install -r Dependencias.txt

2️⃣ Configure o arquivo .env

Crie um arquivo .env dentro da pasta principal:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestao_notas
DB_USER=postgres
DB_PASSWORD=SENHA_AQUI
FLASK_SECRET=uma_chave_secreta

Você pode usar o arquivo .env.example como referência.
3️⃣ Crie o banco de dados

No PostgreSQL:

CREATE DATABASE gestao_notas;

Em seguida execute o script:

database/Banco_de_dados.sql

Isso criará todas as tabelas e o administrador padrão:

email: admin@admin.com
senha: admin123

4️⃣ Execute o servidor

Dentro da pasta src/ execute:

python app.py

O sistema estará disponível em:

http://127.0.0.1:5000

🎨 Frontend

O frontend é composto por:

    templates HTML (Jinja2)

    CSS personalizado em static/style.css

Não é necessário rodar nada adicional — o Flask já serve tudo automaticamente.
🔐 Controle de acesso por tipo de usuário
Ação	Admin	Professor	Aluno
Gerenciar usuários	✔	✖	✖
Gerenciar cursos	✔	✖	✖
Gerenciar disciplinas	✔	✖	✖
Gerenciar turmas	✔	✖	✖
Gerenciar matrículas	✔	✖	✖
Lançar e editar notas	✖	✔	✖
Visualizar turmas próprias	✖	✔	✖
Ver notas próprias	✖	✖	✔
📦 Dependências

Arquivo Dependencias.txt:

flask
psycopg2-binary
python-dotenv

📝 Autor

João Eduardo Godoy
Projeto para a disciplina de Linguagem de Programação 2 – IFSP
