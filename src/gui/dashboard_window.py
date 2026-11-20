# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QGridLayout)
from PySide6.QtCore import Qt


class DashboardWindow(QWidget):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)

        welcome = QLabel(f"Welcome, {self.user_data.get('full_name', 'User')}!")
        welcome.setStyleSheet("font-size: 16px; color: #7f8c8d; margin-bottom: 20px;")
        layout.addWidget(welcome)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        stats_grid.addWidget(self.create_stat_card("Total Scans", "12", "#3498db"), 0, 0)
        stats_grid.addWidget(self.create_stat_card("Open Ports", "47", "#e74c3c"), 0, 1)
        stats_grid.addWidget(self.create_stat_card("High Risk", "8", "#e67e22"), 1, 0)
        stats_grid.addWidget(self.create_stat_card("Assets", "156", "#27ae60"), 1, 1)

        layout.addLayout(stats_grid)

        layout.addSpacing(30)

        quick_actions = QLabel("Quick Actions")
        quick_actions.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(quick_actions)

        actions_layout = QHBoxLayout()

        self.btn_new_scan = QPushButton("Start New Scan")
        self.btn_new_scan.setStyleSheet("background-color: #27ae60; color: white; padding: 12px; font-size: 14px;")

        self.btn_view_reports = QPushButton("View Reports")
        self.btn_view_reports.setStyleSheet("background-color: #3498db; color: white; padding: 12px; font-size: 14px;")

        self.btn_manage_assets = QPushButton("Manage Assets")
        self.btn_manage_assets.setStyleSheet("background-color: #9b59b6; color: white; padding: 12px; font-size: 14px;")

        actions_layout.addWidget(self.btn_new_scan)
        actions_layout.addWidget(self.btn_view_reports)
        actions_layout.addWidget(self.btn_manage_assets)

        layout.addLayout(actions_layout)

        layout.addStretch()
        self.setLayout(layout)

    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        card.setFixedHeight(120)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        value_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: white;")
        title_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        return card