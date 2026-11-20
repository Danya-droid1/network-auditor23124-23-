# -*- coding: utf-8 -*-
"""
Менеджер работы с базой данных PostgreSQL.
Содержит ORM-модели SQLAlchemy для 10 таблиц:
roles, users, network_segments, assets, vulnerability_db,
scan_tasks, scan_results, reports, audit_logs, system_settings.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов SQLAlchemy для работы с БД
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Импорт модуля datetime для работы с временными метками
from datetime import datetime

# Создаём базовый класс для всех ORM-моделей
Base = declarative_base()


class Role(Base):
    """
    ORM-модель таблицы ролей пользователей.
    Хранит информацию о ролях: admin, analyst, auditor.
    """
    __tablename__ = 'roles'  # Имя таблицы в БД

    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String(50), unique=True, nullable=False)  # Название роли (уникальное)
    description = Column(Text)  # Описание роли
    permissions = Column(JSON)  # Права доступа в формате JSON
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # Дата создания

    # Связь с пользователями (один ко многим)
    users = relationship("User", back_populates="role")


class User(Base):
    """
    ORM-модель таблицы пользователей.
    Хранит учётные данные и информацию о пользователях системы.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # Первичный ключ
    username = Column(String(50), unique=True, nullable=False)  # Логин (уникальный)
    password_hash = Column(String(255), nullable=False)  # Хеш пароля (bcrypt)
    role_id = Column(Integer, ForeignKey('roles.id'))  # Внешний ключ на таблицу ролей
    full_name = Column(String(100))  # ФИО пользователя
    email = Column(String(100))  # Email пользователя
    is_active = Column(Boolean, default=True)  # Флаг активности учётной записи
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # Дата создания
    last_login = Column(TIMESTAMP)  # Дата последнего входа

    # Связь с ролью пользователя
    role = relationship("Role", back_populates="users")


class NetworkSegment(Base):
    """
    ORM-модель таблицы сегментов сети.
    Хранит информацию о логических сегментах сети университета.
    """
    __tablename__ = 'network_segments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Название сегмента
    description = Column(Text)  # Описание сегмента
    ip_range = Column(String(50))  # Диапазон IP-адресов (например, 192.168.1.0/24)
    segment_type = Column(String(50))  # Тип сегмента: admin, education, branch, guest
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Asset(Base):
    """
    ORM-модель таблицы сетевых активов.
    Хранит информацию о серверах, рабочих станциях и другом оборудовании.
    """
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))  # Связь с сегментом
    ip_address = Column(String(15), nullable=False)  # IP-адрес актива
    hostname = Column(String(100))  # Имя хоста
    os_type = Column(String(50))  # Тип операционной системы
    asset_type = Column(String(50))  # Тип актива: server, workstation, printer
    is_critical = Column(Boolean, default=False)  # Флаг критичности актива
    last_scan = Column(TIMESTAMP)  # Дата последнего сканирования
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Vulnerability(Base):
    """
    ORM-модель таблицы базы уязвимостей.
    Хранит информацию об известных уязвимостях сетевых портов.
    """
    __tablename__ = 'vulnerability_db'

    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)  # Номер порта
    service = Column(String(50))  # Название сервиса
    risk_level = Column(String(20))  # Уровень риска: Low, Medium, High, Critical
    description = Column(Text)  # Описание уязвимости
    cve_id = Column(String(20))  # Идентификатор CVE (если есть)
    recommendation = Column(Text)  # Рекомендации по устранению
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class ScanTask(Base):
    """
    ORM-модель таблицы задач сканирования.
    Хранит информацию о запущенных задачах сканирования.
    """
    __tablename__ = 'scan_tasks'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))  # Целевой сегмент
    created_by = Column(Integer, ForeignKey('users.id'))  # Кто создал задачу
    ip_range = Column(String(50), nullable=False)  # Диапазон IP для сканирования
    ports_list = Column(Text)  # Список портов через запятую
    status = Column(String(20), default='pending')  # Статус: pending, in_progress, completed
    started_at = Column(TIMESTAMP)  # Время начала сканирования
    completed_at = Column(TIMESTAMP)  # Время завершения
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class ScanResult(Base):
    """
    ORM-модель таблицы результатов сканирования.
    Хранит информацию об обнаруженных открытых портах.
    """
    __tablename__ = 'scan_results'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('scan_tasks.id'))  # Связь с задачей
    asset_id = Column(Integer, ForeignKey('assets.id'))  # Связь с активом
    ip_address = Column(String(15), nullable=False)  # IP-адрес
    port = Column(Integer, nullable=False)  # Номер порта
    is_open = Column(Boolean, default=False)  # Открыт ли порт
    service_name = Column(String(50))  # Название сервиса
    vulnerability_id = Column(Integer, ForeignKey('vulnerability_db.id'))  # Связь с уязвимостью
    detected_at = Column(TIMESTAMP, default=datetime.utcnow)  # Время обнаружения


class Report(Base):
    """
    ORM-модель таблицы отчётов.
    Хранит информацию о сгенерированных отчётах.
    """
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    generated_by = Column(Integer, ForeignKey('users.id'))  # Кто сгенерировал
    report_type = Column(String(50))  # Тип отчёта: docx, xlsx
    file_path = Column(String(255))  # Путь к файлу отчёта
    report_date = Column(TIMESTAMP, default=datetime.utcnow)  # Дата создания
    description = Column(Text)  # Описание отчёта


class AuditLog(Base):
    """
    ORM-модель таблицы журнала аудита.
    Хранит информацию о действиях пользователей в системе.
    """
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Кто выполнил действие
    action = Column(String(100), nullable=False)  # Тип действия
    details = Column(Text)  # Детали действия
    ip_address = Column(String(15))  # IP-адрес пользователя
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)  # Время действия


class SystemSetting(Base):
    """
    ORM-модель таблицы настроек системы.
    Хранит параметры конфигурации приложения.
    """
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True)
    param_name = Column(String(100), unique=True, nullable=False)  # Название параметра
    param_value = Column(Text)  # Значение параметра
    description = Column(Text)  # Описание параметра
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)  # Время последнего обновления


class DatabaseManager:
    """
    Менеджер для работы с базой данных PostgreSQL.
    Предоставляет методы для создания таблиц и получения сессий.
    """

    def __init__(self, db_url: str):
        """
        Инициализация менеджера БД.

        :param db_url: URL для подключения к БД
                       (например, postgresql://user:pass@localhost/dbname)
        """
        # Создаём движок SQLAlchemy
        self.engine = create_engine(db_url)
        # Создаём фабрику сессий
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """
        Создание всех таблиц в базе данных.
        Выполняет SQL-команды CREATE TABLE для всех ORM-моделей.
        """
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Получение новой сессии для работы с БД.

        :return: Экземпляр Session для выполнения запросов
        """
        return self.Session()

    def close(self):
        """
        Закрытие соединения с базой данных.
        Освобождает ресурсы, связанные с подключением.
        """
        self.engine.dispose()