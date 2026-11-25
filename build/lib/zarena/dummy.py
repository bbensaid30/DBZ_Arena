# src/zarena/dummy.py


class TrainingDummy:
    """Mannequin d'entraînement doté de points de vie contrôlés."""

    def __init__(self, name: str, max_hp: int) -> None:
        if max_hp <= 0:
            raise ValueError(
                f"Les PV maximaux doivent être > 0 (reçu : {max_hp})"
            )
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp

    def take_hit(self, damage: int) -> None:
        if damage < 0:
            raise ValueError("Les dégâts infligés doivent être positifs.")
        if self.current_hp == 0:
            raise RuntimeError("Le mannequin est déjà pulvérisé !")
        self.current_hp = max(0, self.current_hp - damage)

    def is_broken(self) -> bool:
        return self.current_hp == 0