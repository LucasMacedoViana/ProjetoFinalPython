from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from CadAluno import Ui_CadAlunos
import pymysql.cursors

class Banco:
    def __init__(self):
        self.conexao = pymysql.connect(
            host="localhost",
            user="root",
            password=,
            database="escola",
            cursorclass=pymysql.cursors.DictCursor
        )

    def inserirAluno(self,nome,idade,curso):
        with self.conexao.cursor() as curso:
            try:
                sql = "INSERT INTO aluno (nome, idade, curso) VALUES (%s, %s, %s)"
                curso.execute(sql(nome, idade, curso))
                self.conexao.commit()
            except Exception as erro:
                print(f'erro ao cadastrar: {erro}')




class Janela(QMainWindow, Ui_CadAlunos):
    def __init__(self):
         super().__init__()

         self.setupUi(self)

         self.btn_editar.setEnabled(False)
         self.btn_excluir.setEnabled(False)


app = QApplication([])
window = Janela()
window.show()
app.exec()
