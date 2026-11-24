# -*- coding: utf-8 -*-
# Окно управления пользователями системы.
# Доступно только администратору.
# Все CRUD-операции выполняются через UserManager в PostgreSQL.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QDialog, QFormLayout, QLineEdit, QComboBox,
                               QHeaderView)
from PySide6.QtCore import Qt

from src.utils.dialogs import info, warning, question


class UsersWindow(QWidget):
    """Окно управления пользователями системы."""

    def __init__(self, user_manager):
        """
        Инициализация окна управления пользователями.

        :param user_manager: Экземпляр UserManager
        """
        super().__init__()
        self.user_manager = user_manager
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Управление пользователями")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        self.info_label = QLabel("Загрузка...")
        self.info_label.setStyleSheet("font-size: 13px; color: #a0a0b0; background: transparent;")
        layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Логин", "Роль", "ФИО", "Email", "Последний вход", "Статус"
        ])

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Добавить пользователя")
        self.add_btn.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.add_btn.clicked.connect(self.add_user)

        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #5dade2; }
        """)
        self.edit_btn.clicked.connect(self.edit_user)

        self.delete_btn = QPushButton("🗑 Удалить")
        self.delete_btn.setStyleSheet("""
            QPushButton { background-color: #e74c3c; color: white; padding: 8px; border-radius: 4px; }
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
        """Обновление таблицы пользователей из БД."""
        users = self.user_manager.get_all_users()

        self.table.setRowCount(0)
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.get('username', '')))
            self.table.setItem(row, 1, QTableWidgetItem(user.get('role', '').capitalize()))
            self.table.setItem(row, 2, QTableWidgetItem(user.get('full_name', '')))
            self.table.setItem(row, 3, QTableWidgetItem(user.get('email', '')))

            last_login = user.get('last_login')
            if last_login:
                self.table.setItem(row, 4, QTableWidgetItem(str(last_login)[:19]))
            else:
                self.table.setItem(row, 4, QTableWidgetItem("Никогда"))

            status = "Активен" if user.get('is_active') else "Заблокирован"
            self.table.setItem(row, 5, QTableWidgetItem(status))

        self.info_label.setText(f"Всего пользователей: {len(users)}")

    def add_user(self):
        """Открытие диалога добавления нового пользователя."""
        roles = self.user_manager.get_roles()
        dialog = AddUserDialog(self, roles=roles)
        if dialog.exec():
            user_data = dialog.get_user_data()
            success = self.user_manager.add_user(
                user_data['username'],
                user_data['password'],
                user_data['role'],
                user_data['full_name'],
                user_data['email']
            )
            if success:
                self.refresh_table()
                info(self, "Успех", f"Пользователь '{user_data['username']}' успешно добавлен в БД.")
            else:
                warning(self, "Ошибка", f"Пользователь с логином '{user_data['username']}' уже существует.")

    def edit_user(self):
        """Редактирование выбранного пользователя."""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Ошибка", "Пожалуйста, выберите пользователя для редактирования.")
            return

        row = selected_rows[0].row()
        username = self.table.item(row, 0).text()

        # Получаем полные данные из БД
        users = self.user_manager.get_all_users()
        user = next((u for u in users if u['username'] == username), None)

        if not user:
            warning(self, "Ошибка", "Не удалось найти пользователя.")
            return

        roles = self.user_manager.get_roles()
        dialog = AddUserDialog(self, edit_mode=True, user_data=user, roles=roles)
        if dialog.exec():
            updated = dialog.get_user_data()
            success = self.user_manager.update_user(
                user['id'],
                role_name=updated['role'],
                full_name=updated['full_name'],
                email=updated['email'],
                password=updated.get('password') if updated.get('password') else None
            )
            if success:
                self.refresh_table()
                info(self, "Успех", "Пользователь успешно обновлён в БД.")
            else:
                warning(self, "Ошибка", "Не удалось обновить пользователя.")

    def delete_user(self):
        """Удаление выбранного пользователя."""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Ошибка", "Пожалуйста, выберите пользователя для удаления.")
            return

        row = selected_rows[0].row()
        username = self.table.item(row, 0).text()

        users = self.user_manager.get_all_users()
        user = next((u for u in users if u['username'] == username), None)

        if not user:
            return

        if username == 'admin':
            warning(self, "Ошибка", "Нельзя удалить пользователя 'admin'.")
            return

        if question(self, "Подтверждение удаления",
                    f"Вы уверены, что хотите удалить пользователя?\n\n"
                    f"Логин: {username}\n"
                    f"ФИО: {user.get('full_name')}\n\n"
                    f"Это действие нельзя отменить."):
            success = self.user_manager.delete_user(user['id'])
            if success:
                self.refresh_table()
                info(self, "Успех", "Пользователь удалён из БД.")
            else:
                warning(self, "Ошибка", "Не удалось удалить пользователя.")


class AddUserDialog(QDialog):
    """Диалог добавления/редактирования пользователя."""

    def __init__(self, parent=None, edit_mode: bool = False, user_data: dict = None, roles: list = None):
        """
        Инициализация диалога.

        :param roles: Список ролей из БД
        """
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.user_data = user_data or {}
        self.roles = roles or []

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
        self.password_input.setPlaceholderText(
            "Минимум 8 символов" if not self.edit_mode else "Оставьте пустым, чтобы не менять")
        form_layout.addRow("Пароль:", self.password_input)

        self.role_combo = QComboBox()
        for role in self.roles:
            self.role_combo.addItem(role['name'])
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

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        save_btn.clicked.connect(self.validate_and_accept)

        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton { background-color: #7f8c8d; color: white; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

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
            'password': self.password_input.text(),
            'role': self.role_combo.currentText(),
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip()
        }