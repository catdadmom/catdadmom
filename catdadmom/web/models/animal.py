""":mod:`catdadmom.models.animal` --- Animals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Boolean, DateTime, Integer, String

from ...orm import Base


class Animal(Base):
    """CatDadMom animal."""

    #: (:class:`sqlalchemy.types.Integer`) The primary key integer.
    id = Column(Integer, primary_key=True)

    #: (:class:`sqlalchemy.types.String`)
    name = Column(String)

    #: (:class:`sqlalchemy.types.Integer`)
    age = Column(Integer)

    #: (:class:`sqlalchemy.types.Boolean`)
    sex = Column(Boolean)

    #: (:class:`sqlalchemy.types.Boolean`)
    castration = Column(Boolean)

    #: (:class:`sqlalchemy.types.DateTime`) The registered time.
    created_at = deferred(
        Column(DateTime(timezone=True), nullable=False, default=now()),
        group='metadata'
    )

    __tablename__ = 'animals'
