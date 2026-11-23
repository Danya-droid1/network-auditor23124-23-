# -*- coding: utf-8 -*-
"""
Окно личного кабинета пользователя.
Отображает информацию о пользователе и предоставляет кнопки
для редактирования профиля и смены пароля.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal

from src.gui.edit_profile_dialog import EditProfileDialog
from src.gui.change_password_dialog import ChangePasswordDialog
from src.utils.dialogs import info


class ProfileWindow(QWidget):
    """
    Окно личного кабинета пользователя.
    Отображает информацию и предоставляет кнопки для редактирования.
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

        # === Блок отображения информации о пользователе ===
        info_frame = QFrame()
        info_frame.setObjectName("profileInfo")
        info_frame.setStyleSheet("""
            QFrame#profileInfo {
                background-color: #2a2a3e;
                border: 1px solid #3a3a52;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)

        # Логин
        info_layout.addWidget(self._make_info_row("Логин:", self.user_data.get('username', 'N/A')))

        # Роль
        info_layout.addWidget(self._make_info_row("Роль:", self.user_data.get('role', 'N/A').capitalize()))

        # ФИО
        info_layout.addWidget(self._make_info_row("ФИО:", self.user_data.get('full_name', 'Не указано')))

        # Email
        info_layout.addWidget(self._make_info_row("Email:", self.user_data.get('email', 'Не указан')))

        # Статус
        info_layout.addWidget(self._make_info_row("Статус:", "Активна"))

        layout.addWidget(info_frame)

        layout.addSpacing(20)

        # === Кнопки действий ===
        btn_layout = QHBoxLayout()

        # Кнопка редактирования профиля
        self.edit_profile_btn = QPushButton("✏️ Редактировать профиль")
        self.edit_profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 12px; border-radius: 4px; font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)
        self.edit_profile_btn.clicked.connect(self.open_edit_profile)
        btn_layout.addWidget(self.edit_profile_btn)

        # Кнопка смены пароля
        self.change_password_btn = QPushButton("🔑 Сменить пароль")
        self.change_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 12px; border-radius: 4px; font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.change_password_btn.clicked.connect(self.open_change_password)
        btn_layout.addWidget(self.change_password_btn)

        layout.addLayout(btn_layout)

        layout.addStretch()
        self.setLayout(layout)

    def _make_info_row(self, label: str, value: str) -> QWidget:
        """
        Создание строки с меткой и значением.

        :param label: Название поля
        :param value: Значение поля
        :return: QWidget с горизонтальным layout
        """
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            QLabel {
                color: #a0a0b0;
                background: transparent;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
        """)
        row_layout.addWidget(label_widget)

        value_widget = QLabel(value)
        value_widget.setStyleSheet("""
            QLabel {
                color: #e6e6f0;
                background: transparent;
                font-size: 14px;
            }
        """)
        row_layout.addWidget(value_widget)
        row_layout.addStretch()

        return row

    def open_edit_profile(self):
        """Открытие диалога редактирования профиля."""
        dialog = EditProfileDialog(self, self.user_data)
        if dialog.exec():
            # Получаем обновлённые данные
            new_data = dialog.get_user_data()
            self.user_data.update(new_data)
            # Отправляем сигнал об изменении
            self.profile_updated.emit(self.user_data)
            # Обновляем отображение
            self.refresh_display()
            info(self, "Успех", "Профиль успешно обновлён.")

    def open_change_password(self):
        """Открытие диалога смены пароля."""
        dialog = ChangePasswordDialog(self)
        if dialog.exec():
            info(self, "Успех", "Пароль успешно изменён.")

    def refresh_display(self):
        """Обновление отображаемой информации."""
        # Пересоздаём информационный блок
        # В реальном приложении лучше обновлять существующие виджеты
        pass