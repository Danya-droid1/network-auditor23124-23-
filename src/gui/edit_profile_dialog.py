# -*- coding: utf-8 -*-
"""
Диалоговое окно редактирования профиля пользователя.
Позволяет изменить ФИО и Email.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                               QLabel, QLineEdit, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt

from src.utils.dialogs import warning


class EditProfileDialog(QDialog):
    """
    Диалог редактирования профиля пользователя.
    """

    def __init__(self, parent=None, user_data: dict = None):
        """
        Инициализация диалога.

        :param parent: Родительское окно
        :param user_data: Текущие данные пользователя
        """
        super().__init__(parent)
        self.user_data = user_data or {}
        self.setWindowTitle("Редактирование профиля")
        self.resize(450, 300)
        self.init_ui()

    def init_ui(self):
        """Инициализация формы диалога."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Редактирование профиля")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(title)

        # Форма редактирования
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Логин (только для отображения)
        self.username_label = QLabel(self.user_data.get('username', 'N/A'))
        self.username_label.setStyleSheet("""
            QLabel {
                color: #a0a0b0;
                background: transparent;
                padding: 6px;
                border: 1px solid #3a3a52;
                border-radius: 4px;
            }
        """)
        form_layout.addRow("Логин (нельзя изменить):", self.username_label)

        # Роль (только для отображения)
        self.role_label = QLabel(self.user_data.get('role', 'N/A').capitalize())
        self.role_label.setStyleSheet("""
            QLabel {
                color: #a0a0b0;
                background: transparent;
                padding: 6px;
                border: 1px solid #3a3a52;
                border-radius: 4px;
            }
        """)
        form_layout.addRow("Роль (нельзя изменить):", self.role_label)

        # ФИО (редактируемое)
        self.fullname_input = QLineEdit()
        self.fullname_input.setText(self.user_data.get('full_name', ''))
        self.fullname_input.setPlaceholderText("Введите ФИО")
        form_layout.addRow("ФИО:", self.fullname_input)

        # Email (редактируемое)
        self.email_input = QLineEdit()
        self.email_input.setText(self.user_data.get('email', ''))
        self.email_input.setPlaceholderText("example@muiv.ru")
        form_layout.addRow("Email:", self.email_input)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("💾 Сохранить")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        save_btn.clicked.connect(self.save_profile)

        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white; 
                padding: 10px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save_profile(self):
        """Сохранение изменений профиля."""
        new_fullname = self.fullname_input.text().strip()
        new_email = self.email_input.text().strip()

        if not new_fullname:
            warning(self, "Ошибка", "Поле ФИО не может быть пустым.")
            return

        if new_email and '@' not in new_email:
            warning(self, "Ошибка", "Некорректный формат Email.")
            return

        self.accept()

    def get_user_data(self) -> dict:
        """Получение обновлённых данных пользователя."""
        return {
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip()
        }