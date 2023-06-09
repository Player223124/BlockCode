from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import algorithm

def res():
    if not ui.textV.toPlainText():
        try:
            if ui.matrixG.isChecked() == True:
                ui.textOut.setText(algorithm.enter_G(ui.textEnter.toPlainText()))
            elif ui.matrixH.isChecked() == True:
                ui.textOut.setText(algorithm.enter_H(ui.textEnter.toPlainText()))
            else:
                ui.textOut.setText('Выберите тип матрицы')
        except:
            ui.textOut.setText('Убедитесь, что ввод выполнен верно')
    else:
        try:
            if ui.matrixG.isChecked() == True:
                ui.textOut.setText(f'{algorithm.enter_G(ui.textEnter.toPlainText())}{algorithm.enter_VG(ui.textEnter.toPlainText(), ui.textV.toPlainText())}')
            elif ui.matrixH.isChecked() == True:
                ui.textOut.setText(f'{algorithm.enter_H(ui.textEnter.toPlainText())}{algorithm.enter_VH(ui.textEnter.toPlainText(), ui.textV.toPlainText())}')
            else:
                ui.textOut.setText('Выберите тип матрицы')
        except:
            ui.textOut.setText('Убедитесь, что ввод выполнен верно')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    ui.textEnter.setText('1 0 1 1 1 1 0 0\n0 1 1 1 0 1 0 0\n0 0 1 1 1 0 1 0\n0 0 0 1 1 1 0 1')
    ui.textV.setText('1 0 0 0 0 1 0 0')

    ui.enter.clicked.connect(lambda: res())
    sys.exit(app.exec_())