# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QMessageBox, QFrame)
from PySide6.QtCore import Qt


class ProfileWindow(QWidget):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Personal Cabinet")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #ecf0f1; padding: 15px; border-radius: 5px;")
        info_layout = QVBoxLayout(info_frame)

        info_layout.addWidget(QLabel(f"Username: {self.user_data.get('username')}"))
        info_layout.addWidget(QLabel(f"Full Name: {self.user_data.get('full_name', 'N/A')}"))
        info_layout.addWidget(QLabel(f"Role: {self.user_data.get('role', 'N/A').capitalize()}"))
        info_layout.addWidget(QLabel("Account Status: Active"))
        info_layout.addWidget(QLabel("Last Login: Today"))

        layout.addWidget(info_frame)

        layout.addSpacing(20)

        layout.addWidget(QLabel("Change Password:"))
        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        self.old_password.setPlaceholderText("Current password")
        layout.addWidget(self.old_password)

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("New password")
        layout.addWidget(self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        layout.addWidget(self.confirm_password)

        self.change_pwd_btn = QPushButton("Change Password")
        self.change_pwd_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        self.change_pwd_btn.clicked.connect(self.change_password)
        layout.addWidget(self.change_pwd_btn)

        layout.addStretch()
        self.setLayout(layout)

    def change_password(self):
        new_pwd = self.new_password.text()
        confirm = self.confirm_password.text()

        if not new_pwd or not confirm:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        if new_pwd != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        QMessageBox.information(self, "Success", "Password changed successfully")