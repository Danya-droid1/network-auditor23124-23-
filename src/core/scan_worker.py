# -*- coding: utf-8 -*-
"""
Модуль фонового сканирования сети.
Запускает TCP-сканирование в отдельном потоке,
определяет имена хостов и типы ОС,
отправляет сигналы о прогрессе и результатах.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов для многопоточности в Qt
from PySide6.QtCore import QThread, Signal
# Импорт сканера портов
from src.core.scanner import PortScanner


class ScanWorker(QThread):
    """
    Рабочий поток для выполнения сканирования сети.
    Работает в фоне, не блокируя интерфейс.
    Отправляет сигналы о прогрессе и результатах.
    """

    # Сигнал обновления прогресса (процент, просканировано, всего, найдено)
    progress = Signal(int, int, int, int)
    # Сигнал завершения с результатами
    finished = Signal(list)
    # Сигнал ошибки
    error = Signal(str)

    def __init__(self, ip_range: str, ports: list, timeout: int = 1):
        """
        Инициализация рабочего потока.

        :param ip_range: Диапазон IP для сканирования
        :param ports: Список портов для проверки
        :param timeout: Таймаут соединения в секундах
        """
        super().__init__()
        self.ip_range = ip_range
        self.ports = ports
        self.timeout = timeout
        self.scanner = PortScanner(timeout=timeout)
        self._is_running = True

    def run(self):
        """
        Основной метод потока.
        Выполняет полное сканирование с определением имён и типов ОС.
        """
        try:
            # Парсим базовый IP из диапазона
            base_ip = self.ip_range.split('/')[0]
            ip_parts = base_ip.split('.')

            # Проверяем корректность формата
            if len(ip_parts) != 4:
                self.error.emit("Некорректный формат IP-диапазона")
                return

            # Всего хостов в диапазоне /24
            total_hosts = 254
            scanned_hosts = 0
            all_results = []
            found_devices = 0

            # Перебираем все IP в диапазоне
            for i in range(1, 255):
                # Проверяем флаг остановки
                if not self._is_running:
                    break

                # Формируем IP-адрес
                ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}"

                # Выполняем полное сканирование хоста
                host_result = self.scanner.scan_host(ip, self.ports)

                # Если есть открытые порты - добавляем в результаты
                if host_result['open_ports']:
                    # Распаковываем в формат для таблицы результатов
                    for port in host_result['open_ports']:
                        result = {
                            'ip': ip,
                            'port': port,
                            'service': self.scanner.get_service_name(port),
                            'hostname': host_result['hostname'],
                            'os_type': host_result['os_type'],
                            'is_open': True,
                            'detected_at': host_result['detected_at']
                        }
                        all_results.append(result)
                    found_devices += 1

                # Увеличиваем счётчик просканированных хостов
                scanned_hosts += 1

                # Вычисляем процент прогресса
                percent = int((scanned_hosts / total_hosts) * 100)

                # Отправляем сигнал прогресса с количеством найденных
                self.progress.emit(percent, scanned_hosts, total_hosts, found_devices)

            # По завершении отправляем все результаты
            self.finished.emit(all_results)

        except Exception as e:
            # При ошибке отправляем сигнал с описанием
            self.error.emit(f"Ошибка сканирования: {str(e)}")

    def stop(self):
        """Остановка процесса сканирования."""
        self._is_running = False
        self.scanner.stop_scanning()