# -*- coding: utf-8 -*-
"""
Окно личного кабинета пользователя.
Отображает данные профиля и форму смены пароля.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6 для построения интерфейса
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QMessageBox, QFrame)
from PySide6.QtCore import Qt


class ProfileWindow(QWidget):
    """
    Личный кабинет пользователя.
    Показывает информацию о текущем пользователе и форму смены пароля.
    """

    def __init__(self, user_data: dict):
        """
        Инициализация окна личного кабинета.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        super().__init__()
        # Сохраняем данные пользователя для отображения
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("Личный кабинет")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        # === Блок информации о пользователе ===
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #ecf0f1; padding: 15px; border-radius: 5px;")
        info_layout = QVBoxLayout(info_frame)

        # Выводим данные пользователя
        info_layout.addWidget(QLabel(f"Логин: {self.user_data.get('username')}"))
        info_layout.addWidget(QLabel(f"ФИО: {self.user_data.get('full_name', 'Не указано')}"))
        info_layout.addWidget(QLabel(f"Роль: {self.user_data.get('role', 'Не указана').capitalize()}"))
        info_layout.addWidget(QLabel("Статус учётной записи: Активна"))
        info_layout.addWidget(QLabel("Последний вход: Сегодня"))

        layout.addWidget(info_frame)

        layout.addSpacing(20)

        # === Форма смены пароля ===
        layout.addWidget(QLabel("Смена пароля:"))

        # Поле ввода текущего пароля
        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        self.old_password.setPlaceholderText("Текущий пароль")
        layout.addWidget(self.old_password)

        # Поле ввода нового пароля
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("Новый пароль")
        layout.addWidget(self.new_password)

        # Поле подтверждения нового пароля
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Подтвердите новый пароль")
        layout.addWidget(self.confirm_password)

        # Кнопка смены пароля
        self.change_pwd_btn = QPushButton("Сменить пароль")
        self.change_pwd_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        self.change_pwd_btn.clicked.connect(self.change_password)
        layout.addWidget(self.change_pwd_btn)

        layout.addStretch()
        self.setLayout(layout)

    def change_password(self):
        """
        Обработка нажатия кнопки смены пароля.
        Проверяет совпадение нового пароля и подтверждения.
        """
        new_pwd = self.new_password.text()
        confirm = self.confirm_password.text()

        # Проверка заполнения полей
        if not new_pwd or not confirm:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return

        # Проверка совпадения паролей
        if new_pwd != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        # TODO: Реализовать сохранение нового пароля в БД
        QMessageBox.information(self, "Успех", "Пароль успешно изменён")