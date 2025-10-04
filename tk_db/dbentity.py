"""Database base entity object module."""

from tk_db.models import Base


class DbEntity:
    """Database entity object."""

    def __init__(self, entity: Base):
        self._bc_entity = entity

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code} - {self.id})"

    @property
    def id(self) -> int:
        """Return entity id."""
        return self._bc_entity.id

    @property
    def code(self) -> str:
        """Return asset code."""
        return self._bc_entity.code

    @property
    def name(self) -> str:
        """Return Entity name."""
        name = getattr(self._bc_entity, "name", None)
        if not name:
            name = self._bc_entity.code

        return name

    @property
    def columns(self):
        """Return entity table column names."""
        return self._bc_entity.__table__.columns.keys()
