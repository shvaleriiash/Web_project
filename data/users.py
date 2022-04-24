import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    Name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)

    PasswordHash = sqlalchemy.Column(sqlalchemy.String)

    Status = sqlalchemy.Column(sqlalchemy.Integer)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)