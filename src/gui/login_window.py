# -*- coding: utf-8 -*-
"""
Окно авторизации пользователя.
Проверяет учётные данные и открывает главное окно.
Все диалоги используют русские кнопки через обёртку dialogs.py.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt

# Импорт обёртки диалогов с русскими кнопками
from src.utils.dialogs import info, warning


class LoginWindow(QMainWindow):
    """
    Окно входа в систему Network Auditor.
    Содержит поля для ввода логина и пароля.
    """

    def __init__(self):
        """Инициализация окна авторизации."""
        super().__init__()
        self.setWindowTitle("Network Auditor — Вход в систему")
        self.resize(400, 300)
        self.init_ui()

        # Тестовые учётные данные для демонстрации
        self.test_users = {
            "admin": {
                "password": "AdminSecure2026!",
                "role": "admin",
                "full_name": "Администратор ИБ"
            },
            "analyst": {
                "password": "AnalystSecure2026!",
                "role": "analyst",
                "full_name": "Аналитик ИБ"
            },
            "auditor": {
                "password": "AuditorSecure2026!",
                "role": "auditor",
                "full_name": "Аудитор"
            }
        }

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("Система аудита сетевой безопасности")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a9eff; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacing(20)

        layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)

        central_widget.setLayout(layout)

    def authenticate(self):
        """
        Проверка введённых учётных данных.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if username in self.test_users and self.test_users[username]["password"] == password:
            user_data = {
                "username": username,
                "role": self.test_users[username]["role"],
                "full_name": self.test_users[username]["full_name"]
            }
            self.open_main_window(user_data)
        else:
            # Русская кнопка "ОК"
            warning(self, "Ошибка", "Неверный логин или пароль")

    def open_main_window(self, user_data: dict):
        """
        Открытие главного окна приложения после успешной авторизации.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        from src.gui.main_window import MainWindow
        self.main_window = MainWindow(user_data)
        self.main_window.show()
        self.close()