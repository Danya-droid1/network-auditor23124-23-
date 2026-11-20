# -*- coding: utf-8 -*-
"""
Главное окно приложения с боковым меню.
Реализует навигацию между разделами с учётом роли пользователя
(admin видит все пункты, auditor — только отчёты).
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame, QMessageBox)
from PySide6.QtCore import Qt

# Импорт всех окон приложения
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
        # Устанавливаем заголовок с указанием роли
        self.setWindowTitle(f"Network Auditor - {user_data.get('role', 'User').capitalize()}")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Создаём центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Боковое меню (Sidebar) ===
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Информация о текущем пользователе
        user_label = QLabel(f"Пользователь: {self.user_data.get('username')}")
        user_label.setStyleSheet("font-weight: bold; margin-bottom: 20px; font-size: 14px;")
        sidebar_layout.addWidget(user_label)

        # Кнопки навигации
        self.btn_dashboard = self.create_nav_button("📊 Дашборд")
        self.btn_scan = self.create_nav_button("🔍 Новое сканирование")
        self.btn_results = self.create_nav_button("📋 Результаты")
        self.btn_reports = self.create_nav_button("📄 Отчёты")
        self.btn_assets = self.create_nav_button("💻 Активы")

        # Добавляем кнопки в меню
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_scan)
        sidebar_layout.addWidget(self.btn_results)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addWidget(self.btn_assets)

        # Кнопки только для администратора
        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities = self.create_nav_button("🛡️ Уязвимости")
            self.btn_settings = self.create_nav_button("⚙️ Настройки")
            sidebar_layout.addWidget(self.btn_vulnerabilities)
            sidebar_layout.addWidget(self.btn_settings)

        # Растягиваем пространство между кнопками и нижним блоком
        sidebar_layout.addStretch()

        # Нижние кнопки (профиль, справка, выход)
        self.btn_profile = self.create_nav_button("👤 Профиль")
        self.btn_about = self.create_nav_button("ℹ️ О программе")
        self.btn_logout = self.create_nav_button("🚪 Выход")

        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_about)
        sidebar_layout.addWidget(self.btn_logout)

        # === Область контента (Stacked Widget) ===
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: #ecf0f1;")

        # Создаём экземпляры всех окон
        self.dashboard = DashboardWindow(self.user_data)
        self.results = ResultsWindow()
        self.reports = ReportsWindow()
        self.assets = AssetsWindow()
        self.profile = ProfileWindow(self.user_data)
        self.about = AboutWindow()

        # Добавляем окна в стек
        self.content_area.addWidget(self.dashboard)  # Индекс 0
        self.content_area.addWidget(self.results)  # Индекс 1
        self.content_area.addWidget(self.reports)  # Индекс 2
        self.content_area.addWidget(self.assets)  # Индекс 3
        self.content_area.addWidget(self.profile)  # Индекс 4
        self.content_area.addWidget(self.about)  # Индекс 5

        # Для администратора добавляем дополнительные окна
        if self.user_data.get('role') == 'admin':
            self.vulnerabilities = VulnerabilityDBWindow()  # Индекс 6
            self.settings = SettingsWindow()  # Индекс 7
            self.content_area.addWidget(self.vulnerabilities)
            self.content_area.addWidget(self.settings)

        # Собираем основной layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)
        central_widget.setLayout(main_layout)

        # === Подключение обработчиков кнопок ===
        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.btn_scan.clicked.connect(self.start_scan)
        self.btn_results.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
        self.btn_assets.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        self.btn_profile.clicked.connect(lambda: self.content_area.setCurrentIndex(4))
        self.btn_about.clicked.connect(lambda: self.content_area.setCurrentIndex(5))

        # Обработчики для администратора
        if self.user_data.get('role') == 'admin':
            self.btn_vulnerabilities.clicked.connect(lambda: self.content_area.setCurrentIndex(6))
            self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(7))

        # Обработчик выхода
        self.btn_logout.clicked.connect(self.logout)

    def create_nav_button(self, text: str) -> QPushButton:
        """
        Создание стилизованной кнопки навигации.

        :param text: Текст кнопки
        :return: Настроенный экземпляр QPushButton
        """
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
        """Запуск диалога настройки нового сканирования."""
        dialog = ScanDialog(self)
        if dialog.exec():
            params = dialog.get_scan_params()
            QMessageBox.information(self, "Сканирование запущено",
                                    f"Начато сканирование диапазона: {params['ip_range']}")
            # Переходим на вкладку результатов
            self.content_area.setCurrentIndex(1)

    def logout(self):
        """Выход из системы с возвратом на окно авторизации."""
        # Запрашиваем подтверждение выхода
        reply = QMessageBox.question(self, "Выход",
                                     "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Импортируем и показываем окно авторизации
            from src.gui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            # Закрываем главное окно
            self.close()