# -*- coding: utf-8 -*-
# Модуль TCP-сканирования сетевых портов с поддержкой многопоточности.
# Реализует класс PortScanner для проверки открытых портов,
# определения имён хостов и типа операционной системы.
# Использует ThreadPoolExecutor для ускорения сканирования.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

import socket
from typing import List, Dict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class PortScanner:
    """
    Класс для сканирования сетевых портов.
    Реализует TCP-сканирование с многопоточностью для ускорения.
    """

    def __init__(self, timeout: int = 1, max_workers: int = 50):
        """
        Инициализация сканера.

        :param timeout: Таймаут соединения в секундах
        :param max_workers: Максимальное количество потоков (по умолчанию 50)
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.is_scanning = False

    def scan_port(self, ip: str, port: int) -> bool:
        """
        Проверка одного порта на IP-адресе.

        :param ip: IP-адрес целевого хоста
        :param port: Номер порта для проверки
        :return: True если порт открыт, False иначе
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def get_service_name(self, port: int) -> str:
        """
        Получение названия сервиса по номеру порта.
        """
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Alt'
        }
        return services.get(port, f'Unknown-{port}')

    def get_hostname(self, ip: str) -> str:
        """
        Получение имени хоста через обратный DNS-запрос.
        """
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror, OSError):
            return "Неизвестно"

    def get_os_type(self, open_ports: List[int]) -> str:
        """
        Определение типа ОС по открытым портам (эвристический метод).
        """
        if 3389 in open_ports or 445 in open_ports:
            return "Windows"
        if 22 in open_ports:
            return "Linux"
        return "Неизвестно"

    def _scan_single_port(self, ip: str, port: int) -> Dict:
        """
        Сканирование одного порта. Вспомогательный метод для многопоточности.

        :return: Словарь с результатом или None, если порт закрыт
        """
        if self.scan_port(ip, port):
            return {
                'ip': ip,
                'port': port,
                'service': self.get_service_name(port),
                'is_open': True
            }
        return None

    def scan_host(self, ip: str, ports: List[int]) -> Dict:
        """
        Полное сканирование одного хоста С ИСПОЛЬЗОВАНИЕМ МНОГОПОТОЧНОСТИ.
        Сканирует все порты параллельно, что ускоряет работу в N раз.

        :param ip: IP-адрес хоста
        :param ports: Список портов для сканирования
        :return: Словарь с результатами (открытые порты, имя хоста, тип ОС)
        """
        open_ports = []

        # === МНОГОПОТОЧНОЕ СКНИРОВАНИЕ ===
        # Создаём пул потоков (по умолчанию 50 потоков)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Отправляем все порты на сканирование параллельно
            future_to_port = {
                executor.submit(self._scan_single_port, ip, port): port
                for port in ports
            }

            # Собираем результаты по мере готовности
            for future in as_completed(future_to_port):
                result = future.result()
                if result is not None:
                    open_ports.append(result['port'])

        # Получаем имя хоста и тип ОС
        hostname = self.get_hostname(ip)
        os_type = self.get_os_type(open_ports)

        return {
            'ip': ip,
            'hostname': hostname,
            'os_type': os_type,
            'open_ports': sorted(open_ports),
            'services': [self.get_service_name(p) for p in sorted(open_ports)],
            'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def scan_host_ports(self, ip: str, ports: List[int]) -> List[Dict]:
        """
        Сканирование одного хоста с возвратом списка открытых портов.
        Используется для отображения в таблице результатов.
        """
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_port = {
                executor.submit(self._scan_single_port, ip, port): port
                for port in ports
            }
            for future in as_completed(future_to_port):
                result = future.result()
                if result is not None:
                    result['detected_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results.append(result)
        return results

    def stop_scanning(self):
        """Остановка процесса сканирования."""
        self.is_scanning = False