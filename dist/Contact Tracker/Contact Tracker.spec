from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Contact Tracker.py'],
             pathex=['C:\\Users\\radio\\Contact Tracker - by Ben Hume and Ethan Corbett'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('Code\Contact Tracker.kv',
'C:\\Users\\radio\\Contact Tracker - by Ben Hume and Ethan Corbett\Contact Tracker.kv',
'DATA')]

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Contact Tracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
Tree('C:\\Users\\radio\\Contact Tracker - by Ben Hume and Ethan Corbett\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in
               (sdl2.dep_bins +
               glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Contact Tracker')
