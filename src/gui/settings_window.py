# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QCheckBox, QSpinBox,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("System Settings")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        layout.addWidget(QLabel("1. Scan Timeout (seconds):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        layout.addWidget(self.timeout_spin)

        self.auto_scan_check = QCheckBox("2. Enable automatic scan by schedule")
        layout.addWidget(self.auto_scan_check)

        layout.addWidget(QLabel("3. Auto-scan period (days):"))
        self.period_spin = QSpinBox()
        self.period_spin.setRange(1, 30)
        self.period_spin.setValue(7)
        layout.addWidget(self.period_spin)

        self.notifications_check = QCheckBox("4. Enable notifications for critical vulnerabilities")
        self.notifications_check.setChecked(True)
        layout.addWidget(self.notifications_check)

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("5. Reports save path:"))
        self.path_input = QLineEdit("C:/NetworkAuditor/Reports")
        path_layout.addWidget(self.path_input)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        layout.addStretch()

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Reports Folder")
        if folder:
            self.path_input.setText(folder)

    def save_settings(self):
        QMessageBox.information(self, "Success", "Settings saved successfully")