import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',                    # Archivo principal
    '--windowed',                 # Evita abrir consola (GUI)
    '--paths=pages',              # Carpetas con módulos adicionales
    '--paths=utils',
    '--add-data=images:images',
    '--name=NefertariVideos'      # Nombre final de la app (.app)
])
