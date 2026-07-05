# ECC

Aplicación web didáctica para estudiar criptografía de curva elíptica sobre cuerpos finitos primos. El proyecto separa un `Backend` en Python/FastAPI, encargado de la lógica matemática, y un `Frontend` en React/TypeScript, encargado de la visualización e interacción. También se incluyen las animaciones generadas con Manim y los vídeos finales integrados en la ruta de aprendizaje.

## Estructura

```text
ECC/
├── Backend/
├── Frontend/
├── Animaciones/
├── docker-compose.yml
├── requirements-animaciones.txt
└── README.md
```

Los vídeos finales se encuentran en `Frontend/public/videos/ecc`. La carpeta `Animaciones/media` no se incluye porque es una salida temporal de Manim y puede regenerarse.

## Ejecución con Docker

El modo recomendado de ejecución es Docker Compose:

```powershell
docker compose up --build
```

Servicios:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Documentación OpenAPI: `http://localhost:8000/docs`

Para detener la aplicación:

```powershell
docker compose down
```

## Ejecución local

Backend:

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Frontend, en otra terminal:

```powershell
cd Frontend
npm install
npm run dev
```

## Pruebas

Backend:

```powershell
cd Backend
.\.venv\Scripts\python.exe -m pytest
```

Frontend:

```powershell
cd Frontend
npm run build
```

## Animaciones

Las escenas de Manim están en `Animaciones`. Los vídeos incluidos en el frontend están ya renderizados a 720p/30 fps. Para regenerarlos en Windows:

```powershell
cd Animaciones
.\render_all_ecc.bat
```

Para regenerar una escena concreta:

```powershell
.\render_all_ecc.bat 5
```

En Linux/macOS:

```bash
cd Animaciones
./render_all_ecc.sh
```

Las dependencias de Manim pueden instalarse desde el archivo `requirements-animaciones.txt` situado en la raíz del proyecto. Además de las dependencias de Python, Manim puede requerir una distribución LaTeX instalada para renderizar algunas expresiones matemáticas.
