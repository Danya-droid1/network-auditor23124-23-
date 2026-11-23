# -*- coding: utf-8 -*-
"""
Главное окно приложения с боковым меню.
Реализует навигацию между разделами с учётом роли пользователя и прав доступа.
Интегрирует реальное сканирование сети через ScanWorker с поддержкой CIDR.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt

from src.gui.dashboard_window import DashboardWindow
from src.gui.scan_dialog import ScanDialog
from src.gui.scan_progress_window import ScanProgressWindow
from src.gui.results_window import ResultsWindow
from src.gui.reports_window import ReportsWindow
from src.gui.settings_window import SettingsWindow
from src.gui.profile_window import ProfileWindow
from src.gui.about_window import AboutWindow
from src.gui.vulnerability_db_window import VulnerabilityDBWindow
from src.gui.assets_window import AssetsWindow
from src.gui.users_window import UsersWindow, ROLE_PERMISSIONS

from src.core.scan_worker import ScanWorker
from src.utils.dialogs import info, warning, critical, question


class MainWindow(QMainWindow):
    """
    Главное окно приложения Network Auditor.
    Содержит боковое меню навигации и область контента.
    """

    def __init__(self, user_data: dict):
        """
        Инициализация главного окна.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        super().__init__()
        self.user_data = user_data
        self.scan_worker = None
        self.last_scan_results = []

        # Получаем права доступа для текущей роли
        self.permissions = ROLE_PERMISSIONS.get(user_data.get('role', 'user'), {})

        self.setWindowTitle(f"Network Auditor — {user_data.get('role', 'User').capitalize()}")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Боковое меню ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #181825;
                border-right: 1px solid #2a2a3e;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Метка с именем пользователя
        self.user_label = QLabel(f"👤 {self.user_data.get('username')}")
        self.user_label.setStyleSheet(
            "font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #4a9eff; background: transparent;")
        sidebar_layout.addWidget(self.user_label)

        # Метка с ФИО
        self.fullname_label = QLabel(self.user_data.get('full_name', ''))
        self.fullname_label.setStyleSheet(
            "font-size: 12px; color: #a0a0b0; background: transparent; margin-bottom: 20px;")
        sidebar_layout.addWidget(self.fullname_label)

        # Кнопки навигации с учётом прав доступа
        self.btn_dashboard = self.create_nav_button("📊 Дашборд")
        sidebar_layout.addWidget(self.btn_dashboard)

        if self.permissions.get('scan', False):
            self.btn_scan = self.create_nav_button("🔍 Новое сканирование")
            sidebar_layout.addWidget(self.btn_scan)

        if self.permissions.get('results', False):
            self.btn_results = self.create_nav_button("📋 Результаты")
            sidebar_layout.addWidget(self.btn_results)

        if self.permissions.get('assets', False):
            self.btn_assets = self.create_nav_button("💻 Активы")
            sidebar_layout.addWidget(self.btn_assets)

        if self.permissions.get('reports', False):
            self.btn_reports = self.create_nav_button("📄 Отчёты")
            sidebar_layout.addWidget(self.btn_reports)

        if self.permissions.get('vulnerabilities', False):
            self.btn_vulnerabilities = self.create_nav_button("🛡️ Уязвимости")
            sidebar_layout.addWidget(self.btn_vulnerabilities)

        if self.permissions.get('settings', False):
            self.btn_settings = self.create_nav_button("⚙️ Настройки")
            sidebar_layout.addWidget(self.btn_settings)

        if self.permissions.get('users', False):
            self.btn_users = self.create_nav_button("👥 Пользователи")
            sidebar_layout.addWidget(self.btn_users)

        sidebar_layout.addStretch()

        # Нижние кнопки (всегда доступны)
        self.btn_profile = self.create_nav_button("👤 Личный кабинет")
        self.btn_about = self.create_nav_button("ℹ️ О программе")
        self.btn_logout = self.create_nav_button("🚪 Выход")

        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_about)
        sidebar_layout.addWidget(self.btn_logout)

        # === Область контента ===
        self.content_area = QStackedWidget()

        # Индексация окон
        idx = 0
        self.dashboard = DashboardWindow(self.user_data)
        self.content_area.addWidget(self.dashboard)
        dashboard_idx = idx
        idx += 1

        if self.permissions.get('scan', False):
            self.results = ResultsWindow()
            self.content_area.addWidget(self.results)
            results_idx = idx
            idx += 1

        if self.permissions.get('assets', False):
            self.assets = AssetsWindow()
            self.content_area.addWidget(self.assets)
            assets_idx = idx
            idx += 1

        if self.permissions.get('reports', False):
            self.reports = ReportsWindow()
            self.content_area.addWidget(self.reports)
            reports_idx = idx
            idx += 1

        if self.permissions.get('vulnerabilities', False):
            self.vulnerabilities = VulnerabilityDBWindow()
            self.content_area.addWidget(self.vulnerabilities)
            vuln_idx = idx
            idx += 1

        if self.permissions.get('settings', False):
            self.settings = SettingsWindow()
            self.content_area.addWidget(self.settings)
            settings_idx = idx
            idx += 1

        if self.permissions.get('users', False):
            self.users = UsersWindow()
            self.content_area.addWidget(self.users)
            users_idx = idx
            idx += 1

        self.profile = ProfileWindow(self.user_data)
        self.content_area.addWidget(self.profile)
        profile_idx = idx
        idx += 1

        self.about = AboutWindow()
        self.content_area.addWidget(self.about)
        about_idx = idx

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)
        central_widget.setLayout(main_layout)

        # === Подключение обработчиков ===
        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(dashboard_idx))

        if self.permissions.get('scan', False):
            self.btn_scan.clicked.connect(self.start_scan)
            self.btn_results.clicked.connect(lambda: self.content_area.setCurrentIndex(results_idx))

        if self.permissions.get('assets', False):
            self.btn_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(assets_idx))

        if self.permissions.get('reports', False):
            self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(reports_idx))

        if self.permissions.get('vulnerabilities', False):
            self.btn_vulnerabilities.clicked.connect(lambda: self.content_area.setCurrentIndex(vuln_idx))

        if self.permissions.get('settings', False):
            self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(settings_idx))

        if self.permissions.get('users', False):
            self.btn_users.clicked.connect(lambda: self.content_area.setCurrentIndex(users_idx))

        self.btn_profile.clicked.connect(lambda: self.content_area.setCurrentIndex(profile_idx))
        self.btn_about.clicked.connect(lambda: self.content_area.setCurrentIndex(about_idx))
        self.btn_logout.clicked.connect(self.logout)

        # Подключаем кнопки на дашборде
        self.dashboard.btn_new_scan.clicked.connect(self.start_scan)

        if self.permissions.get('reports', False):
            self.dashboard.btn_view_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(reports_idx))

        if self.permissions.get('assets', False):
            self.dashboard.btn_manage_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(assets_idx))

        # Устанавливаем контекст для окна результатов
        if self.permissions.get('results', False):
            self.results.set_context(self.user_data.get('username', 'unknown'),
                                     self.reports if self.permissions.get('reports', False) else None)

        # Подключаем сигнал изменения профиля
        self.profile.profile_updated.connect(self.on_profile_updated)

    def on_profile_updated(self, new_user_data: dict):
        """
        Обработчик сигнала об изменении данных профиля.
        """
        self.user_data = new_user_data
        self.fullname_label.setText(new_user_data.get('full_name', ''))
        self.setWindowTitle(f"Network Auditor — {new_user_data.get('role', 'User').capitalize()}")

    def create_nav_button(self, text: str) -> QPushButton:
        """Создание стилизованной кнопки навигации."""
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e6e6f0;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2a2a3e;
            }
            QPushButton:pressed {
                background-color: #3a3a52;
            }
        """)
        return btn

    def start_scan(self):
        """Запуск процесса сканирования сети."""
        dialog = ScanDialog(self)
        if not dialog.exec():
            return

        params = dialog.get_scan_params()
        ip_range = params.get('ip_range', '')
        timeout = params.get('timeout', 1)
        ports = params.get('ports')

        if not ports:
            port_profile = params.get('port_profile', '')
            if "Стандартные" in port_profile:
                ports = [21, 22, 23, 80, 443, 445, 3389]
            elif "Все" in port_profile:
                ports = list(range(1, 1025))
            else:
                ports = [21, 22, 23, 80, 443, 445, 3389]

        if not ports:
            warning(self, "Ошибка", "Не удалось определить список портов.")
            return

        try:
            import ipaddress
            network = ipaddress.ip_network(ip_range, strict=False)
            total_hosts = max(1, network.num_addresses - 2)
        except ValueError:
            total_hosts = 0

        self.progress_window = ScanProgressWindow(total_hosts=total_hosts)
        self.progress_window.show()

        self.scan_worker = ScanWorker(ip_range, ports, timeout)
        self.scan_worker.progress.connect(self.progress_window.update_progress)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)
        self.progress_window.cancel_btn.clicked.connect(self.scan_worker.stop)
        self.scan_worker.start()

    def on_scan_finished(self, results: list):
        """Обработчик завершения сканирования."""
        if hasattr(self, 'progress_window'):
            self.progress_window.close()

        self.last_scan_results = results

        if self.permissions.get('results', False):
            self.results.load_real_data(results)

        if self.permissions.get('assets', False):
            new_assets_count = self.assets.add_from_scan_results(results)

        self.dashboard.update_statistics(results)

        if self.permissions.get('results', False):
            self.content_area.setCurrentIndex(1)

        info(
            self,
            "Сканирование завершено",
            f"Сканирование успешно завершено.\n\n"
            f"Найдено открытых портов: {len(results)}"
        )

    def on_scan_error(self, error_msg: str):
        """Обработчик ошибки сканирования."""
        if hasattr(self, 'progress_window'):
            self.progress_window.close()
        critical(self, "Ошибка сканирования", error_msg)

    def logout(self):
        """Выход из системы."""
        if question(self, "Выход", "Вы уверены, что хотите выйти?"):
            from src.gui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()