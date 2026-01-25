# Middleware SQL → Firebase (Clave-Valor)

Este proyecto implementa un middleware que recibe consultas SQL (`INSERT`, `SELECT`, `DELETE`) y las traduce a operaciones sobre Firebase Realtime Database, usando Python y Flask.

## 🔧 Estructura
- **app.py**: Punto de entrada (Flask)
- **routes.py**: Ruta `/consulta` para recibir SQL
- **controllers/**: Controladores que procesan la consulta
- **services/**: Traducción y ejecución de la consulta
- **database/**: Cliente para Firebase
- **utils/**: Traducción SQL → KV con `sqlparse`

## ▶️ Uso
1. Coloca tu `credenciales-firebase.json` en la raíz
2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta:
   ```
   python app.py
   ```
4. Envia consultas tipo:
   ```json
   POST /consulta
   { "sql": "SELECT * FROM usuarios WHERE id = 101;" }
   ```
