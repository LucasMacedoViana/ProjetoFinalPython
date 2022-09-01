DROP DATABASE escola;

create database escola;

use escola;

create table aluno(
	matricula int PRIMARy key auto_increment,
    nome varchar (255),
    idade int,
    curso varchar (255)
);

