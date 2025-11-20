&nbsp;		Sistema de Gestão de Notas Acadêmicas



Funcionalidades



Autenticação com 3 tipos de usuário (Admin, Professor, Aluno)

Gestão completa de usuários, cursos, disciplinas e turmas

Sistema de matrículas

Lançamento e consulta de notas

Cálculo automático de médias

Relatórios acadêmicos



Tecnologias



Backend: Python

Banco de Dados: PostgreSQL

Arquitetura: MVC (Model-View-Controller)

Autenticação: Sistema próprio



Instalação:

\# Criar ambiente virtual

python -m venv venv



\# Ativar no Windows:

venv\\Scripts\\activate



\# Ativar no Linux/Mac:

source venv/bin/activate



pip -m install -r requirements.txt



\# Conecte ao PostgreSQL

psql -U postgres



\# Crie o banco

CREATE DATABASE sistema\_notas;



\# Saia e execute o script

\\q

psql -U postgres -d sistema\_notas -f database/Banco\_de\_dados.sql





DB\_HOST=localhost

DB\_NAME=sistema\_notas

DB\_USER=postgres

DB\_PASSWORD=sua\_senha

DB\_PORT=5432

