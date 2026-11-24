# -*- coding: utf-8 -*-
# Точка входа приложения Network Auditor.
# Использует SQLite для портативности и автономной работы.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from src.core.database_manager import DatabaseManager
from src.core.user_manager import UserManager
from src.gui.login_window import LoginWindow

# SQLite — файл базы данных в папке проекта (портативность)
DB_URL = "sqlite:///" + os.path.join(os.path.dirname(__file__), "network_auditor.db")


def apply_dark_theme(app):
    """Применение глобальной тёмной темы."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, QColor(230, 230, 240))
    palette.setColor(QPalette.Base, QColor(40, 40, 55))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 62))
    palette.setColor(QPalette.ToolTipBase, QColor(230, 230, 240))
    palette.setColor(QPalette.ToolTipText, QColor(230, 230, 240))
    palette.setColor(QPalette.Text, QColor(230, 230, 240))
    palette.setColor(QPalette.Button, QColor(50, 50, 70))
    palette.setColor(QPalette.ButtonText, QColor(230, 230, 240))
    palette.setColor(QPalette.BrightText, QColor(255, 80, 80))
    palette.setColor(QPalette.Link, QColor(74, 158, 255))
    palette.setColor(QPalette.Highlight, QColor(74, 158, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    app.setStyleSheet("""
        QMainWindow, QWidget { background-color: #1e1e2e; color: #e6e6f0; }
        QLabel { color: #e6e6f0; }
        QLineEdit, QSpinBox, QComboBox, QTextEdit {
            background-color: #2a2a3e; color: #e6e6f0;
            border: 1px solid #3a3a52; border-radius: 4px; padding: 5px;
        }
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #4a9eff; }
        QPushButton {
            background-color: #3a3a52; color: #e6e6f0;
            border: 1px solid #4a4a62; border-radius: 4px; padding: 6px 12px;
        }
        QPushButton:hover { background-color: #4a4a62; }
        QPushButton:pressed { background-color: #2a2a3e; }
        QTableWidget {
            background-color: #2a2a3e; alternate-background-color: #32324a;
            color: #e6e6f0; gridline-color: #3a3a52;
        }
        QHeaderView::section {
            background-color: #3a3a52; color: #e6e6f0;
            padding: 5px; border: 1px solid #4a4a62;
        }
        QProgressBar {
            background-color: #2a2a3e; border: 1px solid #3a3a52;
            border-radius: 4px; text-align: center; color: #e6e6f0;
        }
        QProgressBar::chunk { background-color: #4a9eff; border-radius: 3px; }
        QCheckBox { color: #e6e6f0; }
    """)


def main():
    """Главная функция запуска приложения."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Network Auditor")
    app.setApplicationVersion("1.0")
    apply_dark_theme(app)

    # Инициализация SQLite базы данных
    try:
        db_manager = DatabaseManager(DB_URL)
        user_manager = UserManager(db_manager)
        user_manager.initialize_database()
    except Exception as e:
        QMessageBox.critical(
            None, "Ошибка инициализации БД",
            f"Не удалось инициализировать базу данных:\n{str(e)}"
        )
        sys.exit(1)

    # Передаём user_manager в окно авторизации
    window = LoginWindow(user_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()