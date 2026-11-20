# -*- coding: utf-8 -*-
"""
Точка входа приложения Network Auditor.
Запускает главное окно после авторизации пользователя.
Применяет глобальную тёмную тему оформления.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт системного модуля
import sys

# Импорт компонентов PySide6
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

# Импорт окна авторизации
from src.gui.login_window import LoginWindow


def apply_dark_theme(app):
    """
    Применение глобальной тёмной темы ко всему приложению.
    Настраивает палитру цветов Qt.
    """
    # Создаём палитру для тёмной темы
    palette = QPalette()

    # Основной фон (очень тёмный)
    palette.setColor(QPalette.Window, QColor(30, 30, 46))
    # Светлый текст
    palette.setColor(QPalette.WindowText, QColor(230, 230, 240))
    # Фон для базовых элементов
    palette.setColor(QPalette.Base, QColor(40, 40, 55))
    # Фон для альтернативных строк в таблицах
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 62))
    # Цвет текста подсказок
    palette.setColor(QPalette.ToolTipBase, QColor(230, 230, 240))
    palette.setColor(QPalette.ToolTipText, QColor(230, 230, 240))
    # Цвет обычного текста
    palette.setColor(QPalette.Text, QColor(230, 230, 240))
    # Цвет кнопок
    palette.setColor(QPalette.Button, QColor(50, 50, 70))
    # Цвет текста на кнопках
    palette.setColor(QPalette.ButtonText, QColor(230, 230, 240))
    # Яркий цвет (для активных элементов)
    palette.setColor(QPalette.BrightText, QColor(255, 80, 80))
    # Цвет ссылок
    palette.setColor(QPalette.Link, QColor(74, 158, 255))
    # Цвет подсветки (выделение)
    palette.setColor(QPalette.Highlight, QColor(74, 158, 255))
    # Цвет текста на подсветке
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    # Применяем палитру к приложению
    app.setPalette(palette)

    # Дополнительные стили через QSS
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #1e1e2e;
            color: #e6e6f0;
        }
        QLabel {
            color: #e6e6f0;
        }
        QLineEdit, QSpinBox, QComboBox, QTextEdit {
            background-color: #2a2a3e;
            color: #e6e6f0;
            border: 1px solid #3a3a52;
            border-radius: 4px;
            padding: 5px;
        }
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #4a9eff;
        }
        QPushButton {
            background-color: #3a3a52;
            color: #e6e6f0;
            border: 1px solid #4a4a62;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #4a4a62;
        }
        QPushButton:pressed {
            background-color: #2a2a3e;
        }
        QTableWidget {
            background-color: #2a2a3e;
            alternate-background-color: #32324a;
            color: #e6e6f0;
            gridline-color: #3a3a52;
        }
        QHeaderView::section {
            background-color: #3a3a52;
            color: #e6e6f0;
            padding: 5px;
            border: 1px solid #4a4a62;
        }
        QProgressBar {
            background-color: #2a2a3e;
            border: 1px solid #3a3a52;
            border-radius: 4px;
            text-align: center;
            color: #e6e6f0;
        }
        QProgressBar::chunk {
            background-color: #4a9eff;
            border-radius: 3px;
        }
        QCheckBox {
            color: #e6e6f0;
        }
        QMessageBox {
            background-color: #1e1e2e;
            color: #e6e6f0;
        }
    """)


def main():
    """
    Главная функция запуска приложения.
    Создаёт QApplication, применяет тёмную тему и показывает окно авторизации.
    """
    # Создаём экземпляр приложения Qt
    app = QApplication(sys.argv)

    # Устанавливаем стиль Fusion (кроссплатформенный, хорошо кастомизируется)
    app.setStyle("Fusion")

    # Задаём название и версию приложения
    app.setApplicationName("Network Auditor")
    app.setApplicationVersion("1.0")

    # Применяем тёмную тему
    apply_dark_theme(app)

    # Создаём и показываем окно авторизации
    window = LoginWindow()
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())


# Проверка, что файл запущен напрямую
if __name__ == '__main__':
    main()