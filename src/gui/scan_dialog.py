"""
Dialog window for configuring and starting a network scan.

Author: Golub Daniil Nikolaevich
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QMessageBox, QSpinBox)


class ScanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Network Scan")
        self.resize(400, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # IP Range input
        layout.addWidget(QLabel("Target IP Range (e.g., 192.168.1.0/24):"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.0/24")
        layout.addWidget(self.ip_input)

        # Port selection - ИСПРАВЛЕНО: добавлена закрывающая скобка
        layout.addWidget(QLabel("Port Selection:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems(["Standard Ports (21, 22, 80, 443, 445, 3389)", "All Common Ports (1-1024)", "Custom"])
        layout.addWidget(self.port_combo)

        # Timeout input
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout (seconds):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)

        layout.addStretch()

        # Action buttons
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start Scan")
        self.btn_start.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        self.btn_cancel = QPushButton("Cancel")

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connections
        self.btn_start.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_and_accept(self):
        # Basic validation before accepting the dialog
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Validation Error", "IP range cannot be empty.")
            return
        self.accept()

    def get_scan_params(self) -> dict:
        # Return configured scan parameters
        return {
            "ip_range": self.ip_input.text().strip(),
            "port_profile": self.port_combo.currentText(),
            "timeout": self.timeout_spin.value()
        }