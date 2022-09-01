from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from CadAluno import Ui_CadAlunos
import pymysql.cursors

class Banco:
    def __init__(self):
        self.conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="escola",
            cursorclass=pymysql.cursors.DictCursor
        )

    def listarAlunos(self):
        with self.conexao.cursor() as cursor:
            try:
                sql = "select * from aluno"
                cursor.execute(sql)
                resultado = cursor.fetchall()
                return resultado
            except Exception as erro:
                print(f'Err ao buscar os dados, erro: {erro}')


    def inserirAluno(self, nome, idade, curso):
        with self.conexao.cursor() as cursor:
            try:
                sql = "INSERT INTO aluno (nome, idade, curso) VALUES " \
                      "(%s, %s, %s)"
                cursor.execute(sql, (nome, idade, curso))
                self.conexao.commit()

            except Exception as erro:
                print(f'Erro ao cadastrar: {erro}')

    def consultar(self,nome):
        with self.conexao.cursor() as cursor:
            try:
                sql = "selecto * from aluno where nome like %s"
                cursor.execute(sql(nome))
                self.conexao.commit()
            except Exception as erro:
                print(f'erro ao cadastrar: {erro}')






class Janela(QMainWindow, Ui_CadAlunos):
    def __init__(self):
         super().__init__()
         self.db = Banco()
         self.setupUi(self)
         self.carregarTabela()




         self.btn_novo.clicked.connect(self.inserir)

         self.btn_editar.setEnabled(False)
         self.btn_excluir.setEnabled(False)

    def carregarTabela(self):
        resultado = self.db.listarAlunos()
        self.tb_alunos.setRowCount(len(resultado))
        linha = 0

        for aluno in resultado:
            self.tb_alunos.setItem(linha, 0, QtWidgets.QTableWidgetItem(str(aluno['matricula'])))
            self.tb_alunos.setItem(linha, 1, QtWidgets.QTableWidgetItem(aluno['nome']))
            self.tb_alunos.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(aluno['idade'])))
            self.tb_alunos.setItem(linha, 3, QtWidgets.QTableWidgetItem(aluno['curso']))
            linha += 1

    def inserir(self):
        nome = self.txt_nome.text()
        idade = self.txt_idade.text()
        curso = self.cb_curso.currentText()

        self.db.inserirAluno(nome, idade, curso)
        QMessageBox.information(self, "Sucesso!", "Aluno cadastrado com sucesso!")
        self.limparCampos()



    def limparCampos(self):
        self.txt_nome.setText('')
        self.txt_idade.setText('')
        self.txt_matricula.setText('')



app = QApplication([])
window = Janela()
window.show()
app.exec()
