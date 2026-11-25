# src/zarena/exceptions.py


class ZArenaError(Exception):
    """Exception racine : tout incident propre au simulateur hérite d'ici."""

    pass


class InvalidStatError(ZArenaError):
    """Spécialisation : levée lorsqu'une statistique de base est illégale."""

    pass


class FighterFaintedError(ZArenaError):
    """Spécialisation : levée lorsqu'une entité K.-O. tente d'agir ou d'encaisser."""

    pass


class NotEnoughKiError(ZArenaError):
    """Spécialisation : levée lorsqu'une attaque spéciale manque de Ki."""

    pass



#----------------------------------------------------------------------------------

class DataFetchError(ZArenaError):
    """Levée si l'API distante est injoignable ET qu'aucun cache local n'existe."""
    pass