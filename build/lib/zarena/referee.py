# src/zarena/referee.py
from zarena.exceptions import FighterFaintedError, InvalidStatError
from zarena.warriors import ArenaFighter


def safe_attack_round(attacker: ArenaFighter, defender: ArenaFighter) -> str:
    """Orchestre un échange de coups en interceptant les erreurs métier."""
    try:
        damage = attacker.execute_attack()
        defender.take_damage(damage)
    except FighterFaintedError:
        return "Coup impossible : défenseur déjà hors combat."
    except InvalidStatError:
        return "Anomalie de combat : statistiques invalides."
    else:
        return f"Assaut réussi : {damage} dégâts infligés."