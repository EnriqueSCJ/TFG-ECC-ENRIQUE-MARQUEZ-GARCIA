# FrontendV2

## Papel dentro del sistema

`FrontendV2` es la interfaz didactica del proyecto. No contiene ya el motor matematico finito de ECC: las operaciones sobre `F_p`, protocolos y ataques se solicitan al backend mediante `src/services/eccService.ts`.

El frontend conserva logica local solo cuando pertenece a la experiencia visual:

- Construccion numerica de la curva real de Weierstrass.
- Seleccion interactiva de puntos sobre la curva real.
- Formateo de puntos y numeros.
- Preparacion de trazas para Plotly.

Esta decision evita dos implementaciones paralelas de ECC y hace que el backend sea la fuente unica de verdad matematica.

## Desarrollo

Desde la raiz del proyecto:

```powershell
cd Proyecto
docker compose up --build
```

El frontend queda disponible en:

```txt
http://localhost:5173
```

En modo Docker, Vite redirige `/api` al servicio `backend` mediante `VITE_BACKEND_URL=http://backend:8000`.

Para ejecutar solo el frontend en local es necesario tener el backend levantado en `http://127.0.0.1:8000`:

```powershell
cd Proyecto\FrontendV2
npm install
npm run dev
```

## Verificacion

```powershell
cd Proyecto\FrontendV2
npm run typecheck
npm run build
```

## Frontera con el backend

La capa `src/services/eccService.ts` centraliza los contratos HTTP:

- `validateCurve`
- `getFinitePoints`
- `addPoints`
- `multiplyPoint`
- `pollardsRho`
- `babyStepGiantStep`
- `audit`
- `simulateEcdh`
- `simulateEcdsa`

Las vistas no llaman directamente a `axios`. Esto mantiene una frontera clara entre UI y transporte.

