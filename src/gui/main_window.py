# -*- coding: utf-8 -*-
"""
Главное окно приложения с боковым меню.
Реализует навигацию между разделами с учётом роли пользователя.
Интегрирует реальное сканирование сети через ScanWorker.
Обновлено: подключён сигнал profile_updated для обновления UI при изменении профиля.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt

# Импорт всех окон приложения
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

# Импорт рабочего потока для сканирования
from src.core.scan_worker import ScanWorker
# Импорт обёртки диалогов с русскими кнопками
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

        self.btn_dashboard = self.create_nav_button("📊 Дашборд")
        self.btn_scan = self.create_nav_button("🔍 Новое сканирование")
        self.btn_results = self.create_nav_button("📋 Результаты")
        self.btn_assets = self.create_nav_button("💻 Активы")
        self.btn_reports = self.create_nav_button("📄 Отчёты")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_scan)
        sidebar_layout.addWidget(self.btn_results)
        sidebar_layout.addWidget(self.btn_assets)
        sidebar_layout.addWidget(self.btn_reports)

        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities = self.create_nav_button("🛡️ Уязвимости")
            self.btn_settings = self.create_nav_button("⚙️ Настройки")
            sidebar_layout.addWidget(self.btn_vulnerabilities)
            sidebar_layout.addWidget(self.btn_settings)

        sidebar_layout.addStretch()

        self.btn_profile = self.create_nav_button("👤 Профиль")
        self.btn_about = self.create_nav_button("ℹ️ О программе")
        self.btn_logout = self.create_nav_button("🚪 Выход")

        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_about)
        sidebar_layout.addWidget(self.btn_logout)

        # === Область контента ===
        self.content_area = QStackedWidget()

        self.dashboard = DashboardWindow(self.user_data)
        self.results = ResultsWindow()
        self.assets = AssetsWindow()
        self.reports = ReportsWindow()
        self.profile = ProfileWindow(self.user_data)
        self.about = AboutWindow()

        self.content_area.addWidget(self.dashboard)  # 0
        self.content_area.addWidget(self.results)  # 1
        self.content_area.addWidget(self.assets)  # 2
        self.content_area.addWidget(self.reports)  # 3
        self.content_area.addWidget(self.profile)  # 4
        self.content_area.addWidget(self.about)  # 5

        if self.user_data.get('role') == 'admin':
            self.vulnerabilities = VulnerabilityDBWindow()  # 6
            self.settings = SettingsWindow()  # 7
            self.content_area.addWidget(self.vulnerabilities)
            self.content_area.addWidget(self.settings)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)
        central_widget.setLayout(main_layout)

        # === Подключение обработчиков ===
        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.btn_scan.clicked.connect(self.start_scan)
        self.btn_results.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.btn_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
        self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        self.btn_profile.clicked.connect(lambda: self.content_area.setCurrentIndex(4))
        self.btn_about.clicked.connect(lambda: self.content_area.setCurrentIndex(5))

        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities.clicked.connect(lambda: self.content_area.setCurrentIndex(6))
            self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(7))

        self.btn_logout.clicked.connect(self.logout)

        # Подключаем кнопки на дашборде
        self.dashboard.btn_new_scan.clicked.connect(self.start_scan)
        self.dashboard.btn_view_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        self.dashboard.btn_manage_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(2))

        # Устанавливаем контекст для окна результатов
        self.results.set_context(self.user_data.get('username', 'unknown'), self.reports)

        # === Подключаем сигнал изменения профиля ===
        self.profile.profile_updated.connect(self.on_profile_updated)

    def on_profile_updated(self, new_user_data: dict):
        """
        Обработчик сигнала об изменении данных профиля.
        Обновляет метки в боковом меню и заголовок окна.

        :param new_user_data: Обновлённые данные пользователя
        """
        self.user_data = new_user_data

        # Обновляем метку ФИО в боковом меню
        self.fullname_label.setText(new_user_data.get('full_name', ''))

        # Обновляем заголовок окна
        self.setWindowTitle(f"Network Auditor — {new_user_data.get('role', 'User').capitalize()}")

    def create_nav_button(self, text: str) -> QPushButton:
        """
        Создание стилизованной кнопки навигации в тёмной теме.

        :param text: Текст кнопки
        :return: Настроенный QPushButton
        """
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
        """
        Запуск процесса сканирования сети.
        Открывает диалог настройки, затем запускает ScanWorker в фоне.
        """
        dialog = ScanDialog(self)
        if not dialog.exec():
            return

        params = dialog.get_scan_params()
        ip_range = params['ip_range']
        timeout = params['timeout']

        port_profile = params['port_profile']
        if "Стандартные" in port_profile:
            ports = [21, 22, 23, 80, 443, 445, 3389]
        elif "Все" in port_profile:
            ports = list(range(1, 1025))
        else:
            ports = [21, 22, 23, 80, 443, 445, 3389]

        self.progress_window = ScanProgressWindow()
        self.progress_window.show()

        self.scan_worker = ScanWorker(ip_range, ports, timeout)
        self.scan_worker.progress.connect(self.progress_window.update_progress)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)
        self.progress_window.cancel_btn.clicked.connect(self.scan_worker.stop)
        self.scan_worker.start()

    def on_scan_finished(self, results: list):
        """
        Обработчик завершения сканирования.

        :param results: Список результатов сканирования
        """
        if hasattr(self, 'progress_window'):
            self.progress_window.close()

        self.last_scan_results = results
        self.results.load_real_data(results)
        new_assets_count = self.assets.add_from_scan_results(results)
        self.dashboard.update_statistics(results)
        self.content_area.setCurrentIndex(1)

        info(
            self,
            "Сканирование завершено",
            f"Сканирование успешно завершено.\n\n"
            f"Найдено открытых портов: {len(results)}\n"
            f"Новых активов добавлено в реестр: {new_assets_count}"
        )

    def on_scan_error(self, error_msg: str):
        """
        Обработчик ошибки сканирования.

        :param error_msg: Сообщение об ошибке
        """
        if hasattr(self, 'progress_window'):
            self.progress_window.close()

        critical(self, "Ошибка сканирования", error_msg)

    def logout(self):
        """
        Выход из системы с русскими кнопками подтверждения.
        """
        if question(self, "Выход", "Вы уверены, что хотите выйти?"):
            from src.gui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()