# -*- coding: utf-8 -*-
# Модуль фонового сканирования сети с поддержкой CIDR-масок.
# Запускает TCP-сканирование в отдельном потоке,
# определяет имена хостов и типы ОС,
# отправляет сигналы о прогрессе и результатах.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from PySide6.QtCore import QThread, Signal
import ipaddress
from src.core.scanner import PortScanner


class ScanWorker(QThread):
    """
    Рабочий поток для выполнения сканирования сети.
    Поддерживает CIDR-маски от /32 (1 хост) до /8 (16+ млн хостов).
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

        :param ip_range: Диапазон IP в CIDR-нотации (например, 192.168.1.0/24)
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
        Выполняет полное сканирование с поддержкой CIDR-масок.
        """
        try:
            # Парсим CIDR-диапазон через стандартный модуль ipaddress
            network = ipaddress.ip_network(self.ip_range, strict=False)

            # Получаем все хосты в диапазоне (исключая network и broadcast)
            hosts = list(network.hosts())
            total_hosts = len(hosts)

            if total_hosts == 0:
                self.error.emit("В выбранном диапазоне нет доступных хостов")
                return

            scanned_hosts = 0
            all_results = []
            found_devices = 0

            # Перебираем все IP в диапазоне (не range(1,255)!)
            for ip in hosts:
                # Проверяем флаг остановки
                if not self._is_running:
                    break

                ip_str = str(ip)

                # Выполняем полное сканирование хоста
                host_result = self.scanner.scan_host(ip_str, self.ports)

                # Если есть открытые порты - добавляем в результаты
                if host_result['open_ports']:
                    for port in host_result['open_ports']:
                        result = {
                            'ip': ip_str,
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

                # Отправляем сигнал прогресса
                self.progress.emit(percent, scanned_hosts, total_hosts, found_devices)

            # По завершении отправляем все результаты
            self.finished.emit(all_results)

        except Exception as e:
            self.error.emit(f"Ошибка сканирования: {str(e)}")

    def stop(self):
        """Остановка процесса сканирования."""
        self._is_running = False
        self.scanner.stop_scanning()