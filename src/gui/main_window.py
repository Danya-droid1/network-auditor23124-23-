# -*- coding: utf-8 -*-
"""
Главное окно приложения с боковым меню.
Реализует навигацию между разделами с учётом роли пользователя.
Интегрирует реальное сканирование сети через ScanWorker.
Автоматически импортирует найденные устройства в реестр активов.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame, QMessageBox)
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
        # Ссылка на рабочий поток сканирования
        self.scan_worker = None
        # Хранилище последних результатов сканирования
        self.last_scan_results = []

        # Устанавливаем заголовок с указанием роли
        self.setWindowTitle(f"Network Auditor — {user_data.get('role', 'User').capitalize()}")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Боковое меню (Sidebar) ===
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border-right: 1px solid #2a2a3e;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Информация о текущем пользователе
        user_label = QLabel(f"👤 {self.user_data.get('username')}")
        user_label.setStyleSheet("font-weight: bold; margin-bottom: 20px; font-size: 14px; color: #4a9eff;")
        sidebar_layout.addWidget(user_label)

        # Кнопки навигации
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

        # Кнопки только для администратора
        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities = self.create_nav_button("🛡️ Уязвимости")
            self.btn_settings = self.create_nav_button("⚙️ Настройки")
            sidebar_layout.addWidget(self.btn_vulnerabilities)
            sidebar_layout.addWidget(self.btn_settings)

        sidebar_layout.addStretch()

        # Нижние кнопки
        self.btn_profile = self.create_nav_button("👤 Профиль")
        self.btn_about = self.create_nav_button("ℹ️ О программе")
        self.btn_logout = self.create_nav_button("🚪 Выход")

        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_about)
        sidebar_layout.addWidget(self.btn_logout)

        # === Область контента ===
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: #1e1e2e;")

        # Создаём экземпляры всех окон
        self.dashboard = DashboardWindow(self.user_data)
        self.results = ResultsWindow()
        self.assets = AssetsWindow()
        self.reports = ReportsWindow()
        self.profile = ProfileWindow(self.user_data)
        self.about = AboutWindow()

        # Добавляем окна в стек
        self.content_area.addWidget(self.dashboard)  # 0
        self.content_area.addWidget(self.results)  # 1
        self.content_area.addWidget(self.assets)  # 2
        self.content_area.addWidget(self.reports)  # 3
        self.content_area.addWidget(self.profile)  # 4
        self.content_area.addWidget(self.about)  # 5

        # Для администратора — дополнительные окна
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
        # Открываем диалог настройки
        dialog = ScanDialog(self)
        if not dialog.exec():
            return  # Пользователь отменил

        # Получаем параметры из диалога
        params = dialog.get_scan_params()
        ip_range = params['ip_range']
        timeout = params['timeout']

        # Определяем список портов в зависимости от профиля
        port_profile = params['port_profile']
        if "Стандартные" in port_profile:
            ports = [21, 22, 23, 80, 443, 445, 3389]
        elif "Все" in port_profile:
            ports = list(range(1, 1025))
        else:
            ports = [21, 22, 23, 80, 443, 445, 3389]

        # Создаём окно прогресса
        self.progress_window = ScanProgressWindow()
        self.progress_window.show()

        # Создаём рабочий поток для сканирования
        self.scan_worker = ScanWorker(ip_range, ports, timeout)

        # Подключаем сигналы
        self.scan_worker.progress.connect(self.progress_window.update_progress)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)

        # Подключаем кнопку отмены
        self.progress_window.cancel_btn.clicked.connect(self.scan_worker.stop)

        # Запускаем поток
        self.scan_worker.start()

    def on_scan_finished(self, results: list):
        """
        Обработчик завершения сканирования.
        Сохраняет результаты, передаёт их в окна результатов и активов.

        :param results: Список результатов сканирования
        """
        # Закрываем окно прогресса
        if hasattr(self, 'progress_window'):
            self.progress_window.close()

        # Сохраняем результаты
        self.last_scan_results = results

        # Передаём результаты в окно результатов
        self.results.load_real_data(results)

        # Автоматически импортируем найденные устройства в активы
        new_assets_count = self.assets.add_from_scan_results(results)

        # Обновляем статистику на дашборде
        self.dashboard.update_statistics(results)

        # Переходим на вкладку результатов
        self.content_area.setCurrentIndex(1)

        # Показываем уведомление
        QMessageBox.information(
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

        QMessageBox.critical(self, "Ошибка сканирования", error_msg)

    def logout(self):
        """Выход из системы с возвратом на окно авторизации."""
        reply = QMessageBox.question(
            self, "Выход",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            from src.gui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()