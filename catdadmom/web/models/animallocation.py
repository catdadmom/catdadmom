""":mod:`catdadmom.models.animallocation` --- AnimalLocations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer

from ...orm import Base


class AnimalLocation(Base):
    """CatDadMom animallocation."""

    #: (:class:`sqlalchemy.types.Integer`)
    animal_id = Column(Integer, ForeignKey('animals.id'), primary_key=True)

    #: (:class:`sqlalchemy.types.Integer`)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)

    #: (:class:`sqlalchemy.orm.relationship`)
    animal = relationship('Animal', backref=backref('animal_assoc'))

    #: (:class:`sqlalchemy.orm.relationship`)
    location = relationship('Location', backref=backref('location_assoc'))

    #: (:class:`sqlalchemy.types.DateTime`) The registered time.
    created_at = deferred(
        Column(DateTime(timezone=True), nullable=False, default=now()),
        group='metadata'
    )

    __tablename__ = 'animallocation'