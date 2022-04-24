import sqlalchemy
from data.db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'Category'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)