# -*- coding: utf-8 -*-
"""
Окно управления пользователями системы.
Доступно только администратору.
Позволяет добавлять, редактировать и удалять пользователей,
а также назначать им роли и права доступа.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QDialog, QFormLayout, QLineEdit, QComboBox,
                               QHeaderView, QCheckBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.utils.dialogs import info, warning, question

# Права доступа для каждой роли
ROLE_PERMISSIONS = {
    'admin': {
        'dashboard': True,
        'scan': True,
        'results': True,
        'assets': True,
        'reports': True,
        'vulnerabilities': True,
        'settings': True,
        'users': True
    },
    'auditor': {
        'dashboard': True,
        'scan': True,
        'results': True,
        'assets': True,
        'reports': True,
        'vulnerabilities': True,
        'settings': True,
        'users': False
    },
    'user': {
        'dashboard': True,
        'scan': False,
        'results': False,
        'assets': False,
        'reports': False,
        'vulnerabilities': False,
        'settings': False,
        'users': False
    }
}


class UsersWindow(QWidget):
    """
    Окно управления пользователями системы.
    Доступно только администратору.
    """

    def __init__(self):
        """Инициализация окна управления пользователями."""
        super().__init__()
        # Список пользователей в памяти
        self.users = [
            {'username': 'admin', 'password': 'AdminSecure2026!', 'role': 'admin', 'full_name': 'Администратор ИБ',
             'email': 'admin@muiv.ru'},
            {'username': 'analyst', 'password': 'AnalystSecure2026!', 'role': 'auditor', 'full_name': 'Аналитик ИБ',
             'email': 'analyst@muiv.ru'},
            {'username': 'auditor', 'password': 'AuditorSecure2026!', 'role': 'auditor', 'full_name': 'Аудитор',
             'email': 'auditor@muiv.ru'},
            {'username': 'user', 'password': 'UserSecure2026!', 'role': 'user', 'full_name': 'Пользователь',
             'email': 'user@muiv.ru'}
        ]
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Управление пользователями")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        self.info_label = QLabel(f"Всего пользователей: {len(self.users)}")
        self.info_label.setStyleSheet("font-size: 13px; color: #a0a0b0; background: transparent;")
        layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Логин", "Роль", "ФИО", "Email", "Пароль"
        ])

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Добавить пользователя")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.add_btn.clicked.connect(self.add_user)

        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)
        self.edit_btn.clicked.connect(self.edit_user)

        self.delete_btn = QPushButton("🗑 Удалить")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #ec7063; }
        """)
        self.delete_btn.clicked.connect(self.delete_user)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы пользователей."""
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.users))

        for row, user in enumerate(self.users):
            self.table.setItem(row, 0, QTableWidgetItem(user.get('username', '')))
            self.table.setItem(row, 1, QTableWidgetItem(user.get('role', '').capitalize()))
            self.table.setItem(row, 2, QTableWidgetItem(user.get('full_name', '')))
            self.table.setItem(row, 3, QTableWidgetItem(user.get('email', '')))
            self.table.setItem(row, 4, QTableWidgetItem("••••••••"))

        self.info_label.setText(f"Всего пользователей: {len(self.users)}")

    def add_user(self):
        """Открытие диалога добавления нового пользователя."""
        dialog = AddUserDialog(self)
        if dialog.exec():
            user_data = dialog.get_user_data()

            # Проверка уникальности логина
            for existing in self.users:
                if existing.get('username') == user_data['username']:
                    warning(self, "Ошибка", f"Пользователь с логином '{user_data['username']}' уже существует.")
                    return

            self.users.append(user_data)
            self.refresh_table()
            info(self, "Успех", f"Пользователь '{user_data['username']}' успешно добавлен.")

    def edit_user(self):
        """Редактирование выбранного пользователя."""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Ошибка", "Пожалуйста, выберите пользователя для редактирования.")
            return

        row = selected_rows[0].row()
        user = self.users[row]

        dialog = AddUserDialog(self, edit_mode=True, user_data=user)
        if dialog.exec():
            updated_data = dialog.get_user_data()
            self.users[row] = updated_data
            self.refresh_table()
            info(self, "Успех", "Пользователь успешно обновлён.")

    def delete_user(self):
        """Удаление выбранного пользователя."""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Ошибка", "Пожалуйста, выберите пользователя для удаления.")
            return

        row = selected_rows[0].row()
        user = self.users[row]

        # Защита от удаления admin
        if user.get('username') == 'admin':
            warning(self, "Ошибка", "Нельзя удалить пользователя 'admin'.")
            return

        if question(self, "Подтверждение удаления",
                    f"Вы уверены, что хотите удалить пользователя?\n\n"
                    f"Логин: {user.get('username')}\n"
                    f"ФИО: {user.get('full_name')}\n\n"
                    f"Это действие нельзя отменить."):
            self.users.pop(row)
            self.refresh_table()
            info(self, "Успех", "Пользователь удалён.")


class AddUserDialog(QDialog):
    """
    Диалог добавления/редактирования пользователя.
    """

    def __init__(self, parent=None, edit_mode: bool = False, user_data: dict = None):
        """
        Инициализация диалога.

        :param parent: Родительское окно
        :param edit_mode: Режим редактирования
        :param user_data: Данные пользователя для редактирования
        """
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.user_data = user_data or {}

        if edit_mode:
            self.setWindowTitle("Редактирование пользователя")
        else:
            self.setWindowTitle("Добавление пользователя")

        self.resize(500, 400)
        self.init_ui()

    def init_ui(self):
        """Инициализация формы диалога."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Редактирование пользователя" if self.edit_mode else "Добавление нового пользователя")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(title)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        if self.edit_mode:
            self.username_input.setText(self.user_data.get('username', ''))
            self.username_input.setReadOnly(True)
        else:
            self.username_input.setPlaceholderText("login")
        form_layout.addRow("Логин:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Минимум 8 символов")
        form_layout.addRow("Пароль:", self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "auditor", "user"])
        if self.edit_mode:
            role = self.user_data.get('role', 'user')
            index = self.role_combo.findText(role)
            if index >= 0:
                self.role_combo.setCurrentIndex(index)
        form_layout.addRow("Роль:", self.role_combo)

        self.fullname_input = QLineEdit()
        if self.edit_mode:
            self.fullname_input.setText(self.user_data.get('full_name', ''))
        form_layout.addRow("ФИО:", self.fullname_input)

        self.email_input = QLineEdit()
        if self.edit_mode:
            self.email_input.setText(self.user_data.get('email', ''))
        form_layout.addRow("Email:", self.email_input)

        layout.addLayout(form_layout)

        # Описание прав доступа
        perms_group = QGroupBox("Права доступа для выбранной роли:")
        perms_layout = QVBoxLayout()
        self.perms_label = QLabel()
        self.perms_label.setStyleSheet("color: #a0a0b0; background: transparent;")
        perms_layout.addWidget(self.perms_label)
        perms_group.setLayout(perms_layout)
        layout.addWidget(perms_group)

        self.role_combo.currentTextChanged.connect(self.update_permissions_display)
        self.update_permissions_display()

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        save_btn.clicked.connect(self.validate_and_accept)

        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_permissions_display(self):
        """Обновление отображения прав доступа для выбранной роли."""
        role = self.role_combo.currentText()
        perms = ROLE_PERMISSIONS.get(role, {})

        perm_names = {
            'dashboard': 'Дашборд',
            'scan': 'Новое сканирование',
            'results': 'Результаты',
            'assets': 'Активы',
            'reports': 'Отчёты',
            'vulnerabilities': 'Уязвимости',
            'settings': 'Настройки',
            'users': 'Управление пользователями'
        }

        text = "Доступные вкладки:\n"
        for perm_key, perm_name in perm_names.items():
            if perms.get(perm_key, False):
                text += f"✓ {perm_name}\n"
            else:
                text += f"✗ {perm_name}\n"

        self.perms_label.setText(text)

    def validate_and_accept(self):
        """Валидация данных перед сохранением."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        fullname = self.fullname_input.text().strip()

        if not username:
            warning(self, "Ошибка", "Логин не может быть пустым.")
            return

        if not self.edit_mode and not password:
            warning(self, "Ошибка", "Пароль не может быть пустым.")
            return

        if not self.edit_mode and len(password) < 8:
            warning(self, "Ошибка", "Пароль должен содержать минимум 8 символов.")
            return

        if not fullname:
            warning(self, "Ошибка", "ФИО не может быть пустым.")
            return

        self.accept()

    def get_user_data(self) -> dict:
        """Получение данных пользователя."""
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text() if self.password_input.text() else self.user_data.get('password',
                                                                                                         ''),
            'role': self.role_combo.currentText(),
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip()
        }