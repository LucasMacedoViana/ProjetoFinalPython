from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from CadAluno import Ui_CadAlunos
import pymysql.cursors


class Banco:
    def __init__(self):
        self.conexao = pymysql.connect(host="localhost",
                                       user="root",
                                       password="admin",
                                       database="escola",
                                       cursorclass=pymysql.cursors.DictCursor)

    def listarAlunos(self):
        with self.conexao.cursor() as cursor:
            try:
                sql = "SELECT * FROM aluno"
                cursor.execute(sql)
                resultado = cursor.fetchall()
                return resultado

            except Exception as erro:
                print(f'Erro ao buscar os dados. Erro: {erro}')

    def inserirAluno(self, nome, idade, curso):
        with self.conexao.cursor() as cursor:
            try:
                sql = "INSERT INTO aluno (nome, idade, curso) VALUES " \
                      "(%s, %s, %s)"
                cursor.execute(sql, (nome, idade, curso))
                self.conexao.commit()

            except Exception as erro:
                print(f'Erro ao cadastrar: {erro}')

    def editarAluno(self, nome, idade, curso, matricula):
        with self.conexao.cursor() as cursor:
            try:
                sql = "UPDATE aluno SET nome = %s, idade = %s, curso = %s" \
                      "WHERE matricula = %s"
                cursor.execute(sql, (nome, idade, curso, matricula))
                self.conexao.commit()

            except Exception as erro:
                print(f'Erro ao editar. Erro: {erro}')


class Janela(QMainWindow, Ui_CadAlunos):
    def __init__(self):
        super().__init__()

        self.db = Banco()

        self.setupUi(self)

        self.carregarTabela()

        # evento
        self.tb_alunos.cellClicked.connect(self.tabelaClicou)
        self.btn_novo.clicked.connect(self.inserir)
        self.btn_editar.clicked.connect(self.editar)

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

    def tabelaClicou(self, row):
        matricula = self.tb_alunos.item(row, 0).text()
        nome = self.tb_alunos.item(row, 1).text()
        idade = self.tb_alunos.item(row, 2).text()

        self.txt_matricula.setText(matricula)
        self.txt_nome.setText(nome)
        self.txt_idade.setText(idade)

        self.habilitarBotoes()

    def inserir(self):
        nome = self.txt_nome.text()
        idade = self.txt_idade.text()
        curso = self.cb_curso.currentText()

        self.db.inserirAluno(nome, idade, curso)
        QMessageBox.information(self, "Sucesso!", "Aluno cadastrado com sucesso!")
        self.limparCampos()
        self.carregarTabela()

    def editar(self):
        matricula = self.txt_matricula.text()
        nome = self.txt_nome.text()
        idade = self.txt_idade.text()
        curso = self.cb_curso.currentText()

        resultado = QMessageBox.question(self, "Tem certeza?",
                                         "Deseja alterar os dados?",
                                         QMessageBox.Yes | QMessageBox.No)

        if resultado == QMessageBox.Yes:
            self.db.editarAluno(nome, idade, curso, matricula)
            QMessageBox.information(self, "Atualizado", "Aluno alterado com sucesso")
            self.limparCampos()
            self.desabilitarBotoes()
            self.carregarTabela()
        else:
            self.limparCampos()
            self.desabilitarBotoes()

    def limparCampos(self):
        self.txt_nome.setText('')
        self.txt_idade.setText('')
        self.txt_matricula.setText('')

    def habilitarBotoes(self):
        self.btn_editar.setEnabled(True)
        self.btn_excluir.setEnabled(True)

    def desabilitarBotoes(self):
        self.btn_editar.setEnabled(False)
        self.btn_excluir.setEnabled(False)


app = QApplication([])
window = Janela()
window.show()
app.exec()