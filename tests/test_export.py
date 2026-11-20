# -*- coding: utf-8 -*-
"""
Юнит-тесты для класса ReportExporter.
Проверяет корректность генерации отчётов в форматах DOCX и XLSX.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля для создания тестов
import unittest
# Импорт модуля для работы с файловой системой
import os
# Импорт тестируемого класса
from src.core.export import ReportExporter


class TestReportExporter(unittest.TestCase):
    """
    Набор тестов для класса ReportExporter.
    """

    def setUp(self):
        """
        Метод вызывается перед каждым тестом.
        Создаёт экземпляр экспортёра и тестовые данные.
        """
        # Используем отдельную директорию для тестов
        self.exporter = ReportExporter(output_dir="test_reports")
        # Тестовые данные для отчётов
        self.sample_data = [
            {"ip": "192.168.1.1", "port": 80, "service": "HTTP", "risk": "Низкий"},
            {"ip": "192.168.1.2", "port": 445, "service": "SMB", "risk": "Высокий"}
        ]

    def test_export_to_docx(self):
        """Тест генерации DOCX-отчёта."""
        filepath = self.exporter.export_to_docx(self.sample_data)
        # Файл должен существовать
        self.assertTrue(os.path.exists(filepath))
        # Расширение должно быть .docx
        self.assertTrue(filepath.endswith(".docx"))

    def test_export_to_xlsx(self):
        """Тест генерации XLSX-отчёта."""
        filepath = self.exporter.export_to_xlsx(self.sample_data)
        # Файл должен существовать
        self.assertTrue(os.path.exists(filepath))
        # Расширение должно быть .xlsx
        self.assertTrue(filepath.endswith(".xlsx"))

    def tearDown(self):
        """
        Метод вызывается после каждого теста.
        Удаляет тестовую директорию с отчётами.
        """
        import shutil
        if os.path.exists("test_reports"):
            shutil.rmtree("test_reports")


# Запуск тестов при прямом выполнении файла
if __name__ == '__main__':
    unittest.main()