# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

pillow_hiddenimports = collect_submodules('PIL')
pillow_binaries = collect_dynamic_libs('PIL')

a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=pillow_binaries,
    datas=[
        ('BaseDeDatos.db', '.'),
        ('basura.png', '.'),
        ('borrador.webp', '.'),
        ('Lapiz.png', '.'),
        ('recibido.png', '.'),
        ('Enviado.png', '.'),
        ('contactos.png', '.'),
        ('cuenta.png', '.'),
        ('paisaje-ilustracion-atardecer-en-el-bosque-montanas_3840x2160_xtrafondos.com.jpg', '.'),
    ],
    hiddenimports=[
        'UI',
        'registro',
        'recuperar',
        'Funciones',
        'Clases',
        'bd',
        'app_utils',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        *pillow_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
