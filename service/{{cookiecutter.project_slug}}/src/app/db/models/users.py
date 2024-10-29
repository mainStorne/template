from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'

