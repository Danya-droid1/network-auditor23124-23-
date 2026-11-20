# -*- coding: utf-8 -*-
"""
Окно справки "О программе".
Содержит ФИО автора, тему ВКР, версию и университет.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class AboutWindow(QWidget):
    """
    Окно "О программе" с информацией об авторе и версии.
    """

    def __init__(self):
        """Инициализация окна справки."""
        super().__init__()
        self.setWindowTitle("О программе Network Auditor")
        self.resize(450, 350)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Название приложения
        title = QLabel("Network Auditor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Версия приложения
        version = QLabel("Версия 1.0")
        version.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        layout.addSpacing(20)

        # Описание приложения
        desc = QLabel(
            "Десктопное приложение для аудита открытых сетевых портов\nи выявления уязвимостей в локальных сетях.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 12px;")
        layout.addWidget(desc)

        layout.addSpacing(20)

        # Информация об авторе
        author = QLabel("Автор: Голуб Даниил Николаевич")
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(author)

        # Группа студента
        group = QLabel("Группа: о.ИЗДтс 23.1/Б4-23")
        group.setAlignment(Qt.AlignCenter)
        layout.addWidget(group)

        # Тема ВКР
        thesis = QLabel(
            "Тема ВКР: Разработка клиент-серверного десктопного приложения\nдля аудита открытых сетевых портов")
        thesis.setAlignment(Qt.AlignCenter)
        thesis.setStyleSheet("font-size: 11px; font-style: italic;")
        layout.addWidget(thesis)

        layout.addSpacing(20)

        # Информация об университете
        university = QLabel("ЧОУ ВО «Московский университет им. С.Ю. Витте»\nКафедра информационных систем")
        university.setAlignment(Qt.AlignCenter)
        university.setStyleSheet("font-size: 11px; color: #7f8c8d;")
        layout.addWidget(university)

        # Год выполнения работы
        year = QLabel("2026")
        year.setAlignment(Qt.AlignCenter)
        layout.addWidget(year)

        self.setLayout(layout)