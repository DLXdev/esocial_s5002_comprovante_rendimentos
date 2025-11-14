# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['esocial_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('exemplos/*.xml', 'exemplos'),
        ('exemplos_2025/*.xml', 'exemplos_2025'),
        ('exemplos_csv/*.md', 'exemplos_csv'),
        ('*.md', '.'),
    ],
    hiddenimports=[],
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
    name='esocial_converter',
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
    # Removed invalid icon reference
)