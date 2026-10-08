# src/zarena/records.py
import json
from pathlib import Path
from zarena.battle import DuelResult


def export_duel_summary(result: DuelResult, filepath: Path | str) -> None:
    """Sauvegarde le bilan d'un affrontement dans un fichier JSON."""
    data = {
        "winner": result.winner.name,
        "loser": result.loser.name,
        "turns": result.turns,
        "remaining_hp": result.remaining_hp,
    }
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)