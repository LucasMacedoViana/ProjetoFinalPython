from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from CadAluno import Ui_CadAlunos
import pymysql.cursors



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
