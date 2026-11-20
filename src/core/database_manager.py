
"""
PostgreSQL database manager module
Uses SQLAlchemy ORM for data access

Author: Golub Daniil Nikolaevich
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    full_name = Column(String(100))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    last_login = Column(TIMESTAMP)

    role = relationship("Role", back_populates="users")


class NetworkSegment(Base):
    __tablename__ = 'network_segments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    ip_range = Column(String(50))
    segment_type = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))
    ip_address = Column(String(15), nullable=False)
    hostname = Column(String(100))
    os_type = Column(String(50))
    asset_type = Column(String(50))
    is_critical = Column(Boolean, default=False)
    last_scan = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Vulnerability(Base):
    __tablename__ = 'vulnerability_db'

    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    service = Column(String(50))
    risk_level = Column(String(20))
    description = Column(Text)
    cve_id = Column(String(20))
    recommendation = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class ScanTask(Base):
    __tablename__ = 'scan_tasks'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('network_segments.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    ip_range = Column(String(50), nullable=False)
    ports_list = Column(Text)
    status = Column(String(20), default='pending')
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class ScanResult(Base):
    __tablename__ = 'scan_results'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('scan_tasks.id'))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    ip_address = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    is_open = Column(Boolean, default=False)
    service_name = Column(String(50))
    vulnerability_id = Column(Integer, ForeignKey('vulnerability_db.id'))
    detected_at = Column(TIMESTAMP, default=datetime.utcnow)


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    generated_by = Column(Integer, ForeignKey('users.id'))
    report_type = Column(String(50))
    file_path = Column(String(255))
    report_date = Column(TIMESTAMP, default=datetime.utcnow)
    description = Column(Text)


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    details = Column(Text)
    ip_address = Column(String(15))
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)


class SystemSetting(Base):
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True)
    param_name = Column(String(100), unique=True, nullable=False)
    param_value = Column(Text)
    description = Column(Text)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()