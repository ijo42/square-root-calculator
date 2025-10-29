# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller specification file for Square Root Calculator.
Калькулятор квадратного корня - конфигурация сборки.

This file configures how PyInstaller builds the standalone executable.
Этот файл настраивает сборку standalone исполняемого файла.

Usage / Использование:
   Linux/macOS:   uv run pyinstaller square_root_calculator.spec
   Windows:       uv run pyinstaller square_root_calculator.spec
"""

block_cipher = None

a = Analysis(
   ['main.py'],
   pathex=[],
   binaries=[],
   datas=[
       ('src/square_root_calculator', 'square_root_calculator'),
   ],
   hiddenimports=[
       'PyQt6',
       'PyQt6.QtCore',
       'PyQt6.QtGui',
       'PyQt6.QtWidgets',
       'qt_material',
       'square_root_calculator',
       'square_root_calculator.core',
       'square_root_calculator.core.calculator',
       'square_root_calculator.core.history',
       'square_root_calculator.core.settings',
       'square_root_calculator.core.update_checker',
       'square_root_calculator.ui',
       'square_root_calculator.ui.main_window',
       'square_root_calculator.locales',
       'square_root_calculator.locales.translator',
   ],
   hookspath=[],
   hooksconfig={},
   runtime_hooks=[],
   excludes=[],
   win_no_prefer_redirects=False,
   win_private_assemblies=False,
   cipher=block_cipher,
   noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
   pyz,
   a.scripts,
   a.binaries,
   a.zipfiles,
   a.datas,
   [],
   name='SquareRootCalculator',
   debug=False,
   bootloader_ignore_signals=False,
   strip=False,
   upx=True,
   upx_exclude=[],
   runtime_tmpdir=None,
   console=False,  # GUI application, no console window
   disable_windowed_traceback=False,
   argv_emulation=False,
   target_arch=None,
   codesign_identity=None,
   entitlements_file=None,
)