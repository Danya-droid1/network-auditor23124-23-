# -*- coding: utf-8 -*-
"""
Слой интеграции между графическим интерфейсом и ядром приложения.
Связывает сканер, базу данных и экспорт отчётов в единый workflow.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт сканера портов
from src.core.scanner import PortScanner
# Импорт менеджера БД и моделей задач/результатов
from src.core.database_manager import DatabaseManager, ScanResult, ScanTask
# Импорт экспортёра отчётов
from src.core.export import ReportExporter
# Импорт логгера аудита
from src.utils.logger import AuditLogger
# Импорт модуля datetime для временных меток
from datetime import datetime


class IntegrationLayer:
    """
    Класс-посредник между GUI и ядром.
    Координирует работу сканера, БД, экспорта и логгера.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализация слоя интеграции.

        :param db_manager: Экземпляр DatabaseManager для работы с БД
        """
        self.db = db_manager
        self.scanner = PortScanner()
        self.exporter = ReportExporter()
        self.logger = AuditLogger()

    def execute_scan(self, user_id: int, username: str, ip_range: str, ports: list) -> list:
        """
        Выполнение полного цикла сканирования:
        1. Логирование начала сканирования
        2. Создание задачи в БД
        3. Запуск сканера
        4. Сохранение результатов
        5. Обновление статуса задачи

        :param user_id: ID пользователя, запустившего сканирование
        :param username: Логин пользователя
        :param ip_range: Диапазон IP для сканирования
        :param ports: Список портов для проверки
        :return: Список результатов сканирования
        """
        # Логируем запуск сканирования
        self.logger.log_scan(user_id, username, ip_range, len(ports))

        # Получаем сессию для работы с БД
        session = self.db.get_session()
        try:
            # Создаём новую задачу сканирования
            task = ScanTask(
                created_by=user_id,
                ip_range=ip_range,
                ports_list=",".join(map(str, ports)),
                status="в процессе",
                started_at=datetime.now()
            )
            session.add(task)
            session.commit()
            task_id = task.id

            # Запускаем сканирование диапазона
            results = self.scanner.scan_range(ip_range, ports)

            # Сохраняем каждый результат в БД
            for result in results:
                scan_result = ScanResult(
                    task_id=task_id,
                    ip_address=result['ip'],
                    port=result['port'],
                    is_open=True,
                    service_name=result['service']
                )
                session.add(scan_result)

            # Обновляем статус задачи на "завершено"
            task.status = "завершено"
            task.completed_at = datetime.now()
            session.commit()

            return results
        except Exception as e:
            # При ошибке логируем и откатываем транзакцию
            self.logger.log_error(str(e), "execute_scan")
            session.rollback()
            return []
        finally:
            # Обязательно закрываем сессию
            session.close()

    def export_results(self, user_id: int, username: str, results: list, format: str = "docx") -> str:
        """
        Экспорт результатов сканирования в файл.

        :param user_id: ID пользователя
        :param username: Логин пользователя
        :param results: Список результатов сканирования
        :param format: Формат файла ('docx' или 'xlsx')
        :return: Путь к созданному файлу
        """
        # Выбираем метод экспорта в зависимости от формата
        if format == "docx":
            filepath = self.exporter.export_to_docx(results)
        else:
            filepath = self.exporter.export_to_xlsx(results)

        # Логируем факт экспорта
        self.logger.log_export(user_id, username, format, filepath)
        return filepath