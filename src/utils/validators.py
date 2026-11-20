# -*- coding: utf-8 -*-
"""
Модуль валидаторов входных данных.
Содержит статические методы для проверки IP-адресов, портов,
логинов и паролей на корректность.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля регулярных выражений
import re
# Импорт типа Tuple для возврата кортежей (результат, сообщение)
from typing import Tuple


class Validators:
    """
    Класс-коллекция статических методов валидации.
    Все методы возвращают кортеж (bool, str):
    (результат проверки, сообщение об ошибке или успехе)
    """

    @staticmethod
    def validate_ip_range(ip_range: str) -> Tuple[bool, str]:
        """
        Проверка корректности формата IP-диапазона в нотации CIDR.

        :param ip_range: Строка вида '192.168.1.0/24'
        :return: Кортеж (успех, сообщение)
        """
        # Регулярное выражение для проверки формата IP/CIDR
        pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
        if not re.match(pattern, ip_range):
            return False, "Некорректный формат IP-диапазона"

        # Извлекаем базовый IP-адрес
        base_ip = ip_range.split('/')[0]
        parts = base_ip.split('.')

        # Проверяем, что каждая часть IP находится в диапазоне 0-255
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False, "Части IP-адреса должны быть в диапазоне от 0 до 255"

        # Проверяем маску CIDR (0-32)
        if '/' in ip_range:
            mask = int(ip_range.split('/')[1])
            if not 0 <= mask <= 32:
                return False, "Маска CIDR должна быть в диапазоне от 0 до 32"

        return True, "IP-диапазон корректен"

    @staticmethod
    def validate_port(port: int) -> Tuple[bool, str]:
        """
        Проверка корректности номера порта.

        :param port: Номер порта для проверки
        :return: Кортеж (успех, сообщение)
        """
        # Порт должен быть в диапазоне 1-65535
        if not 1 <= port <= 65535:
            return False, "Порт должен быть в диапазоне от 1 до 65535"
        return True, "Порт корректен"

    @staticmethod
    def validate_ports_list(ports_str: str) -> Tuple[bool, str]:
        """
        Проверка строки со списком портов через запятую.

        :param ports_str: Строка вида '80, 443, 3389'
        :return: Кортеж (успех, сообщение)
        """
        try:
            # Разбиваем строку и преобразуем в числа
            ports = [int(p.strip()) for p in ports_str.split(',')]
            # Проверяем каждый порт
            for port in ports:
                valid, msg = Validators.validate_port(port)
                if not valid:
                    return False, msg
            return True, "Список портов корректен"
        except ValueError:
            return False, "Порты должны быть целыми числами, разделёнными запятыми"

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Проверка корректности логина пользователя.

        :param username: Логин для проверки
        :return: Кортеж (успех, сообщение)
        """
        # Логин должен содержать минимум 3 символа
        if len(username) < 3:
            return False, "Логин должен содержать минимум 3 символа"
        # Разрешены только латинские буквы, цифры и подчёркивания
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Логин может содержать только буквы, цифры и подчёркивания"
        return True, "Логин корректен"

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Проверка надёжности пароля.

        :param password: Пароль для проверки
        :return: Кортеж (успех, сообщение)
        """
        # Пароль должен содержать минимум 8 символов
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"
        # Обязательна хотя бы одна заглавная буква
        if not re.search(r'[A-Z]', password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"
        # Обязательна хотя бы одна строчная буква
        if not re.search(r'[a-z]', password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"
        # Обязательна хотя бы одна цифра
        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        return True, "Пароль соответствует требованиям безопасности"