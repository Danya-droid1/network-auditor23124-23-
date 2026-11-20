# -*- coding: utf-8 -*-
"""
Модуль журналирования действий пользователей (audit log).
Записывает все значимые события в файл audit.log для последующего анализа.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля стандартного логгирования Python
import logging
# Импорт модуля datetime для временных меток
from datetime import datetime
# Импорт типа Optional для необязательных параметров
from typing import Optional


class AuditLogger:
    """
    Класс для ведения журнала аудита действий пользователей.
    Использует стандартный модуль logging для записи событий в файл.
    """

    def __init__(self, log_file: str = "audit.log"):
        """
        Инициализация логгера.

        :param log_file: Путь к файлу журнала
        """
        self.log_file = log_file
        # Создаём именованный логгер
        self.logger = logging.getLogger('NetworkAuditor')
        self.logger.setLevel(logging.INFO)

        # Настраиваем обработчик, если он ещё не добавлен
        if not self.logger.handlers:
            # Обработчик для записи в файл с кодировкой UTF-8
            handler = logging.FileHandler(log_file, encoding='utf-8')
            handler.setLevel(logging.INFO)
            # Формат записи: время - уровень - сообщение
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_action(self, user_id: int, username: str, action: str, details: str = ""):
        """
        Запись произвольного действия пользователя в журнал.

        :param user_id: ID пользователя
        :param username: Логин пользователя
        :param action: Тип действия
        :param details: Дополнительные детали
        """
        log_entry = f"Пользователь: {username} (ID: {user_id}) | Действие: {action} | Детали: {details}"
        self.logger.info(log_entry)

    def log_login(self, username: str, success: bool, ip_address: str = ""):
        """
        Запись попытки входа в систему.

        :param username: Логин пользователя
        :param success: Успешность входа
        :param ip_address: IP-адрес пользователя
        """
        status = "УСПЕХ" if success else "НЕУДАЧА"
        log_entry = f"Попытка входа: {username} | Статус: {status} | IP: {ip_address}"
        self.logger.info(log_entry)

    def log_scan(self, user_id: int, username: str, ip_range: str, ports_count: int):
        """
        Запись запуска сканирования сети.

        :param user_id: ID пользователя
        :param username: Логин пользователя
        :param ip_range: Диапазон IP для сканирования
        :param ports_count: Количество портов
        """
        log_entry = f"Сканирование запущено пользователем {username} (ID: {user_id}) | Диапазон: {ip_range} | Портов: {ports_count}"
        self.logger.info(log_entry)

    def log_export(self, user_id: int, username: str, report_type: str, file_path: str):
        """
        Запись экспорта отчёта.

        :param user_id: ID пользователя
        :param username: Логин пользователя
        :param report_type: Тип отчёта (docx/xlsx)
        :param file_path: Путь к сохранённому файлу
        """
        log_entry = f"Отчёт экспортирован пользователем {username} (ID: {user_id}) | Тип: {report_type} | Путь: {file_path}"
        self.logger.info(log_entry)

    def log_error(self, error_msg: str, context: str = ""):
        """
        Запись ошибки в журнал.

        :param error_msg: Сообщение об ошибке
        :param context: Контекст возникновения ошибки
        """
        log_entry = f"Ошибка: {error_msg} | Контекст: {context}"
        self.logger.error(log_entry)

    def get_log_entries(self, limit: int = 100) -> list:
        """
        Получение последних записей из журнала.

        :param limit: Максимальное количество записей
        :return: Список строк из журнала
        """
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Возвращаем последние N записей
                return lines[-limit:]
        except FileNotFoundError:
            # Если файл журнала не существует, возвращаем пустой список
            return []