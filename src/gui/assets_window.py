# -*- coding: utf-8 -*-
"""
Окно реестра сетевых активов.
Отображает таблицу всех учтённых сетевых узлов с их характеристиками.
Поддерживает операции: добавление, удаление, массовое удаление,
импорт из результатов сканирования.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QHeaderView, QDialog, QFormLayout,
                               QLineEdit, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# Импорт обёртки диалогов с русскими кнопками
from src.utils.dialogs import info, warning, question


class AssetsWindow(QWidget):
    """
    Окно реестра сетевых активов.
    """

    def __init__(self):
        """Инициализация окна реестра активов."""
        super().__init__()
        self.assets = []
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Реестр сетевых активов")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        self.info_label = QLabel("Всего активов: 0")
        self.info_label.setStyleSheet("font-size: 13px; color: #a0a0b0; background: transparent;")
        layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "IP-адрес", "Имя хоста", "Тип ОС", "Сегмент",
            "Открытых портов", "Дата обнаружения"
        ])

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Добавить актив")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.add_btn.clicked.connect(self.add_asset)

        self.import_btn = QPushButton("📥 Импорт из сканирования")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #5dade2; }
        """)
        self.import_btn.clicked.connect(self.import_from_scan)

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #af7ac5; }
        """)
        self.refresh_btn.clicked.connect(self.refresh_table)

        self.delete_btn = QPushButton("🗑 Удалить выбранное")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #f39c12; }
        """)
        self.delete_btn.clicked.connect(self.delete_selected)

        self.delete_all_btn = QPushButton("❌ Удалить все")
        self.delete_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; 
                padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #ec7063; }
        """)
        self.delete_all_btn.clicked.connect(self.delete_all)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.delete_all_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы активов."""
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.assets))

        for row, asset in enumerate(self.assets):
            id_item = QTableWidgetItem(str(asset.get('id', row + 1)))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)

            ip_item = QTableWidgetItem(asset.get('ip', 'N/A'))
            ip_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, ip_item)

            hostname_item = QTableWidgetItem(asset.get('hostname', 'Неизвестно'))
            hostname_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, hostname_item)

            os_item = QTableWidgetItem(asset.get('os_type', 'Неизвестно'))
            os_item.setTextAlignment(Qt.AlignCenter)
            if asset.get('os_type') == 'Windows':
                os_item.setBackground(QColor("#3498db"))
                os_item.setForeground(QColor("white"))
            elif asset.get('os_type') == 'Linux':
                os_item.setBackground(QColor("#e67e22"))
                os_item.setForeground(QColor("white"))
            self.table.setItem(row, 3, os_item)

            segment_item = QTableWidgetItem(asset.get('segment', 'Не определён'))
            segment_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, segment_item)

            ports_count = len(asset.get('open_ports', []))
            ports_item = QTableWidgetItem(str(ports_count))
            ports_item.setTextAlignment(Qt.AlignCenter)
            if ports_count >= 3:
                ports_item.setBackground(QColor("#e74c3c"))
                ports_item.setForeground(QColor("white"))
            elif ports_count >= 1:
                ports_item.setBackground(QColor("#f39c12"))
                ports_item.setForeground(QColor("black"))
            self.table.setItem(row, 5, ports_item)

            date_item = QTableWidgetItem(asset.get('detected_at', 'N/A'))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 6, date_item)

        self.info_label.setText(f"Всего активов: {len(self.assets)}")

    def add_asset(self):
        """Открытие диалога добавления нового актива."""
        dialog = AddAssetDialog(self)
        if dialog.exec():
            asset_data = dialog.get_asset_data()

            for existing in self.assets:
                if existing.get('ip') == asset_data['ip']:
                    warning(self, "Дубликат",
                            f"Актив с IP-адресом {asset_data['ip']} уже существует в реестре.")
                    return

            self.assets.append(asset_data)
            self.refresh_table()
            info(self, "Успех", f"Актив {asset_data['ip']} успешно добавлен в реестр.")

    def import_from_scan(self):
        """Импорт активов из результатов последнего сканирования."""
        main_window = self.window()

        if not hasattr(main_window, 'last_scan_results') or not main_window.last_scan_results:
            warning(self, "Нет данных",
                    "Нет результатов сканирования для импорта.\n\nСначала выполните сканирование сети.")
            return

        ip_data = {}
        for result in main_window.last_scan_results:
            ip = result.get('ip')
            if ip not in ip_data:
                ip_data[ip] = {
                    'ip': ip,
                    'hostname': result.get('hostname', 'Неизвестно'),
                    'os_type': result.get('os_type', 'Неизвестно'),
                    'open_ports': [],
                    'segment': self._detect_segment(ip),
                    'detected_at': result.get('detected_at', 'N/A')
                }
            ip_data[ip]['open_ports'].append(result.get('port'))

        new_count = 0
        for ip, data in ip_data.items():
            exists = any(a.get('ip') == ip for a in self.assets)
            if not exists:
                self.assets.append(data)
                new_count += 1

        self.refresh_table()

        if new_count > 0:
            info(self, "Импорт завершён",
                 f"Импортировано новых активов: {new_count}\n\n"
                 f"Всего активов в реестре: {len(self.assets)}")
        else:
            info(self, "Импорт завершён",
                 "Все обнаруженные устройства уже есть в реестре.\n\nНовые активы не добавлены.")

    def _detect_segment(self, ip: str) -> str:
        """Определение сегмента сети по IP-адресу."""
        parts = ip.split('.')
        if len(parts) != 4:
            return "Не определён"

        if parts[0] == '192' and parts[1] == '168' and parts[2] == '1':
            return "Административный"
        elif parts[0] == '192' and parts[1] == '168' and parts[2] == '2':
            return "Учебный"
        elif parts[0] == '10' and parts[1] == '0':
            return "Филиал"
        elif parts[0] == '172' and parts[1] == '16':
            return "Гостевой"
        elif parts[0] == '127':
            return "Локальный"
        return "Не определён"

    def delete_selected(self):
        """Удаление выбранного актива."""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Не выбран актив",
                    "Пожалуйста, выберите актив в таблице для удаления.")
            return

        row = selected_rows[0].row()

        if row >= len(self.assets):
            return

        asset = self.assets[row]
        ip = asset.get('ip', 'N/A')
        hostname = asset.get('hostname', 'Неизвестно')

        if question(self, "Подтверждение удаления",
                    f"Вы уверены, что хотите удалить актив?\n\n"
                    f"IP-адрес: {ip}\n"
                    f"Имя хоста: {hostname}\n\n"
                    f"Это действие нельзя отменить."):
            self.assets.pop(row)
            self.refresh_table()
            info(self, "Успех", f"Актив {ip} удалён из реестра.")

    def delete_all(self):
        """Массовое удаление всех активов."""
        if not self.assets:
            info(self, "Реестр пуст", "В реестре нет активов для удаления.")
            return

        if question(self, "ВНИМАНИЕ: Массовое удаление",
                    f"Вы собираетесь удалить ВСЕ активы из реестра!\n\n"
                    f"Количество активов: {len(self.assets)}\n\n"
                    f"Это действие нельзя отменить.\nПродолжить?"):
            self.assets.clear()
            self.refresh_table()
            info(self, "Успех", "Все активы удалены из реестра.")

    def add_from_scan_results(self, scan_results: list):
        """
        Автоматическое добавление активов из результатов сканирования.

        :param scan_results: Список результатов сканирования
        :return: Количество добавленных новых активов
        """
        ip_data = {}
        for result in scan_results:
            ip = result.get('ip')
            if ip not in ip_data:
                ip_data[ip] = {
                    'ip': ip,
                    'hostname': result.get('hostname', 'Неизвестно'),
                    'os_type': result.get('os_type', 'Неизвестно'),
                    'open_ports': [],
                    'segment': self._detect_segment(ip),
                    'detected_at': result.get('detected_at', 'N/A')
                }
            ip_data[ip]['open_ports'].append(result.get('port'))

        new_count = 0
        for ip, data in ip_data.items():
            exists = any(a.get('ip') == ip for a in self.assets)
            if not exists:
                self.assets.append(data)
                new_count += 1

        self.refresh_table()
        return new_count


