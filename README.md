# E-Signum Firma Digital para Documentos

Aplicacion web en Python/Flask para gestionar documentos PDF, actas, multiples firmantes, cargos, permisos, auditoria, observaciones y cierre documental.

## Instalacion local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

## Hosting

Revisa [DEPLOY_HOSTING.md](DEPLOY_HOSTING.md).

El archivo de entrada WSGI es:

```text
wsgi:application
```

## Datos

La aplicacion usa SQLite. La ruta puede configurarse con:

```text
ESIGNUM_DB_PATH
```

En este proyecto se incluye la carpeta `data` con base, documentos, imagenes y archivos generados.

## Seguridad

- Usa HTTPS en produccion.
- No publiques la carpeta `data` si el repositorio o hosting quedan publicos.
- Configura `FIRMA_SECRET_KEY` con una clave larga y privada.
- Haz respaldos periodicos de la base de datos y documentos.

