# -*- coding: utf-8 -*-
"""
Модуль обёрток над QMessageBox для русскоязычных диалогов.
Заменяет стандартные английские тексты кнопок (Yes/No/OK/Cancel)
на русские equivalents (Да/Нет/ОК/Отмена).
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов QMessageBox
from PySide6.QtWidgets import QMessageBox


def info(parent, title: str, text: str):
    """
    Информационный диалог с русской кнопкой "ОК".
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle(title)
    box.setText(text)
    ok_btn = box.addButton("ОК", QMessageBox.AcceptRole)
    box.exec()
    return ok_btn


def warning(parent, title: str, text: str):
    """
    Диалог предупреждения с русской кнопкой "ОК".
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(title)
    box.setText(text)
    ok_btn = box.addButton("ОК", QMessageBox.AcceptRole)
    box.exec()
    return ok_btn


def critical(parent, title: str, text: str):
    """
    Диалог критической ошибки с русской кнопкой "ОК".
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle(title)
    box.setText(text)
    ok_btn = box.addButton("ОК", QMessageBox.AcceptRole)
    box.exec()
    return ok_btn


def question(parent, title: str, text: str) -> bool:
    """
    Диалог подтверждения с русскими кнопками "Да" / "Нет".

    :return: True если нажато "Да", False если "Нет" или закрыто
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Question)
    box.setWindowTitle(title)
    box.setText(text)
    yes_btn = box.addButton("Да", QMessageBox.YesRole)
    no_btn = box.addButton("Нет", QMessageBox.NoRole)
    box.exec()
    return box.clickedButton() is yes_btn