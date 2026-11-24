# -*- coding: utf-8 -*-
# Сервисный слой для работы с пользователями через SQLite.
# Инкапсулирует всю бизнес-логику: аутентификация, CRUD, права доступа.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

import json
import bcrypt
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database_manager import DatabaseManager, User, Role

# Права доступа по ролям
ROLE_PERMISSIONS = {
    'admin': {
        'dashboard': True, 'scan': True, 'results': True, 'assets': True,
        'reports': True, 'vulnerabilities': True, 'settings': True, 'users': True
    },
    'auditor': {
        'dashboard': True, 'scan': True, 'results': True, 'assets': True,
        'reports': True, 'vulnerabilities': True, 'settings': True, 'users': False
    },
    'user': {
        'dashboard': True, 'scan': False, 'results': False, 'assets': False,
        'reports': False, 'vulnerabilities': False, 'settings': False, 'users': False
    }
}

# Тестовые пользователи для инициализации БД
DEFAULT_USERS = [
    {'username': 'admin', 'password': 'AdminSecure2026!', 'role': 'admin', 'full_name': 'Администратор ИБ',
     'email': 'admin@muiv.ru'},
    {'username': 'analyst', 'password': 'AnalystSecure2026!', 'role': 'auditor', 'full_name': 'Аналитик ИБ',
     'email': 'analyst@muiv.ru'},
    {'username': 'auditor', 'password': 'AuditorSecure2026!', 'role': 'auditor', 'full_name': 'Аудитор',
     'email': 'auditor@muiv.ru'},
    {'username': 'user', 'password': 'UserSecure2026!', 'role': 'user', 'full_name': 'Пользователь',
     'email': 'user@muiv.ru'}
]


class UserManager:
    """Сервисный слой для управления пользователями."""

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализация менеджера пользователей.

        :param db_manager: Экземпляр DatabaseManager для работы с БД
        """
        self.db = db_manager

    def initialize_database(self):
        """Инициализация базы данных: создание таблиц и добавление тестовых данных."""
        # Создаём таблицы, если их нет
        self.db.create_tables()

        session = self.db.get_session()
        try:
            # Проверяем, есть ли уже роли
            roles_count = session.query(Role).count()
            if roles_count == 0:
                # Создаём роли (permissions как JSON-строка)
                admin_role = Role(name='admin', description='Администратор ИБ',
                                  permissions=json.dumps(ROLE_PERMISSIONS['admin']))
                auditor_role = Role(name='auditor', description='Аудитор ИБ',
                                    permissions=json.dumps(ROLE_PERMISSIONS['auditor']))
                user_role = Role(name='user', description='Обычный пользователь',
                                 permissions=json.dumps(ROLE_PERMISSIONS['user']))

                session.add_all([admin_role, auditor_role, user_role])
                session.commit()

                # Создаём тестовых пользователей
                for user_data in DEFAULT_USERS:
                    role = session.query(Role).filter_by(name=user_data['role']).first()
                    hashed = self.hash_password(user_data['password'])

                    user = User(
                        username=user_data['username'],
                        password_hash=hashed,
                        role_id=role.id,
                        full_name=user_data['full_name'],
                        email=user_data['email'],
                        is_active=True,
                        created_at=datetime.utcnow()
                    )
                    session.add(user)

                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка инициализации БД: {e}")
            raise
        finally:
            session.close()

    def authenticate(self, username: str, password: str) -> dict:
        """
        Аутентификация пользователя по логину и паролю.

        :param username: Логин пользователя
        :param password: Пароль в открытом виде
        :return: Словарь с данными пользователя или None
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()

            if not user or not user.is_active:
                return None

            # Проверяем пароль через bcrypt
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return None

            # Обновляем время последнего входа
            user.last_login = datetime.utcnow()
            session.commit()

            # Получаем роль и права
            role = session.query(Role).filter_by(id=user.role_id).first()
            # Парсим JSON из текста
            permissions = json.loads(role.permissions) if role and role.permissions else ROLE_PERMISSIONS['user']

            return {
                'id': user.id,
                'username': user.username,
                'role': role.name if role else 'user',
                'full_name': user.full_name,
                'email': user.email,
                'permissions': permissions
            }
        finally:
            session.close()

    def get_all_users(self) -> list:
        """Получение списка всех пользователей."""
        session = self.db.get_session()
        try:
            users = session.query(User).all()
            result = []
            for user in users:
                role = session.query(Role).filter_by(id=user.role_id).first()
                result.append({
                    'id': user.id,
                    'username': user.username,
                    'role': role.name if role else 'user',
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'created_at': user.created_at,
                    'last_login': user.last_login
                })
            return result
        finally:
            session.close()

    def add_user(self, username: str, password: str, role_name: str,
                 full_name: str, email: str) -> bool:
        """Добавление нового пользователя."""
        session = self.db.get_session()
        try:
            existing = session.query(User).filter_by(username=username).first()
            if existing:
                return False

            role = session.query(Role).filter_by(name=role_name).first()
            if not role:
                return False

            user = User(
                username=username,
                password_hash=self.hash_password(password),
                role_id=role.id,
                full_name=full_name,
                email=email,
                is_active=True,
                created_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Ошибка добавления пользователя: {e}")
            return False
        finally:
            session.close()

    def update_user(self, user_id: int, role_name: str = None,
                    full_name: str = None, email: str = None,
                    password: str = None) -> bool:
        """Обновление данных пользователя."""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False

            if full_name is not None:
                user.full_name = full_name
            if email is not None:
                user.email = email
            if password is not None:
                user.password_hash = self.hash_password(password)
            if role_name is not None:
                role = session.query(Role).filter_by(name=role_name).first()
                if role:
                    user.role_id = role.id

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Ошибка обновления пользователя: {e}")
            return False
        finally:
            session.close()

    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя (нельзя удалить admin)."""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False
            if user.username == 'admin':
                return False

            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Ошибка удаления пользователя: {e}")
            return False
        finally:
            session.close()

    def update_profile(self, user_id: int, full_name: str, email: str) -> bool:
        """Обновление профиля текущего пользователя."""
        return self.update_user(user_id, full_name=full_name, email=email)

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Смена пароля с проверкой текущего."""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False

            if not bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return False

            user.password_hash = self.hash_password(new_password)
            session.commit()
            return True
        finally:
            session.close()

    def hash_password(self, password: str) -> str:
        """Хеширование пароля через bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def get_roles(self) -> list:
        """Получение списка всех ролей."""
        session = self.db.get_session()
        try:
            roles = session.query(Role).all()
            return [{'id': r.id, 'name': r.name, 'description': r.description} for r in roles]
        finally:
            session.close()