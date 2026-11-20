# -*- coding: utf-8 -*-
"""
Точка входа приложения Network Auditor.
Запускает главное окно после авторизации пользователя.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт системного модуля для работы с интерпретатором
import sys

# Импорт компонентов графического интерфейса из библиотеки PySide6
from PySide6.QtWidgets import QApplication

# Импорт окна авторизации
from src.gui.login_window import LoginWindow


def main():
    """
    Главная функция запуска приложения.
    Создаёт экземпляр QApplication и отображает окно авторизации.
    """
    # Создаём экземпляр приложения Qt
    app = QApplication(sys.argv)

    # Устанавливаем стиль интерфейса Fusion (кроссплатформенный)
    app.setStyle("Fusion")

    # Задаём название приложения
    app.setApplicationName("Network Auditor")

    # Задаём версию приложения
    app.setApplicationVersion("1.0")

    # Создаём и отображаем окно авторизации
    window = LoginWindow()
    window.show()

    # Запускаем цикл обработки событий Qt
    sys.exit(app.exec())


# Проверка, что файл запущен напрямую, а не импортирован
if __name__ == '__main__':
    main()