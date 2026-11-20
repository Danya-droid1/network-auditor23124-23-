# -*- coding: utf-8 -*-
"""
Модуль аутентификации пользователей.
Реализует проверку паролей через bcrypt-хеширование
и возвращает данные пользователя с его ролью.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт библиотеки bcrypt для безопасного хеширования паролей
import bcrypt

# Импорт менеджера БД и модели пользователя
from src.core.database_manager import DatabaseManager, User


class AuthManager:
    """
    Менеджер аутентификации пользователей.
    Обеспечивает безопасную проверку учётных данных.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализация менеджера аутентификации.

        :param db_manager: Экземпляр DatabaseManager для работы с БД
        """
        self.db = db_manager

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверка соответствия введённого пароля сохранённому хешу.

        :param plain_password: Пароль в открытом виде
        :param hashed_password: Хеш пароля из базы данных
        :return: True если пароли совпадают, False иначе
        """
        # Используем bcrypt для сравнения пароля с хешем
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, username: str, password: str) -> dict:
        """
        Аутентификация пользователя по логину и паролю.

        :param username: Логин пользователя
        :param password: Пароль в открытом виде
        :return: Словарь с данными пользователя или None при ошибке
        """
        # Получаем сессию для работы с БД
        session = self.db.get_session()
        try:
            # Ищем пользователя по логину
            user = session.query(User).filter_by(username=username).first()
            # Проверяем, что пользователь найден и активен
            if user and user.is_active:
                # Проверяем пароль
                if self.verify_password(password, user.password_hash):
                    # Возвращаем данные пользователя
                    return {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role.name if user.role else "unknown",
                        "full_name": user.full_name
                    }
        finally:
            # Обязательно закрываем сессию после работы
            session.close()
        # Возвращаем None, если аутентификация не удалась
        return None

    def hash_password(self, password: str) -> str:
        """
        Генерация bcrypt-хеша для пароля.
        Используется при создании новых пользователей.

        :param password: Пароль в открытом виде
        :return: Хеш пароля в виде строки
        """
        # Генерируем соль для хеширования
        salt = bcrypt.gensalt()
        # Хешируем пароль и преобразуем в строку
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')