# -*- coding: utf-8 -*-
"""
Модуль TCP-сканирования сетевых портов.
Реализует класс PortScanner для проверки открытых портов,
определения имён хостов и типа операционной системы.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля socket для работы с сетевыми соединениями
import socket
# Импорт типов для типизации аргументов
from typing import List, Dict, Tuple
# Импорт модуля datetime для работы с датой и временем
from datetime import datetime


class PortScanner:
    """
    Класс для сканирования сетевых портов.
    Реализует TCP-сканирование, определение имён хостов
    и определение типа ОС по открытым портам.
    """

    def __init__(self, timeout: int = 1):
        """
        Инициализация сканера.

        :param timeout: Таймаут соединения в секундах (по умолчанию 1 сек)
        """
        self.timeout = timeout
        self.is_scanning = False

    def scan_port(self, ip: str, port: int) -> bool:
        """
        Проверка одного порта на IP-адресе.
        Пытается установить TCP-соединение с указанным портом.

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
        except Exception as e:
            print(f"Ошибка при сканировании {ip}:{port} - {e}")
            return False

    def get_service_name(self, port: int) -> str:
        """
        Получение названия сервиса по номеру порта.

        :param port: Номер порта
        :return: Название сервиса или 'Unknown-<порт>'
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
        Получение имени хоста по IP-адресу через обратный DNS-запрос.
        Если имя не удаётся определить, возвращает 'Неизвестно'.

        :param ip: IP-адрес хоста
        :return: Имя хоста или 'Неизвестно'
        """
        try:
            # Выполняем обратный DNS-запрос
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror, OSError):
            # Если имя не найдено или произошла ошибка
            return "Неизвестно"

    def get_os_type(self, open_ports: List[int]) -> str:
        """
        Определение типа операционной системы по открытым портам.
        Эвристический метод, основанный на типичных сервисах ОС.

        :param open_ports: Список открытых портов на хосте
        :return: Тип ОС: 'Windows', 'Linux' или 'Неизвестно'
        """
        # RDP (3389) или SMB (445) характерны для Windows
        if 3389 in open_ports or 445 in open_ports:
            return "Windows"
        # SSH (22) без RDP/SMB обычно указывает на Linux/Unix
        if 22 in open_ports:
            return "Linux"
        # HTTP/HTTPS может быть на любой ОС
        if 80 in open_ports or 443 in open_ports:
            return "Неизвестно"
        return "Неизвестно"

    def scan_host(self, ip: str, ports: List[int]) -> Dict:
        """
        Полное сканирование одного хоста.
        Возвращает информацию об открытых портах, имени хоста и типе ОС.

        :param ip: IP-адрес хоста
        :param ports: Список портов для сканирования
        :return: Словарь с результатами сканирования хоста
        """
        open_ports = []

        # Сканируем все порты
        for port in ports:
            if self.scan_port(ip, port):
                open_ports.append(port)

        # Получаем имя хоста
        hostname = self.get_hostname(ip)

        # Определяем тип ОС
        os_type = self.get_os_type(open_ports)

        # Формируем результат
        result = {
            'ip': ip,
            'hostname': hostname,
            'os_type': os_type,
            'open_ports': open_ports,
            'services': [self.get_service_name(p) for p in open_ports],
            'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return result

    def scan_host_ports(self, ip: str, ports: List[int]) -> List[Dict]:
        """
        Сканирование одного хоста с возвратом списка открытых портов.
        Используется для отображения в таблице результатов.

        :param ip: IP-адрес хоста
        :param ports: Список портов для сканирования
        :return: Список словарей с информацией об открытых портах
        """
        results = []
        for port in ports:
            is_open = self.scan_port(ip, port)
            if is_open:
                result = {
                    'ip': ip,
                    'port': port,
                    'service': self.get_service_name(port),
                    'is_open': True,
                    'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                results.append(result)
        return results

    def stop_scanning(self):
        """Остановка процесса сканирования."""
        self.is_scanning = False