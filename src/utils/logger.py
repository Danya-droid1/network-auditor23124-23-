# Author: Golub Daniil Nikolaevich

import logging
from datetime import datetime
from typing import Optional


class AuditLogger:
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.logger = logging.getLogger('NetworkAuditor')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.FileHandler(log_file, encoding='utf-8')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_action(self, user_id: int, username: str, action: str, details: str = ""):
        log_entry = f"User: {username} (ID: {user_id}) | Action: {action} | Details: {details}"
        self.logger.info(log_entry)

    def log_login(self, username: str, success: bool, ip_address: str = ""):
        status = "SUCCESS" if success else "FAILED"
        log_entry = f"Login attempt: {username} | Status: {status} | IP: {ip_address}"
        self.logger.info(log_entry)

    def log_scan(self, user_id: int, username: str, ip_range: str, ports_count: int):
        log_entry = f"Scan initiated by {username} (ID: {user_id}) | Range: {ip_range} | Ports: {ports_count}"
        self.logger.info(log_entry)

    def log_export(self, user_id: int, username: str, report_type: str, file_path: str):
        log_entry = f"Report exported by {username} (ID: {user_id}) | Type: {report_type} | Path: {file_path}"
        self.logger.info(log_entry)

    def log_error(self, error_msg: str, context: str = ""):
        log_entry = f"Error: {error_msg} | Context: {context}"
        self.logger.error(log_entry)

    def get_log_entries(self, limit: int = 100) -> list:
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-limit:]
        except FileNotFoundError:
            return []