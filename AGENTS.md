# ArchLinuxStudio

Guía de instalación y mantenimiento de un Arch Linux para producción de audio, con scripts para actualizar el sistema y descargar las últimas releases de aplicaciones desde GitHub.

## Visibilidad y rama
- Público (github.com/Toletum/ArchLinuxStudio). Rama por defecto: `main`.
- Descripción en GitHub: "Arch Linux Studio".

## Stack
- Bash para scripts de sistema.
- Python 3 para `update.py`.
- Dependencias (`requirements.txt`): `httpx`, `argparse`, `tqdm`.
  - `argparse` es parte de la librería estándar de Python 3; la entrada en `requirements.txt` no hace falta.

## Estructura
- `README.md`: guía manual (WiFi, zram, PipeWire, RT, Flatpak, yay, AppImages, sink virtual). Es el documento principal.
- `archupdate`: actualiza el sistema (`pacman -Syu`, `yay -Sua`, `flatpak update`), limpia Flatpak y borra paquetes huérfanos.
- `update_gh.sh`: ejecuta `update.py` para JJazzLab (`tar.xz`), LMMS y MuseScore/MuSE (`x86_64.AppImage`).
- `update.py`: consulta `api.github.com/repos/<repo>/releases`, descarga el primer asset que termine en la extensión indicada y guarda el histórico en `downloads_history.db` (SQLite).

## Comandos
```bash
python -m venv venv
./venv/bin/pip install -r requirements.txt
./update_gh.sh
./archupdate
./venv/bin/python update.py "<usuario/repo>" "<extensión>" [-f]
```
- `archupdate` requiere `sudo` y `yay`; no verificado en este entorno.
- Tests: no hay.

## Configuración
- Sin variables de entorno ni ficheros de configuración.
- `update.py` escribe `downloads_history.db` y los ficheros descargados en el directorio actual.

## Convenciones y reglas para agentes
- Ejecutar `update.py` desde la raíz del repo; la base de datos y las descargas se crean en el CWD.
- `*.db` y `/venv/` están en `.gitignore`.
- Los scripts ejecutan comandos con privilegios (`sudo pacman`, `pacman -Rs`). No ejecutarlos sin confirmación del usuario.
- Añadir una app nueva a `update_gh.sh` con el formato `repo extensión`.

## Estado
- Sin tests.
- `archupdate` borra huérfanos con `pacman -Rs` sin confirmación interactiva (`$huerfanos` sin comillas).
- `update.py` captura cualquier excepción y solo la imprime; un fallo no detiene el script con código de error.
- El README contiene datos personales del equipo (usuario, configuración WiFi) y rutas de instalación locales.
