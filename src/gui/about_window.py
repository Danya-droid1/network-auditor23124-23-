# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Network Auditor")
        self.resize(450, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Network Auditor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        version = QLabel("Version 1.0")
        version.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        layout.addSpacing(20)

        desc = QLabel("Desktop application for auditing open network ports\nand identifying vulnerabilities in local networks.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 12px;")
        layout.addWidget(desc)

        layout.addSpacing(20)

        author = QLabel("Author: Golub Daniil Nikolaevich")
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(author)

        group = QLabel("Group: PI-21-1")
        group.setAlignment(Qt.AlignCenter)
        layout.addWidget(group)

        thesis = QLabel("Thesis: Development of client-server desktop application\nfor auditing open network ports")
        thesis.setAlignment(Qt.AlignCenter)
        thesis.setStyleSheet("font-size: 11px; font-style: italic;")
        layout.addWidget(thesis)

        layout.addSpacing(20)

        university = QLabel("CHOU VO 'Moscow University named after S.Yu. Witte'\nDepartment of Information Systems")
        university.setAlignment(Qt.AlignCenter)
        university.setStyleSheet("font-size: 11px; color: #7f8c8d;")
        layout.addWidget(university)

        year = QLabel("2026")
        year.setAlignment(Qt.AlignCenter)
        layout.addWidget(year)

        self.setLayout(layout)