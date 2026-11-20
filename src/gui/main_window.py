# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QPushButton, QStackedWidget, QLabel, QFrame, QMessageBox)
from PySide6.QtCore import Qt

from src.gui.dashboard_window import DashboardWindow
from src.gui.scan_dialog import ScanDialog
from src.gui.results_window import ResultsWindow
from src.gui.reports_window import ReportsWindow
from src.gui.settings_window import SettingsWindow
from src.gui.profile_window import ProfileWindow
from src.gui.about_window import AboutWindow
from src.gui.vulnerability_db_window import VulnerabilityDBWindow
from src.gui.assets_window import AssetsWindow


class MainWindow(QMainWindow):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle(f"Network Auditor - {user_data.get('role', 'User').capitalize()}")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        user_label = QLabel(f"User: {self.user_data.get('username')}")
        user_label.setStyleSheet("font-weight: bold; margin-bottom: 20px; font-size: 14px;")
        sidebar_layout.addWidget(user_label)

        self.btn_dashboard = self.create_nav_button("📊 Dashboard")
        self.btn_scan = self.create_nav_button("🔍 New Scan")
        self.btn_results = self.create_nav_button("📋 Results")
        self.btn_reports = self.create_nav_button("📄 Reports")
        self.btn_assets = self.create_nav_button("💻 Assets")
        
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_scan)
        sidebar_layout.addWidget(self.btn_results)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addWidget(self.btn_assets)

        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities = self.create_nav_button("🛡️ Vulnerabilities")
            self.btn_settings = self.create_nav_button("⚙️ Settings")
            sidebar_layout.addWidget(self.btn_vulnerabilities)
            sidebar_layout.addWidget(self.btn_settings)

        sidebar_layout.addStretch()

        self.btn_profile = self.create_nav_button("👤 Profile")
        self.btn_about = self.create_nav_button("ℹ️ About")
        self.btn_logout = self.create_nav_button("🚪 Logout")
        
        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_about)
        sidebar_layout.addWidget(self.btn_logout)

        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: #ecf0f1;")
        
        self.dashboard = DashboardWindow(self.user_data)
        self.results = ResultsWindow()
        self.reports = ReportsWindow()
        self.assets = AssetsWindow()
        self.profile = ProfileWindow(self.user_data)
        self.about = AboutWindow()
        
        self.content_area.addWidget(self.dashboard)
        self.content_area.addWidget(self.results)
        self.content_area.addWidget(self.reports)
        self.content_area.addWidget(self.assets)
        self.content_area.addWidget(self.profile)
        self.content_area.addWidget(self.about)
        
        if self.user_data.get('role') == 'admin':
            self.vulnerabilities = VulnerabilityDBWindow()
            self.settings = SettingsWindow()
            self.content_area.addWidget(self.vulnerabilities)
            self.content_area.addWidget(self.settings)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)
        central_widget.setLayout(main_layout)

        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.btn_scan.clicked.connect(self.start_scan)
        self.btn_results.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
        self.btn_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        self.btn_profile.clicked.connect(lambda: self.content_area.setCurrentIndex(4))
        self.btn_about.clicked.connect(lambda: self.content_area.setCurrentIndex(5))
        
        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities.clicked.connect(lambda: self.content_area.setCurrentIndex(6))
            self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(7))
        
        self.btn_logout.clicked.connect(self.logout)

    def create_nav_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        return btn

    def start_scan(self):
        dialog = ScanDialog(self)
        if dialog.exec():
            params = dialog.get_scan_params()
            QMessageBox.information(self, "Scan Started", 
                                  f"Scan initiated for range: {params['ip_range']}")
            self.content_area.setCurrentIndex(1)

    def logout(self):
        reply = QMessageBox.question(self, "Logout", 
                                    "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            from src.gui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()