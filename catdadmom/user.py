""":mod:`catdadmom.user` --- Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from sqlalchemy.orm import deferred
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Boolean, DateTime, Integer, String, Unicode


from .orm import Base


class User(Base):
    """CatDadMom users."""

    #: (:class:`sqlalchemy.types.Integer`) The primary key integer.
    id = Column(Integer, primary_key=True)

    #: (:class:`sqlalchemy.types.String`) The login name.
    login = Column(String, nullable=False, unique=True)

    #: (:class:`sqlalchemy.types.String`) The hashed password.
    password_hash = deferred(Column(String, nullable=False))

    #: (:class:`sqlalchemy.types.Unicode`) The email address.
    email = Column(Unicode, nullable=False, unique=True)

    #: (:class:`sqlalchemy.types.DateTime`) The time :attr:`email` is verified.
    email_verified_at = deferred(
        Column(DateTime(timezone=True), default=None),
        group='metadata'
    )

    #: (:class:`sqlalchemy.types.Boolean`) ``True`` if the user is an admin.
    admin = deferred(
        Column(Boolean, nullable=False, default=False, server_default=false()),
        group='metadata'
    )

    #: (:class:`sqlalchemy.types.DateTime`) The registered time.
    created_at = deferred(
        Column(DateTime(timezone=True), nullable=False, default=now()),
        group='metadata'
    )

    __tablename__ = 'users'
