# -*- mode: python ; coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Конфигурационный файл PyInstaller для сборки .exe
# Содержит настройки сборки исполняемого файла Network Auditor.
# Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23

block_cipher = None

# Анализ зависимостей проекта
a = Analysis(
    ['main.py'],                          # Точка входа
    pathex=[],
    binaries=[],
    datas=[],
    # Скрытые импорты, которые PyInstaller может не обнаружить
    hiddenimports=['PySide6', 'sqlalchemy', 'psycopg2', 'docx', 'openpyxl', 'bcrypt'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Создание архива Python-файлов
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Создание исполняемого файла
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NetworkAuditor',                # Имя выходного файла
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                             # Сжатие UPX для уменьшения размера
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                        # Без консольного окна (GUI-приложение)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)