class AddAssetDialog(QDialog):
    """Диалог ручного добавления нового актива."""

    def __init__(self, parent=None):
        """Инициализация диалога добавления актива."""
        super().__init__(parent)
        self.setWindowTitle("Добавление актива")
        self.resize(450, 350)
        self.init_ui()

    def init_ui(self):
        """Инициализация формы диалога."""
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Добавление нового актива")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addRow(title)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.10")
        layout.addRow("IP-адрес:", self.ip_input)

        self.hostname_input = QLineEdit()
        self.hostname_input.setPlaceholderText("srv-db-01")
        layout.addRow("Имя хоста:", self.hostname_input)

        self.os_combo = QComboBox()
        self.os_combo.addItems(["Windows", "Linux", "Неизвестно"])
        layout.addRow("Тип ОС:", self.os_combo)

        self.segment_combo = QComboBox()
        self.segment_combo.addItems([
            "Административный", "Учебный", "Филиал", "Гостевой", "Не определён"
        ])
        layout.addRow("Сегмент сети:", self.segment_combo)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("✓ Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("✖ Отмена")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def validate_and_accept(self):
        """Валидация данных перед сохранением."""
        ip = self.ip_input.text().strip()

        if not ip:
            warning(self, "Ошибка", "IP-адрес не может быть пустым.")
            return

        parts = ip.split('.')
        if len(parts) != 4:
            warning(self, "Ошибка", "Некорректный формат IP-адреса.\nПример: 192.168.1.10")
            return

        try:
            for part in parts:
                num = int(part)
                if not 0 <= num <= 255:
                    raise ValueError
        except ValueError:
            warning(self, "Ошибка", "Каждая часть IP-адреса должна быть числом от 0 до 255.")
            return

        self.accept()

    def get_asset_data(self) -> dict:
        """Получение данных актива из полей диалога."""
        from datetime import datetime
        return {
            'ip': self.ip_input.text().strip(),
            'hostname': self.hostname_input.text().strip() or "Неизвестно",
            'os_type': self.os_combo.currentText(),
            'open_ports': [],
            'segment': self.segment_combo.currentText(),
            'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }