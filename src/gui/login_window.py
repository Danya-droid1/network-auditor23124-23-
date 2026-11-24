# -*- coding: utf-8 -*-
# Окно авторизации пользователя.
# Проверяет учётные данные через UserManager и БД.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt

from src.utils.dialogs import warning


class LoginWindow(QMainWindow):
    """Окно входа в систему Network Auditor."""

    def __init__(self, user_manager):
        """
        Инициализация окна авторизации.

        :param user_manager: Экземпляр UserManager для работы с БД
        """
        super().__init__()
        self.user_manager = user_manager
        self.setWindowTitle("Network Auditor — Вход в систему")
        self.resize(400, 300)
        self.init_ui()

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
        self.username_input.returnPressed.connect(self.authenticate)
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.returnPressed.connect(self.authenticate)
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
        """Проверка учётных данных через БД."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            warning(self, "Ошибка", "Пожалуйста, введите логин и пароль.")
            return

        # Аутентификация через UserManager
        user_data = self.user_manager.authenticate(username, password)

        if user_data:
            self.open_main_window(user_data)
        else:
            warning(self, "Ошибка", "Неверный логин или пароль")

    def open_main_window(self, user_data: dict):
        """Открытие главного окна после успешной авторизации."""
        from src.gui.main_window import MainWindow
        # Передаём user_manager и user_data
        self.main_window = MainWindow(user_data, self.user_manager)
        self.main_window.show()
        self.close()