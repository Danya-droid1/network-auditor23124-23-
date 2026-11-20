# Author: Golub Daniil Nikolaevich

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                               QPushButton)
from PySide6.QtCore import Qt, QTimer


class ScanProgressWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan in Progress")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.status_label = QLabel("Scanning network...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.details_label = QLabel("Hosts scanned: 0 / 254")
        self.details_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.details_label)

        layout.addSpacing(20)

        self.cancel_btn = QPushButton("Cancel Scan")
        self.cancel_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        self.cancel_btn.clicked.connect(self.cancel_scan)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(500)

    def update_progress(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 5)
            hosts = int((current + 5) / 100 * 254)
            self.details_label.setText(f"Hosts scanned: {hosts} / 254")
        else:
            self.timer.stop()
            self.status_label.setText("Scan completed!")

    def cancel_scan(self):
        self.timer.stop()
        self.status_label.setText("Scan cancelled")
        self.close()