from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import attacks, ecc, protocols

app = FastAPI(
    title="ECC Didactico API",
    version="1.0.0",
    description=(
        "API canónica para el cálculo algebraico de curvas elípticas "
        "sobre cuerpos primos pequeños."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Parámetros de entrada no válidos.",
            "errors": exc.errors(),
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(ecc.router)
app.include_router(attacks.router)
app.include_router(protocols.router)
