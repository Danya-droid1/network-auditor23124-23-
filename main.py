
"""
Network Auditor - Network Security Audit System
Main application entry point

Author: Golub Daniil Nikolaevich
Thesis: Development of client-server desktop application
        for auditing open network ports
Version: 1.0
"""

import sys
from PySide6.QtWidgets import QApplication
from src.gui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Network Auditor")
    app.setApplicationVersion("1.0")

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()