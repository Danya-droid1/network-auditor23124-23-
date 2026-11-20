@echo off
REM -*- coding: utf-8 -*-
REM Скрипт сборки исполняемого файла Network Auditor для Windows.
REM Запускает PyInstaller с конфигурацией из build.spec.
REM Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

echo ========================================
echo Сборка Network Auditor...
echo ========================================

REM Запуск PyInstaller с очисткой предыдущей сборки
pyinstaller build.spec --clean

REM Проверка результата сборки
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Сборка успешно завершена!
    echo Исполняемый файл: dist\NetworkAuditor.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ОШИБКА: Сборка не удалась!
    echo ========================================
    pause
)