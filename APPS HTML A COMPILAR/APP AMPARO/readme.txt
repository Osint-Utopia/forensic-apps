			Generador de JSON de Ley de Amparo con Tesis

			Instrucciones:
			1. Instala Python 3, si no lo tienes.
			2. Instala la librería necesaria:
			   pip install python-docx

			3. Coloca estos tres archivos en la misma carpeta:
			   - generar_json_amparo.py
			   - ley de amparo para convinar.docx
			   - tesis de amparo para convinar-.docx

			4. Ejecuta el script desde la terminal:
			   python generar_json_amparo.py

			5. El archivo resultante se llamará:
			   ley_amparo_tesis_completo.json



			Te voy a explicar cómo empacarlo como .exe paso a paso, y también te puedo dejar el comando listo.

			—

			🚨 REQUISITO: Debes tener instalada la herramienta PyInstaller.

			Si ya tienes Python en tu PC, abre la terminal (CMD o PowerShell) y ejecuta:

			bash
			Copiar
			Editar
			pip install pyinstaller
			—

			🧱 Luego, en la carpeta donde tienes el archivo generar_json_amparo.py y los DOCX, corre este comando:

			bash
			Copiar
			Editar
			pyinstaller --onefile --console generar_json_amparo.py
			Esto generará una carpeta /dist con el archivo ejecutable:

			📂 dist/generar_json_amparo.exe

			Ese .exe lo puedes correr haciendo doble clic o desde terminal:

			bash
			Copiar
			Editar
			.\dist\generar_json_amparo.exe
			—