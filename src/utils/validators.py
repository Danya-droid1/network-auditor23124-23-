# Author: Golub Daniil Nikolaevich

import re
from typing import Tuple


class Validators:
    @staticmethod
    def validate_ip_range(ip_range: str) -> Tuple[bool, str]:
        pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
        if not re.match(pattern, ip_range):
            return False, "Invalid IP range format"

        base_ip = ip_range.split('/')[0]
        parts = base_ip.split('.')

        for part in parts:
            if not 0 <= int(part) <= 255:
                return False, "IP address parts must be between 0 and 255"

        if '/' in ip_range:
            mask = int(ip_range.split('/')[1])
            if not 0 <= mask <= 32:
                return False, "CIDR mask must be between 0 and 32"

        return True, "Valid IP range"

    @staticmethod
    def validate_port(port: int) -> Tuple[bool, str]:
        if not 1 <= port <= 65535:
            return False, "Port must be between 1 and 65535"
        return True, "Valid port"

    @staticmethod
    def validate_ports_list(ports_str: str) -> Tuple[bool, str]:
        try:
            ports = [int(p.strip()) for p in ports_str.split(',')]
            for port in ports:
                valid, msg = Validators.validate_port(port)
                if not valid:
                    return False, msg
            return True, "Valid ports list"
        except ValueError:
            return False, "Ports must be comma-separated integers"

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, "Valid username"

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        return True, "Valid password"