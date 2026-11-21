# -*- coding: utf-8 -*-
"""
Окно личного кабинета пользователя.
Отображает данные профиля и позволяет их редактировать:
- ФИО
- Email
- Смена пароля
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFrame, QFormLayout)
from PySide6.QtCore import Qt, Signal

# Импорт обёртки диалогов с русскими кнопками
from src.utils.dialogs import info, warning


class ProfileWindow(QWidget):
    """
    Личный кабинет пользователя.
    Позволяет просматривать и редактировать данные профиля.
    """

    # Сигнал об изменении данных пользователя
    profile_updated = Signal(dict)

    def __init__(self, user_data: dict):
        """
        Инициализация окна личного кабинета.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        super().__init__()
        self.user_data = user_data.copy()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("Личный кабинет")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        # === Блок редактирования данных пользователя ===
        edit_header = QLabel("Редактирование профиля")
        edit_header.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #4a9eff; background: transparent; margin-top: 10px;")
        layout.addWidget(edit_header)

        # Форма редактирования
        form_frame = QFrame()
        form_frame.setObjectName("profileForm")
        form_frame.setStyleSheet("""
            QFrame#profileForm {
                background-color: #2a2a3e;
                border: 1px solid #3a3a52;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(10)

        # Логин (только для чтения)
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

        # Роль (только для чтения)
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

        layout.addWidget(form_frame)

        # Кнопка сохранения изменений профиля
        self.save_profile_btn = QPushButton("💾 Сохранить изменения профиля")
        self.save_profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.save_profile_btn.clicked.connect(self.save_profile)
        layout.addWidget(self.save_profile_btn)

        layout.addSpacing(20)

        # === Разделитель ===
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3a3a52; max-height: 2px;")
        layout.addWidget(separator)

        layout.addSpacing(10)

        # === Форма смены пароля ===
        pwd_header = QLabel("Смена пароля")
        pwd_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(pwd_header)

        pwd_frame = QFrame()
        pwd_frame.setObjectName("passwordForm")
        pwd_frame.setStyleSheet("""
            QFrame#passwordForm {
                background-color: #2a2a3e;
                border: 1px solid #3a3a52;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        pwd_layout = QFormLayout(pwd_frame)
        pwd_layout.setSpacing(10)

        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        self.old_password.setPlaceholderText("Введите текущий пароль")
        pwd_layout.addRow("Текущий пароль:", self.old_password)

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("Минимум 8 символов")
        pwd_layout.addRow("Новый пароль:", self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Повторите новый пароль")
        pwd_layout.addRow("Подтверждение:", self.confirm_password)

        layout.addWidget(pwd_frame)

        # Кнопка смены пароля
        self.change_pwd_btn = QPushButton("🔑 Сменить пароль")
        self.change_pwd_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)
        self.change_pwd_btn.clicked.connect(self.change_password)
        layout.addWidget(self.change_pwd_btn)

        layout.addStretch()
        self.setLayout(layout)

    def save_profile(self):
        """
        Сохранение изменений профиля (ФИО, Email).
        Отправляет сигнал profile_updated с обновлёнными данными.
        """
        new_fullname = self.fullname_input.text().strip()
        new_email = self.email_input.text().strip()

        # Валидация
        if not new_fullname:
            warning(self, "Ошибка", "Поле ФИО не может быть пустым.")
            return

        # Простая проверка email
        if new_email and '@' not in new_email:
            warning(self, "Ошибка", "Некорректный формат Email.")
            return

        # Обновляем данные
        self.user_data['full_name'] = new_fullname
        self.user_data['email'] = new_email

        # Отправляем сигнал об изменении
        self.profile_updated.emit(self.user_data)

        info(self, "Успех",
             f"Профиль успешно обновлён.\n\n"
             f"ФИО: {new_fullname}\n"
             f"Email: {new_email or 'не указан'}")

    def change_password(self):
        """
        Обработка нажатия кнопки смены пароля.
        Проверяет совпадение нового пароля и подтверждения.
        """
        old_pwd = self.old_password.text()
        new_pwd = self.new_password.text()
        confirm = self.confirm_password.text()

        # Проверка заполнения полей
        if not old_pwd or not new_pwd or not confirm:
            warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверка текущего пароля (для демо - сравниваем с тестовым)
        if old_pwd != "AdminSecure2026!" and old_pwd != "AnalystSecure2026!" and old_pwd != "AuditorSecure2026!":
            warning(self, "Ошибка", "Неверный текущий пароль.")
            return

        # Проверка длины нового пароля
        if len(new_pwd) < 8:
            warning(self, "Ошибка", "Новый пароль должен содержать минимум 8 символов.")
            return

        # Проверка совпадения паролей
        if new_pwd != confirm:
            warning(self, "Ошибка", "Пароли не совпадают.")
            return

        # TODO: Реализовать сохранение нового пароля в БД через bcrypt
        self.old_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()

        info(self, "Успех", "Пароль успешно изменён.\n\n"
                            "В реальной системе новый пароль был бы захеширован через bcrypt "
                            "и сохранён в таблицу users базы данных.")