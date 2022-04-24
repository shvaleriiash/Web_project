import sqlalchemy
from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'Product'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    Name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)

    Description = sqlalchemy.Column(sqlalchemy.String)

    Price = sqlalchemy.Column(sqlalchemy.Integer)

    Count = sqlalchemy.Column(sqlalchemy.Integer)

    ImageId = sqlalchemy.Column(sqlalchemy.Integer)

    Category = sqlalchemy.Column(sqlalchemy.Integer)