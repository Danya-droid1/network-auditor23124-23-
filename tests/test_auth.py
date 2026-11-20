# -*- coding: utf-8 -*-
"""
Юнит-тесты для класса AuthManager.
Проверяет корректность хеширования и верификации паролей через bcrypt.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля для создания тестов
import unittest
# Импорт тестируемого класса
from src.core.auth import AuthManager


class TestAuthManager(unittest.TestCase):
    """
    Набор тестов для класса AuthManager.
    """

    def test_hash_password(self):
        """Тест генерации хеша пароля."""
        password = "TestPassword123!"
        # Вызываем метод хеширования
        hashed = AuthManager.hash_password(None, password)
        # Результат должен быть строкой
        self.assertIsInstance(hashed, str)
        # Хеш bcrypt всегда начинается с '$2b$'
        self.assertTrue(hashed.startswith("$2b$"))

    def test_verify_password(self):
        """Тест успешной верификации пароля."""
        password = "TestPassword123!"
        # Сначала хешируем пароль
        hashed = AuthManager.hash_password(None, password)
        # Затем проверяем совпадение
        result = AuthManager.verify_password(None, password, hashed)
        # Должно вернуть True
        self.assertTrue(result)

    def test_verify_wrong_password(self):
        """Тест верификации неверного пароля."""
        password = "TestPassword123!"
        # Хешируем правильный пароль
        hashed = AuthManager.hash_password(None, password)
        # Проверяем с неправильным паролем
        result = AuthManager.verify_password(None, "WrongPassword", hashed)
        # Должно вернуть False
        self.assertFalse(result)


# Запуск тестов при прямом выполнении файла
if __name__ == '__main__':
    unittest.main()