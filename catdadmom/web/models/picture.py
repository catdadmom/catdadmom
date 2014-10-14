""":mod:`catdadmom.models.picture` --- Pictures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import deferred, relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String

from ...orm import Base
from .animal import Animal


class Picture(Base):
    """CatDadMom picture."""

    #: (:class:`sqlalchemy.types.Integer`) The primary key integer.
    id = Column(Integer, primary_key=True)

    #: (:class:`sqlalchemy.types.String`)
    title = Column(String)

    #: (:class:`sqlalchemy.types.Integer`)
    animal_id = Column(Integer, ForeignKey('animals.id'))

    #: (:class:`sqlalchemy.orm.relationship`)
    animal = relationship(
        Animal,
        backref=backref('pictures', uselist=True, cascade='delete,all')
    )

    #: (:class:`sqlalchemy.types.DateTime`) The registered time.
    created_at = deferred(
        Column(DateTime(timezone=True), nullable=False, default=now()),
        group='metadata'
    )

    __tablename__ = 'pictures'
