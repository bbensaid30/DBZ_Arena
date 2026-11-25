# src/zarena/cli.py
import subprocess
import sys
from pathlib import Path


def launch_app() -> None:
    """Lance l'interface web Streamlit (compatible installation standard et éditable)."""
    try:
        import app

        app_path = Path(app.__file__).resolve().parent / "main.py"
    except ImportError:
        app_path = Path.cwd() / "app" / "main.py"

    if not app_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {app_path}. "
            "Vérifiez la présence de app/__init__.py et relancez 'uv pip install -e .'."
        )

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path)],
        check=True,
    )
