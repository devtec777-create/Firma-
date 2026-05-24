# Sistema de Firma Digital para PDFs

Aplicacion web en Python/Flask para gestionar documentos PDF con multiples firmantes, cargos, permisos, auditoria y cierre automatico cuando todas las firmas requeridas fueron realizadas.

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

## Usuario inicial

Al iniciar por primera vez se crea un super administrador:

- RUT: `99.999.999-9`
- Clave: `Admin12345!`

Cambia esa clave usando el flujo de recuperacion antes de usar el sistema en produccion.

## Funciones incluidas

- Usuarios con nombre, RUT, correo de recuperacion, cargo y codigo interno.
- Cargo por defecto: Bombero.
- Super administrador y administradores.
- Registro historico al otorgar y quitar administradores.
- Tipos de documentos configurables.
- Reglas de firma por cargo y cantidad requerida.
- Permisos por usuario: ver, imprimir, descargar e informe de historial.
- Subida de PDFs por administrador.
- Firma por clave del usuario.
- Codigo numerico aleatorio de firma asociado a usuario y documento.
- Visibilidad del estado de firmas.
- Cierre automatico del documento cuando se completan todas las firmas.
- Generacion de PDF final con todas las firmas estampadas.
- Auditoria no eliminable desde la aplicacion.
- Informe de historial por usuario.
- Recuperacion de contrasena mediante token registrado en auditoria.
- Aviso por correo a los firmantes cuando se les asigna un documento.
- Bandeja de salida para revisar correos enviados, fallidos o no configurados.

## Configuracion de correo SMTP

Si no configuras SMTP, el sistema no puede enviar correos reales y deja los avisos registrados en **Administracion > Bandeja de salida** con estado `not_configured`.

Ejemplo en PowerShell antes de ejecutar:

```powershell
$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="tu-correo@gmail.com"
$env:SMTP_PASSWORD="clave-o-app-password"
$env:SMTP_FROM="tu-correo@gmail.com"
$env:SMTP_TLS="1"
.\.venv\Scripts\python.exe run_app.py 5002
```

Para Gmail normalmente debes usar una **clave de aplicacion**, no la clave normal de la cuenta.

## Nota legal

Este programa implementa una firma interna trazable mediante autenticacion, codigo aleatorio, auditoria y estampado visible en PDF. Para firma electronica avanzada o certificada puede requerirse integracion con certificados digitales, proveedor acreditado o normativa local aplicable.
