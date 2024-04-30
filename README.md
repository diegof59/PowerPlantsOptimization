# PowerPlantsOptimization

Modelo con técnicas de optimización e implementación en MiniZinc para un conjunto de plantas de energía administradas por un proveedor.

## Ejecución

Para ejecutar el modelo, se debe tener instalado MiniZinc (debe estar en el PATH del sistema).

Para ejecutar la aplicación con interfaz gráfica, se usará Python (>=3.6) y un entorno virtual ( llamado y creado en la carpeta oculta .venv). Desde la carpeta root del proyecto, se ejecutan los siguientes comandos:

En Linux:
```sh
python -m venv .venv
source .venv\Scripts\activate
pip install poetry
poetry install
```

En Windows:
```powershell
python -m venv .venv
.venv/Scripts/activate
pip install poetry
poetry install
```

Luego, se ejecuta el script `gui.py` con el siguiente comando:

```sh
python3 gui.py
```

