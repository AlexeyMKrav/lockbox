import uuid

from sqlalchemy import ForeignKey, LargeBinary, Table, Column, BINARY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BINARY

from src.db.database import Base

userGroup_table = Table(
    'user_group',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
    extend_existing=True,
)

userRole_table = Table(
    'user_role',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    extend_existing=True,
)


class DbUser(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    displayName: Mapped[str]
    certificates: Mapped[list['DbCertificate']] = relationship(back_populates='user')
    groups: Mapped[list['DbGroup']] = relationship(secondary=userGroup_table, back_populates='users')
    roles: Mapped[list['DbRole']] = relationship(secondary=userGroup_table, back_populates='users')


class DbCertificate(Base):
    __tablename__ = 'certificates'
    __table_args__ = {'extend_existing': True}
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    publicKey: Mapped[str]
    token: Mapped[str]
    transportKey: Mapped[bytes]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped['DbUser'] = relationship(back_populates='certificates')


class DbGroup(Base):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True}
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    users: Mapped[list['DbUser']] = relationship(secondary=userGroup_table, back_populates='groups')


class DbRole(Base):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    users: Mapped[list['DbUser']] = relationship(secondary=userGroup_table, back_populates='roles')
