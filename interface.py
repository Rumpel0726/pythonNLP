
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from parse import ParseObj

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Чат-интерфейс")
        self.setGeometry(100, 100, 800, 600)

        self.parseobj = ParseObj()
        #self.parseobj.parse_main('https://www.yarnews.net/news/bymonth/2014/12/0/')


        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Область для отображения новости
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        layout.addWidget(self.content_area)
        # Настройка стилей для области контента
        self.content_area.setStyleSheet("""
            QTextEdit {
                font-size: 14pt;
                padding: 10px;
                background-color: #ffffff;
                border: 1px solid #cccccc;
            }
        """)

        # Поле ввода
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        layout.addWidget(self.input_field)

        # Кнопка отправки

        self.send_button = QPushButton("Вперед")
        self.send_button.clicked.connect(self.next_message)
        layout.addWidget(self.send_button)

    # def send_message(self):
    #     message = self.input_field.toPlainText()
    #     if message:
    #         self.chat_area.append(f"Вы: {message}")
    #         self.input_field.clear()
    
    
    # Функция для перехода к следующей новости
    def next_message(self):
        self.content_area.clear()
        self.content_area.append(str(self.parseobj.db.get_next_line()[3]))
