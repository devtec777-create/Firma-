# E-Signum - Guia para subir a hosting

## Carpeta de la aplicacion

La aplicacion esta en:

`C:\Users\ceacc\Documents\Codex\2026-05-17\cr-ame-un-programa-en-python`

## Archivos principales

- `app.py`: aplicacion Flask.
- `wsgi.py`: entrada para hosting WSGI.
- `requirements.txt`: dependencias obligatorias.
- `requirements-optional.txt`: dependencias opcionales para transcripcion de audio.
- `data/.sqlite3`: base de datos actual con la informacion del sistema.
- `data/uploads`: PDFs originales.
- `data/signed`: PDFs generados o firmados.
- `data/config_images`: imagenes de configuracion.
- `data/audio`: audios subidos para transcripcion.

## Antes de subir

1. Haz una copia de seguridad de la carpeta `data`.
2. No dejes `data` como carpeta publica del sitio.
3. Configura una clave secreta fija en el hosting:

```bash
FIRMA_SECRET_KEY="una-clave-larga-y-segura"
```

4. Configura la ruta de la base de datos:

```bash
ESIGNUM_DB_PATH="/ruta/privada/firma_digital.sqlite3"
```

En este equipo, la base actual esta en `data/.sqlite3`. Para hosting se recomienda copiarla como `firma_digital.sqlite3` en una carpeta privada y apuntar `ESIGNUM_DB_PATH` a esa ruta.

## Instalacion en hosting Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si usaras transcripcion de audio:

```bash
pip install -r requirements-optional.txt
```

## Comando WSGI recomendado

```bash
gunicorn wsgi:application --bind 0.0.0.0:8000
```

En paneles tipo cPanel, PythonAnywhere, Render, Railway o VPS, configura:

- WSGI callable: `wsgi:application`
- Working directory: carpeta del proyecto
- Python version: 3.11 o superior
- Start command: `gunicorn wsgi:application --bind 0.0.0.0:$PORT`

## Carpetas que deben tener escritura

El usuario del servidor debe poder escribir en:

- `data`
- `data/uploads`
- `data/signed`
- `data/config_images`
- `data/audio`

## SMTP

El SMTP se configura desde el menu `Configuracion`. Si el hosting bloquea salida SMTP, usa un proveedor como SendGrid, Mailgun, Gmail con clave de aplicacion o el SMTP del dominio.

## Seguridad minima

- Usa HTTPS.
- No publiques la carpeta `data`.
- Mantén `FIRMA_SECRET_KEY` fija y privada.
- Haz respaldo periodico de la base SQLite y carpetas de documentos.
- Si el sistema crece mucho, conviene migrar de SQLite a PostgreSQL.

