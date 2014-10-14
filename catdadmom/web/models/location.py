""":mod:`catdadmom.models.location` --- Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, Float

from ...orm import Base


class Location(Base):
    """CatDadMom locations."""

    #: (:class:`sqlalchemy.types.Integer`) The primary key integer.
    id = Column(Integer, primary_key=True)

    #: (:class:`sqlalchemy.types.Float`)
    latitude = Column(Float)

    #: (:class:`sqlalchemy.types.Float`)
    longitude = Column(Float)

    #: (:class:`sqlalchemy.orm.relationship`)
    animals = relationship(
        'Animal',
        secondary='animallocation'
    )

    #: (:class:`sqlalchemy.types.DateTime`) The registered time.
    created_at = deferred(
        Column(DateTime(timezone=True), nullable=False, default=now()),
        group='metadata'
    )

    __tablename__ = 'locations'