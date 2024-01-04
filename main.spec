# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('energy_audit_app/graphs_data/average_values/*', 'energy_audit_app/graphs_data/average_values'),
        ('energy_audit_app/graphs_data/energy_balance/*', 'energy_audit_app/graphs_data/energy_balance'),
        ('energy_audit_app/graphs_data/specific_values/*', 'energy_audit_app/graphs_data/specific_values')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Energy Audit App',
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
