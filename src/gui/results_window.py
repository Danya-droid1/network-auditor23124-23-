"""
Window displaying scan results in a tabular format with export options.

Author: Golub Daniil Nikolaevich
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton, QHeaderView)
from PySide6.QtCore import Qt


class ResultsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel("Scan Results")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header_label)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["IP Address", "Port", "Service", "Risk Level", "Timestamp"])

        # Stretch the last column
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Export buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_export_docx = QPushButton("Export to DOCX")
        self.btn_export_xlsx = QPushButton("Export to XLSX")

        self.btn_export_docx.setStyleSheet("background-color: #2980b9; color: white; padding: 8px;")
        self.btn_export_xlsx.setStyleSheet("background-color: #27ae60; color: white; padding:  a8px;")

        btn_layout.addWidget(self.btn_export_docx)
        btn_layout.addWidget(self.btn_export_xlsx)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Load dummy data for demonstration
        self.load_dummy_data()

    def load_dummy_data(self):
        # Populate table with sample data
        sample_data = [
            ("192.168.1.10", "22", "SSH", "Medium", "2026-11-19 10:00:00"),
            ("192.168.1.10", "80", "HTTP", "Low", "2026-11-19 10:00:01"),
            ("192.168.1.15", "445", "SMB", "High", "2026-11-19 10:00:05"),
        ]

        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                # Color-code risk levels
                if col == 3:
                    if value == "High":
                        item.setBackground(Qt.red)
                        item.setForeground(Qt.white)
                    elif value == "Medium":
                        item.setBackground(Qt.yellow)

                self.table.setItem(row, col, item)