# -*- mode: python ; coding: utf-8 -*-
import os
import platform

from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE
from dotenv import load_dotenv

load_dotenv()

block_cipher = None
application_name = os.getenv('APP_NAME')
application_id = os.getenv('APP_ID')
icon_file = 'src/data/images/icon'
icon_extension = '.icns' if platform.system() == 'Darwin' else '.ico'
icon_compiled_file = f"{icon_file}{icon_extension}"

a = Analysis(['src/main.py'],
             pathex=['./'],
             binaries=[],
             datas=[
                 ('.env', '.'),
                 (icon_compiled_file, '.'),
             ],
             hiddenimports=[
                 "pkg_resources.py2_warn"
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=application_name,
          debug=False,
          bootloader_ignore_signals=False,
          icon=icon_compiled_file,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=application_name)

app = BUNDLE(coll,
             name=f"{application_name}.app",
             icon=icon_compiled_file,
             bundle_identifier=application_id,
             info_plist={
                 'NSPrincipalClass': 'NSApplication',
                 'NSAppleScriptEnabled': False,
             })
