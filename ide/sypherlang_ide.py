import os
import sys
import subprocess
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog,
                             QAction, QMessageBox, QVBoxLayout, QWidget, QPushButton, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class SypherLangIDE(QMainWindow):
    output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SypherLang IDE")
        self.setGeometry(200, 100, 1200, 800)

        # Initialize UI components
        self.editor = QTextEdit(self)
        self.editor.setFont(QFont("Courier", 12))
        self.output_display = QTextEdit(self)
        self.output_display.setFont(QFont("Courier", 10))
        self.output_display.setReadOnly(True)

        # Set Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("SypherLang Code Editor:"))
        layout.addWidget(self.editor, 7)
        layout.addWidget(QLabel("Output Console:"))
        layout.addWidget(self.output_display, 3)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Menu
        self.init_menu()

        # Signals
        self.output_signal.connect(self.update_output)

    def init_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")

        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Run Menu
        run_menu = menu_bar.addMenu("&Run")
        run_action = QAction("&Run Code", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SypherLang File", "", "SypherLang Files (*.sypher);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.editor.setText(file.read())

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save SypherLang File", "", "SypherLang Files (*.sypher);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.editor.toPlainText())

    def run_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "Warning", "Cannot run empty code.")
            return
        self.output_display.clear()
        threading.Thread(target=self.execute_code, args=(code,)).start()

    def execute_code(self, code):
        try:
            # Assume 'sypherlang_interpreter' is the command-line tool to run SypherLang code
            process = subprocess.Popen(['sypherlang_interpreter'],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)
            stdout, stderr = process.communicate(input=code)

            if stderr:
                self.output_signal.emit(f"[ERROR]\n{stderr}")
            else:
                self.output_signal.emit(f"[OUTPUT]\n{stdout}")
        except FileNotFoundError:
            self.output_signal.emit("[ERROR]\nSypherLang interpreter not found. Please make sure it is installed and available in your PATH.")
        except Exception as e:
            self.output_signal.emit(f"[ERROR]\n{str(e)}")

    def update_output(self, text):
        self.output_display.append(text)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = SypherLangIDE()
    ide.show()
    sys.exit(app.exec_())
