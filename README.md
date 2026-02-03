# SQL to NoSQL Translator Middleware

Este proyecto implementa un middleware capaz de traducir sentencias SQL estándar a consultas nativas para bases de datos NoSQL (específicamente Firebase Realtime Database) en tiempo real.

El sistema fue desarrollado como parte del Trabajo de Titulación de la **Escuela Politécnica Nacional**.

## 🚀 Características Principales

*   **Traducción en Tiempo Real:** Convierte `SELECT`, `INSERT`, `UPDATE` y `DELETE` de SQL a operaciones JSON de Firebase.
*   **Estrategia Híbrida:** Utiliza una combinación de filtrado nativo y procesamiento en memoria para soportar queries complejos (`OR`, `ILIKE`).
*   **Herramienta Educativa:** Muestra el código equivalente en **JavaScript** y **Python** para ayudar a desarrolladores relacionales a aprender paradigmas NoSQL.
*   **Interfaz Moderna:** Frontend construido con Next.js con soporte para modo oscuro, historial y visualización de JSON.

## 🛠️ Stack Tecnológico

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![Firebase](https://img.shields.io/badge/Firebase-Realtime%20Database-orange)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC)

## 🏗️ Arquitectura

El sistema sigue una arquitectura C4 (Component-Based) que desacopla el Parser (Backend) de la Visualización (Frontend).

## 📦 Instalación y Despliegue

Sigue estos pasos para ejecutar el proyecto en tu entorno local.

### Prerrequisitos
*   Python 3.8+
*   Node.js 18+
*   Cuenta de Firebase activa

### 1. Clonar el repositorio
```bash
git clone https://github.com/greyox97/sql-nosql-tic.git
cd sql-nosql-tic
```

### 2. Configurar Backend (Flask)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

Crea un archivo `.env` en `/backend` con tus credenciales:
```env
FIREBASE_CREDENTIALS=ruta/a/tus/credenciales.json
FIREBASE_DB_URL=https://tu-proyecto.firebaseio.com/
```

### 3. Configurar Frontend (Next.js)
```bash
cd ../frontend
npm install
```

### 4. Ejecutar
En dos terminales separadas:

**Backend:**
```bash
python app . py
```

**Frontend:**
```bash
npm run dev
```

Visita `http://localhost:3000` en tu navegador.

---
**Autor:** Sebastián Sánchez  
**Institución:** Escuela Politécnica Nacional  


