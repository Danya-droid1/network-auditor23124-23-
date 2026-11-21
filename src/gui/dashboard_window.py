# -*- coding: utf-8 -*-
"""
Окно дашборда со статистикой и быстрыми действиями.
Отображает реальную статистику на основе последних сканирований.
Исправлено отображение текста в карточках через objectName и прозрачный фон меток.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QGridLayout)
from PySide6.QtCore import Qt


class DashboardWindow(QWidget):
    """
    Главный дашборд приложения.
    Показывает статистику и предоставляет быстрые действия.
    """

    def __init__(self, user_data: dict):
        """
        Инициализация дашборда.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        super().__init__()
        self.user_data = user_data
        # Счётчики статистики
        self.total_scans = 0
        self.open_ports = 0
        self.high_risk = 0
        self.total_assets = 0
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        header = QLabel("Панель управления")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        # Приветствие
        welcome = QLabel(f"Добро пожаловать, {self.user_data.get('full_name', 'Пользователь')}!")
        welcome.setStyleSheet("font-size: 16px; color: #a0a0b0; background: transparent;")
        layout.addWidget(welcome)

        # === Сетка статистических карточек ===
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        # Создаём карточки
        self.card_scans = self.create_stat_card("Всего сканирований", str(self.total_scans), "#3498db")
        self.card_ports = self.create_stat_card("Открытых портов", str(self.open_ports), "#e74c3c")
        self.card_risk = self.create_stat_card("Высокий риск", str(self.high_risk), "#e67e22")
        self.card_assets = self.create_stat_card("Активов в сети", str(self.total_assets), "#27ae60")

        stats_grid.addWidget(self.card_scans, 0, 0)
        stats_grid.addWidget(self.card_ports, 0, 1)
        stats_grid.addWidget(self.card_risk, 1, 0)
        stats_grid.addWidget(self.card_assets, 1, 1)

        layout.addLayout(stats_grid)

        layout.addSpacing(30)

        # === Блок быстрых действий ===
        quick_actions = QLabel("Быстрые действия")
        quick_actions.setStyleSheet("font-size: 18px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(quick_actions)

        actions_layout = QHBoxLayout()

        self.btn_new_scan = QPushButton("🔍 Начать новое сканирование")
        self.btn_new_scan.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 12px; font-size: 14px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)

        self.btn_view_reports = QPushButton("📄 Просмотреть отчёты")
        self.btn_view_reports.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 12px; font-size: 14px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)

        self.btn_manage_assets = QPushButton("💻 Управление активами")
        self.btn_manage_assets.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; color: white; 
                padding: 12px; font-size: 14px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #af7ac5; }
        """)

        actions_layout.addWidget(self.btn_new_scan)
        actions_layout.addWidget(self.btn_view_reports)
        actions_layout.addWidget(self.btn_manage_assets)

        layout.addLayout(actions_layout)

        layout.addStretch()
        self.setLayout(layout)

    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """
        Создание цветной карточки со статистикой.
        Использует objectName для точечного стилизования меток,
        чтобы стили QFrame не перекрывали цвет текста QLabel.

        :param title: Название показателя
        :param value: Числовое значение
        :param color: Цвет фона карточки
        :return: Настроенный QFrame
        """
        # Создаём контейнер карточки
        card = QFrame()
        # Задаём objectName для изоляции стилей — стили применяются только к самой карточке
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {color};
                border-radius: 10px;
            }}
        """)
        card.setFixedHeight(140)

        # Создаём layout для карточки
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        # Растяжение сверху и снизу для центрирования по вертикали
        card_layout.addStretch()

        # Большое число (значение)
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet("""
            QLabel#statValue {
                font-size: 36px;
                font-weight: bold;
                color: white;
                background: transparent;
                border: none;
            }
        """)
        value_label.setAlignment(Qt.AlignCenter)

        # Подпись (название)
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        title_label.setStyleSheet("""
            QLabel#statTitle {
                font-size: 14px;
                color: white;
                background: transparent;
                border: none;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)

        # Добавляем метки в layout карточки
        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)
        card_layout.addStretch()

        # Сохраняем ссылки на виджеты для последующего обновления
        card.value_label = value_label
        card.title_label = title_label

        return card

    def update_statistics(self, scan_results: list):
        """
        Обновление статистики на основе результатов сканирования.

        :param scan_results: Список результатов последнего сканирования
        """
        # Увеличиваем счётчик сканирований
        self.total_scans += 1

        # Количество открытых портов
        self.open_ports = len(scan_results)

        # Подсчёт портов высокого и критического риска
        high_risk_ports = [21, 23, 445, 3389, 5432, 3306]
        self.high_risk = sum(1 for r in scan_results if r.get('port') in high_risk_ports)

        # Подсчёт уникальных активов (IP-адресов)
        unique_ips = set(r.get('ip') for r in scan_results)
        self.total_assets = len(unique_ips)

        # Обновляем значения в карточках
        self.card_scans.value_label.setText(str(self.total_scans))
        self.card_ports.value_label.setText(str(self.open_ports))
        self.card_risk.value_label.setText(str(self.high_risk))
        self.card_assets.value_label.setText(str(self.total_assets))

        # Принудительно перерисовываем карточки
        self.card_scans.value_label.repaint()
        self.card_ports.value_label.repaint()
        self.card_risk.value_label.repaint()
        self.card_assets.value_label.repaint()