from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QToolBar,
    QPushButton, QFileDialog, QFontComboBox, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QTextCharFormat, QFont
from PyQt5.QtCore import Qt
import sys

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Панель инструментов
        toolbar = QToolBar()
        layout.addWidget(toolbar)

        self.bold_button = QPushButton("B")
        self.bold_button.setCheckable(True)
        self.bold_button.clicked.connect(self.toggle_bold)
        toolbar.addWidget(self.bold_button)

        self.italic_button = QPushButton("I")
        self.italic_button.setCheckable(True)
        self.italic_button.clicked.connect(self.toggle_italic)
        toolbar.addWidget(self.italic_button)

        self.underline_button = QPushButton("U")
        self.underline_button.setCheckable(True)
        self.underline_button.clicked.connect(self.toggle_underline)
        toolbar.addWidget(self.underline_button)

        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.set_font)
        toolbar.addWidget(self.font_box)

        self.font_size_box = QComboBox()
        self.font_size_box.setEditable(True)
        for i in range(8, 31, 2):
            self.font_size_box.addItem(str(i))
        self.font_size_box.setCurrentText("12")
        self.font_size_box.currentTextChanged.connect(self.set_font_size)
        toolbar.addWidget(self.font_size_box)

        self.undo_button = QPushButton("↶")
        self.undo_button.clicked.connect(self.undo)
        toolbar.addWidget(self.undo_button)

        self.redo_button = QPushButton("↷")
        self.redo_button.clicked.connect(self.redo)
        toolbar.addWidget(self.redo_button)

        self.save_button = QPushButton("💾")
        self.save_button.clicked.connect(self.save_file)
        toolbar.addWidget(self.save_button)

        self.open_button = QPushButton("📂")
        self.open_button.clicked.connect(self.open_file)
        toolbar.addWidget(self.open_button)

        # Сам текст
        self.text = QTextEdit()
        layout.addWidget(self.text)

    # Стили текста
    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_button.isChecked() else QFont.Normal)
        self.text.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_button.isChecked())
        self.text.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_button.isChecked())
        self.text.mergeCurrentCharFormat(fmt)

    # Шрифт
    def set_font(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.text.mergeCurrentCharFormat(fmt)

    def set_font_size(self, size):
        try:
            size = int(size)
        except ValueError:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.text.mergeCurrentCharFormat(fmt)

    # Файл
    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "HTML Files (*.html);;Text Files (*.txt)")
        if path:
            if path.endswith(".txt"):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text.toPlainText())
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text.toHtml())

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "HTML Files (*.html);;Text Files (*.txt)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if path.endswith(".txt"):
                    self.text.setPlainText(content)
                else:
                    self.text.setHtml(content)

    # Отмена / Повтор
    def undo(self):
        self.text.undo()

    def redo(self):
        self.text.redo()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
