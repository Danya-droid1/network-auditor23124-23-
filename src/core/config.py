# -*- coding: utf-8 -*-
"""
Менеджер конфигурации приложения.
Загружает и сохраняет настройки в JSON-файл.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля для работы с JSON-форматом
import json
# Импорт модуля для работы с файловой системой
import os
# Импорт типа Any для универсальных значений
from typing import Any, Optional


class ConfigurationManager:
    """
    Класс для управления настройками приложения.
    Хранит параметры в JSON-файле и предоставляет методы для их чтения/записи.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Инициализация менеджера конфигурации.

        :param config_file: Путь к файлу конфигурации
        """
        self.config_file = config_file
        # Загружаем конфигурацию при создании объекта
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Загрузка конфигурации из JSON-файла.
        Если файл не существует, возвращаются настройки по умолчанию.

        :return: Словарь с настройками
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()

    def save_config(self):
        """
        Сохранение текущей конфигурации в JSON-файл.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                # indent=2 для красивого форматирования
                # ensure_ascii=False для сохранения кириллицы
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получение значения параметра по ключу.

        :param key: Название параметра
        :param default: Значение по умолчанию, если ключ не найден
        :return: Значение параметра
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Установка значения параметра с автосохранением.

        :param key: Название параметра
        :param value: Новое значение
        """
        self.config[key] = value
        self.save_config()

    def get_default_config(self) -> dict:
        """
        Получение настроек по умолчанию.

        :return: Словарь с настройками по умолчанию
        """
        return {
            "scan_timeout": 1,  # Таймаут сканирования (сек)
            "auto_scan_enabled": False,  # Автосканирование включено
            "auto_scan_period": 7,  # Период автосканирования (дни)
            "notifications_enabled": True,  # Уведомления включены
            "reports_path": "C:/NetworkAuditor/Reports",  # Путь для отчётов
            "theme": "light",  # Тема оформления
            "language": "ru"  # Язык интерфейса
        }