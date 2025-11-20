-- Criar tabela de usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) CHECK (tipo_usuario IN ('aluno', 'professor', 'administrador'))
);

-- Criar tabela de curso
CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- Criar tabela de disciplina
CREATE TABLE disciplina (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    id_curso INT REFERENCES cursos(id) ON DELETE CASCADE
);

-- Criar tabela de turma
CREATE TABLE turma (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    id_disciplina INT REFERENCES disciplinas(id) ON DELETE CASCADE,
    id_professor INT REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Criar tabela de matricula
CREATE TABLE matricula (
    id SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES usuarios(id) ON DELETE CASCADE,
    id_turma INT REFERENCES turmas(id) ON DELETE CASCADE,
    data_matricula DATE DEFAULT CURRENT_DATE,
    UNIQUE (id_aluno, id_turma)
);

-- Criar tabela de nota
CREATE TABLE nota (
    id SERIAL PRIMARY KEY,
    id_matricula INT REFERENCES matriculas(id) ON DELETE CASCADE,
    nota1 NUMERIC(5,2),
    nota2 NUMERIC(5,2),
    nota_final NUMERIC(5,2),
    media NUMERIC(5,2) GENERATED ALWAYS AS ((COALESCE(nota1,0) + COALESCE(nota2,0) + COALESCE(nota_final,0))/3) STORED,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--Inserir dados usuario
INSERT INTO usuario (nome, email, senha, tipo_usuario)
VALUES
('João Eduardo', 'joao.eduardo@escola.com', '123456', 'aluno'),
('Fulano Silva', 'fulano.silva@escola.com', '123456', 'aluno'),
('Ciclano Pereira', 'ciclano.pereira@escola.com', '123456', 'aluno'),
('Prof. Beltrano Santos', 'beltrano.santos@escola.com', 'prof123', 'professor'),
('Prof. João Pereira', 'joao.pereira@escola.com', 'prof123', 'professor'),
('Admin Geral', 'admin@escola.com', 'admin123', 'administrador');

--Inserir dados curso
INSERT INTO curso (nome, descricao)
VALUES
('Tecnologia em Analise e Desenvolvimento de Sistemas', 'Curso voltado à área de tecnologia e desenvolvimento de sistemas.'),
('Teste', 'Curso focado sobre testar o banco de Dados criado.');

--Inserir dados disciplina
INSERT INTO disciplina (nome, descricao, id_curso)
VALUES
('Banco de Dados', 'Introdução a bancos relacionais e SQL.', 1),
('Disciplina teste', 'Apenas um teste.', 2);

--Inserir dados turma
INSERT INTO turma (nome, id_disciplina, id_professor)
VALUES
('Turma BD 2025A', 1, 4),  -- Prof. Mariana Silva
('Turma POO 2025A', 2, 5), -- Prof. João Pereira
('Turma GP 2025A', 3, 4);  -- Prof. Mariana Silva

--Inserir dados matricula
INSERT INTO matricula (id_aluno, id_turma)
VALUES
(1, 1), 
(2, 1), 
(3, 2), 
(1, 2), 
(2, 3); 

--Inserir dados nota
INSERT INTO nota (id_matricula, nota1, nota2, nota_final)
VALUES
(1, 8.5, 7.0, 9.0),
(2, 6.0, 8.0, 7.5),
(3, 9.0, 8.5, 8.0),
(4, 7.5, 7.5, 8.5),
(5, 8.0, 6.5, 7.0);
