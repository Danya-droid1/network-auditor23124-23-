# -*- coding: utf-8 -*-
# Диалоговое окно смены пароля пользователя.
# Проверяет текущий пароль и сохраняет новый в БД через UserManager.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                               QLabel, QLineEdit, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt

from src.utils.dialogs import warning


class ChangePasswordDialog(QDialog):
    """Диалог смены пароля пользователя."""

    def __init__(self, parent=None, user_manager=None, user_id: int = None):
        """
        Инициализация диалога.

        :param parent: Родительское окно
        :param user_manager: Экземпляр UserManager
        :param user_id: ID текущего пользователя
        """
        super().__init__(parent)
        self.user_manager = user_manager
        self.user_id = user_id
        self.setWindowTitle("Смена пароля")
        self.resize(450, 280)
        self.init_ui()

    def init_ui(self):
        """Инициализация формы диалога."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Смена пароля")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        self.old_password.setPlaceholderText("Введите текущий пароль")
        form_layout.addRow("Текущий пароль:", self.old_password)

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("Минимум 8 символов")
        form_layout.addRow("Новый пароль:", self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Повторите новый пароль")
        form_layout.addRow("Подтверждение:", self.confirm_password)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()

        change_btn = QPushButton("🔑 Сменить пароль")
        change_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)
        change_btn.clicked.connect(self.change_password)

        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white; 
                padding: 10px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(change_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def change_password(self):
        """Обработка смены пароля через БД."""
        old_pwd = self.old_password.text()
        new_pwd = self.new_password.text()
        confirm = self.confirm_password.text()

        if not old_pwd or not new_pwd or not confirm:
            warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if len(new_pwd) < 8:
            warning(self, "Ошибка", "Новый пароль должен содержать минимум 8 символов.")
            return

        if new_pwd != confirm:
            warning(self, "Ошибка", "Пароли не совпадают.")
            return

        # Смена пароля через UserManager
        success = self.user_manager.change_password(self.user_id, old_pwd, new_pwd)

        if success:
            self.accept()
        else:
            warning(self, "Ошибка", "Неверный текущий пароль или ошибка сохранения.")