"""
Main application window with sidebar navigation.

Author: Golub Daniil Nikolaevich
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle(f"Network Auditor - {user_data.get('role', 'User').capitalize()}")
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar setup
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # User info label
        user_label = QLabel(f"User: {self.user_data.get('username')}")
        user_label.setStyleSheet("font-weight: bold; margin-bottom: 20px;")
        sidebar_layout.addWidget(user_label)

        # Navigation buttons
        self.btn_dashboard = self.create_nav_button("Dashboard")
        self.btn_scan = self.create_nav_button("New Scan")
        self.btn_results = self.create_nav_button("Results")
        self.btn_reports = self.create_nav_button("Reports")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_scan)
        sidebar_layout.addWidget(self.btn_results)
        sidebar_layout.addWidget(self.btn_reports)

        # Admin-only settings button
        if self.user_data.get('role') == 'admin':
            self.btn_settings = self.create_nav_button("Settings")
            sidebar_layout.addWidget(self.btn_settings)

        sidebar_layout.addStretch()

        # Logout button
        self.btn_logout = self.create_nav_button("Logout")
        sidebar_layout.addWidget(self.btn_logout)

        # Content area (Stacked Widget)
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: #ecf0f1;")

        # Placeholder pages
        self.content_area.addWidget(self.create_placeholder("Dashboard View"))
        self.content_area.addWidget(self.create_placeholder("New Scan View"))
        self.content_area.addWidget(self.create_placeholder("Scan Results View"))
        self.content_area.addWidget(self.create_placeholder("Reports View"))
        if self.user_data.get('role') == 'admin':
            self.content_area.addWidget(self.create_placeholder("Admin Settings View"))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)
        central_widget.setLayout(main_layout)

        # Connect buttons to stack widget
        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.btn_scan.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.btn_results.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
        self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        if self.user_data.get('role') == 'admin':
            self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(4))

    def create_nav_button(self, text: str) -> QPushButton:
        # Helper to create styled sidebar buttons
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        return btn

    def create_placeholder(self, text: str) -> QWidget:
        # Helper to create temporary placeholder views
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #7f8c8d;")
        layout.addWidget(label)
        return widget