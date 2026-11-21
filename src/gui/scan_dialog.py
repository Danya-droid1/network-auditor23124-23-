# -*- coding: utf-8 -*-
# Диалоговое окно настройки сканирования.
# Позволяет ввести IP-диапазон с CIDR-маской, выбрать набор портов
# или ввести произвольный список портов.
# Валидирует введённые данные и показывает оценку времени сканирования.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QSpinBox)
from PySide6.QtCore import Qt

from src.utils.dialogs import warning, question


class ScanDialog(QDialog):
    """
    Диалог настройки нового сканирования сети.
    Поддерживает CIDR-маски и произвольный список портов.
    """

    def __init__(self, parent=None):
        """Инициализация диалога настройки сканирования."""
        super().__init__(parent)
        self.setWindowTitle("Настройка сканирования сети")
        self.resize(500, 420)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса диалога."""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("Параметры сканирования")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(title)

        # Поле ввода IP-диапазона с CIDR-маской
        layout.addWidget(QLabel("Целевой диапазон IP (например, 192.168.1.0/24):"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.0/24")
        self.ip_input.textChanged.connect(self.update_time_estimate)
        layout.addWidget(self.ip_input)

        # Выбор профиля портов
        layout.addWidget(QLabel("Выбор портов:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems([
            "Стандартные порты (21, 22, 23, 80, 443, 445, 3389)",
            "Все распространённые порты (1-1024)",
            "Произвольный список"
        ])
        self.port_combo.currentTextChanged.connect(self.on_port_selection_changed)
        layout.addWidget(self.port_combo)

        # Поле для произвольного списка портов (скрыто по умолчанию)
        self.custom_ports_input = QLineEdit()
        self.custom_ports_input.setPlaceholderText("Введите порты через запятую: 80, 443, 8080, 3306")
        self.custom_ports_input.setVisible(False)
        self.custom_ports_input.textChanged.connect(self.update_time_estimate)
        layout.addWidget(self.custom_ports_input)

        # Настройка таймаута
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Таймаут на порт (секунды):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        self.timeout_spin.valueChanged.connect(self.update_time_estimate)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)

        # Оценка времени сканирования
        self.time_estimate_label = QLabel("Примерное время сканирования: не рассчитано")
        self.time_estimate_label.setStyleSheet(
            "font-size: 13px; color: #f39c12; background: transparent; font-weight: bold;")
        layout.addWidget(self.time_estimate_label)

        layout.addStretch()

        # Кнопки действий
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ Начать сканирование")
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.btn_cancel = QPushButton("✖ Отмена")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white; 
                padding: 10px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #95a5a6; }
        """)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Подключаем обработчики
        self.btn_start.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def on_port_selection_changed(self, text: str):
        """
        Обработчик изменения выбора портов.
        Показывает/скрывает поле для произвольного списка.
        """
        if "Произвольный" in text:
            self.custom_ports_input.setVisible(True)
        else:
            self.custom_ports_input.setVisible(False)

        self.update_time_estimate()

    def get_ports_list(self) -> list:
        """
        Получение списка портов на основе выбранного профиля.

        :return: Список номеров портов
        """
        profile = self.port_combo.currentText()

        if "Стандартные" in profile:
            return [21, 22, 23, 80, 443, 445, 3389]
        elif "Все распространённые" in profile:
            return list(range(1, 1025))
        else:
            # Произвольный список
            ports_text = self.custom_ports_input.text().strip()
            if not ports_text:
                return []

            try:
                ports = [int(p.strip()) for p in ports_text.split(',') if p.strip()]
                ports = [p for p in ports if 1 <= p <= 65535]
                return ports
            except ValueError:
                return []

    def update_time_estimate(self):
        """
        Обновление оценки времени сканирования.
        Формула: хосты × порты × таймаут = секунды
        """
        ip_range = self.ip_input.text().strip()
        timeout = self.timeout_spin.value()
        ports = self.get_ports_list()

        if not ip_range or not ports:
            self.time_estimate_label.setText("Примерное время сканирования: не рассчитано")
            return

        # Парсим CIDR
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            num_hosts = network.num_addresses - 2
            if num_hosts < 1:
                num_hosts = 1
        except ValueError:
            self.time_estimate_label.setText("Примерное время сканирования: некорректный IP-диапазон")
            return

        # Рассчитываем время
        total_seconds = num_hosts * len(ports) * timeout

        if total_seconds < 60:
            time_str = f"{total_seconds} сек"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time_str = f"{minutes} мин {seconds} сек"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            time_str = f"{hours} ч {minutes} мин"

        self.time_estimate_label.setText(
            f"Примерное время сканирования: {time_str}\n"
            f"(Хостов: {num_hosts}, Портов: {len(ports)}, Таймаут: {timeout} сек)"
        )

    def validate_and_accept(self):
        """
        Валидация введённых данных перед закрытием диалога.
        """
        ip = self.ip_input.text().strip()

        if not ip:
            warning(self, "Ошибка валидации", "Диапазон IP не может быть пустым.")
            return

        # Проверка CIDR-формата
        try:
            network = ipaddress.ip_network(ip, strict=False)

            # Предупреждение для больших сетей
            num_hosts = network.num_addresses - 2
            if num_hosts > 1000:
                if not question(
                        self,
                        "Внимание: большая сеть",
                        f"Выбранная сеть содержит {num_hosts} хостов.\n\n"
                        f"Сканирование может занять много времени.\n\n"
                        f"Продолжить?"
                ):
                    return
        except ValueError:
            warning(
                self, "Ошибка валидации",
                "Некорректный формат IP-диапазона.\nПример: 192.168.1.0/24"
            )
            return

        # Проверка произвольных портов
        if "Произвольный" in self.port_combo.currentText():
            ports = self.get_ports_list()
            if not ports:
                warning(
                    self, "Ошибка валидации",
                    "Введите хотя бы один порт (от 1 до 65535).\nПример: 80, 443, 8080"
                )
                return

        self.accept()

    def get_scan_params(self) -> dict:
        """
        Получение параметров сканирования из полей диалога.

        :return: Словарь с параметрами сканирования
        """
        return {
            "ip_range": self.ip_input.text().strip(),
            "port_profile": self.port_combo.currentText(),
            "ports": self.get_ports_list(),
            "timeout": self.timeout_spin.value()
        }


# Импорт нужен для расчёта времени
import ipaddress