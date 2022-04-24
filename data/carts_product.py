import sqlalchemy
from sqlalchemy import ForeignKey

from data.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class CartsProduct(SqlAlchemyBase):
    __tablename__ = 'CartsProduct'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    OwnerCart = sqlalchemy.Column(sqlalchemy.String, ForeignKey('Carts.Id'), index=True, nullable=False)

    ProductId = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('Product.Id'), nullable=False)

    Status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    RealTimePrice = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('Product.Price'), nullable=True)

    PayTimePrice = sqlalchemy.Column(sqlalchemy.REAL)

    Date = sqlalchemy.Column(sqlalchemy.DATE)