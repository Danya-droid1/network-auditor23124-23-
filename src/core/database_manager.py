# -*- coding: utf-8 -*-
# Менеджер работы с базой данных SQLite.
# Содержит ORM-модели SQLAlchemy для портативного хранения данных.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class Role(Base):
    """Модель таблицы ролей пользователей."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON как текст (SQLite не поддерживает JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")


class User(Base):
    """Модель таблицы пользователей."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    full_name = Column(String(100))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    role = relationship("Role", back_populates="users")


class NetworkSegment(Base):
    """Модель таблицы сегментов сети."""
    __tablename__ = 'network_segments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    ip_range = Column(String(50))
    segment_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class Asset(Base):
    """Модель таблицы сетевых активов."""
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))
    ip_address = Column(String(15), nullable=False)
    hostname = Column(String(100))
    os_type = Column(String(50))
    asset_type = Column(String(50))
    is_critical = Column(Boolean, default=False)
    last_scan = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Vulnerability(Base):
    """Модель таблицы базы уязвимостей."""
    __tablename__ = 'vulnerability_db'

    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    service = Column(String(50))
    risk_level = Column(String(20))
    description = Column(Text)
    cve_id = Column(String(20))
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanTask(Base):
    """Модель таблицы задач сканирования."""
    __tablename__ = 'scan_tasks'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    ip_range = Column(String(50), nullable=False)
    ports_list = Column(Text)
    status = Column(String(20), default='pending')
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanResult(Base):
    """Модель таблицы результатов сканирования."""
    __tablename__ = 'scan_results'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('scan_tasks.id'))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    ip_address = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    is_open = Column(Boolean, default=False)
    service_name = Column(String(50))
    vulnerability_id = Column(Integer, ForeignKey('vulnerability_db.id'))
    detected_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    """Модель таблицы отчётов."""
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    generated_by = Column(Integer, ForeignKey('users.id'))
    report_type = Column(String(50))
    file_path = Column(String(255))
    report_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)


class AuditLog(Base):
    """Модель таблицы журнала аудита."""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    details = Column(Text)
    ip_address = Column(String(15))
    timestamp = Column(DateTime, default=datetime.utcnow)


class SystemSetting(Base):
    """Модель таблицы настроек системы."""
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True)
    param_name = Column(String(100), unique=True, nullable=False)
    param_value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Менеджер для работы с базой данных SQLite."""

    def __init__(self, db_url: str):
        """
        Инициализация менеджера БД.

        :param db_url: URL для подключения к БД (sqlite:///path/to/db)
        """
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Создание всех таблиц в базе данных."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Получение новой сессии для работы с БД."""
        return self.Session()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.engine.dispose()