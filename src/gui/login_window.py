# -*- coding: utf-8 -*-
"""
Окно авторизации пользователя.
Проверяет учётные данные и открывает главное окно.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6 для создания графического интерфейса
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt


class LoginWindow(QMainWindow):
    """
    Окно входа в систему Network Auditor.
    Содержит поля для ввода логина и пароля.
    """

    def __init__(self):
        """Инициализация окна авторизации."""
        super().__init__()
        # Устанавливаем заголовок окна
        self.setWindowTitle("Network Auditor - Вход в систему")
        # Устанавливаем размер окна
        self.resize(400, 300)
        # Инициализируем интерфейс
        self.init_ui()

        # Тестовые учётные данные для демонстрации
        # В реальной системе данные берутся из БД
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
        # Создаём центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаём вертикальный layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок приложения
        title_label = QLabel("Система аудита сетевой безопасности")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Поле ввода логина
        layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        layout.addWidget(self.username_input)

        # Поле ввода пароля (скрытый ввод)
        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрываем вводимые символы
        self.password_input.setPlaceholderText("Введите пароль")
        layout.addWidget(self.password_input)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)  # Подключаем обработчик
        layout.addWidget(self.login_button)

        central_widget.setLayout(layout)

    def authenticate(self):
        """
        Проверка введённых учётных данных.
        Сравнивает введённые данные с тестовыми пользователями.
        """
        # Получаем введённые данные
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Проверяем наличие пользователя и совпадение пароля
        if username in self.test_users and self.test_users[username]["password"] == password:
            # Формируем данные пользователя
            user_data = {
                "username": username,
                "role": self.test_users[username]["role"],
                "full_name": self.test_users[username]["full_name"]
            }
            # Открываем главное окно
            self.open_main_window(user_data)
        else:
            # Показываем сообщение об ошибке
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_main_window(self, user_data: dict):
        """
        Открытие главного окна приложения после успешной авторизации.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        # Импортируем здесь, чтобы избежать циклических импортов
        from src.gui.main_window import MainWindow
        # Создаём и показываем главное окно
        self.main_window = MainWindow(user_data)
        self.main_window.show()
        # Закрываем окно авторизации
        self.close()