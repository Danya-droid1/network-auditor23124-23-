# -*- coding: utf-8 -*-
"""
Юнит-тесты для класса PortScanner.
Проверяет корректность работы методов сканирования портов
и определения названий сервисов.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля для создания тестов
import unittest
# Импорт тестируемого класса
from src.core.scanner import PortScanner


class TestPortScanner(unittest.TestCase):
    """
    Набор тестов для класса PortScanner.
    """

    def setUp(self):
        """
        Метод вызывается перед каждым тестом.
        Создаёт экземпляр сканера с таймаутом 1 секунда.
        """
        self.scanner = PortScanner(timeout=1)

    def test_scan_port_open(self):
        """Тест проверки порта на localhost."""
        result = self.scanner.scan_port("127.0.0.1", 80)
        # Результат должен быть булевым значением
        self.assertIsInstance(result, bool)

    def test_get_service_name(self):
        """Тест определения названия сервиса по порту."""
        # Проверяем известные порты
        self.assertEqual(self.scanner.get_service_name(80), "HTTP")
        self.assertEqual(self.scanner.get_service_name(443), "HTTPS")
        self.assertEqual(self.scanner.get_service_name(22), "SSH")
        self.assertEqual(self.scanner.get_service_name(21), "FTP")

    def test_get_service_name_unknown(self):
        """Тест обработки неизвестного порта."""
        # Для неизвестного порта должен возвращаться шаблон 'Unknown-<порт>'
        result = self.scanner.get_service_name(9999)
        self.assertEqual(result, "Unknown-9999")

    def test_scan_host(self):
        """Тест сканирования хоста по списку портов."""
        results = self.scanner.scan_host("127.0.0.1", [80, 443])
        # Результат должен быть списком
        self.assertIsInstance(results, list)

    def test_stop_scanning(self):
        """Тест остановки процесса сканирования."""
        # Устанавливаем флаг сканирования
        self.scanner.is_scanning = True
        # Вызываем метод остановки
        self.scanner.stop_scanning()
        # Проверяем, что флаг сброшен
        self.assertFalse(self.scanner.is_scanning)


# Запуск тестов при прямом выполнении файла
if __name__ == '__main__':
    unittest.main()