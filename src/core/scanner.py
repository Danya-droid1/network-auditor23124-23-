"""
Network port scanning module
Implements TCP port scanning functionality

Author: Golub Daniil Nikolaevich
"""

import socket
from typing import List, Dict
from datetime import datetime


class PortScanner:
    def __init__(self, timeout: int = 1):
        self.timeout = timeout
        self.is_scanning = False

    def scan_port(self, ip: str, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception as e:
            print(f"Scan error {ip}:{port} - {e}")
            return False

    def get_service_name(self, port: int) -> str:
        # Well-known ports mapping
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Alt'
        }
        return services.get(port, f'Unknown-{port}')

    def scan_host(self, ip: str, ports: List[int]) -> List[Dict]:
        results = []
        for port in ports:
            is_open = self.scan_port(ip, port)
            if is_open:
                result = {
                    'ip': ip,
                    'port': port,
                    'service': self.get_service_name(port),
                    'is_open': True,
                    'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                results.append(result)
        return results

    def stop_scanning(self):
        self.is_scanning = False