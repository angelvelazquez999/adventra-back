# Adventra — Back

## Requisitos 
- Python 

## Instalar Poetry

- Windows (PowerShell):
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verificar:
```bash
poetry --version
```


1. Instalar dependencias con Poetry:
```bash
poetry install
```

## Ejecutar la aplicación
- Abrir shell gestionado por Poetry:
```bash
poetry shell
```
- Ejecutar con Uvicorn (ajuste el módulo de entrada según su proyecto, por ejemplo `app.main:app`):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
O sin activar el shell:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

