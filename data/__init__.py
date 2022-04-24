import os
import string
from random import sample, shuffle
from tempfile import SpooledTemporaryFile

from werkzeug.utils import secure_filename

from data import db_session
from data.carts import Cart
from data.carts_product import CartsProduct
from data.category import Category
from data.product import Product
from data.users import User


def generate_random_trash(m):
    digits = list(set(string.digits) - {'1', '0'})
    while True:
        c = m // 3
        b = m - 2 * c
        if c <= 8:
            a = sample(digits, c)
        else:
            a = digits
            d = (c - len(digits)) + c + b
            if d % 2 == 0:
                c, b = int(d / 2), int(d / 2)
            else:
                c, b = int(d // 2), int(d // 2 + 1)
        a.extend(sample(digits, c))
        a.extend(sample(digits, b))
        shuffle(a)
        a = ''.join(a)
        if (a + ".jpg" not in os.listdir("./static/img/")) and (
                a + ".png" not in os.listdir("./static/img/")) and (
                a + ".jpeg" not in os.listdir("./static/img/")):
            break
    return a


def get_all_categorys():
    db_sess = db_session.create_session()
    return db_sess.query(Category).all()


def get_all_products_with_category(categorys):
    db_sess = db_session.create_session()
    Products = db_sess.query(Product).all()
    Access = []
    for i in Products:
        if i.Id in categorys:
            Access.append(i)
    return Access


def create_user(id, name, password, status):
    db_sess = db_session.create_session()
    user = User(id=id, Name=name, Status=status)
    user.set_password(password)
    create_cart(user, db_sess)
    db_sess.add(user)
    db_sess.commit()


def create_cart(user, db_sess):
    cart = Cart(Owner=user.id)
    db_sess.add(cart)
    db_sess.commit()


def add_product(name, description, price, count, image, form, res):
    db_sess = db_session.create_session()
    imageid = generate_random_trash(10)
    cat = None
    for categories in res:
        if form.category.data in categories:
            cat = categories[0]
    new_product = Product(Name=name,
                          Description=description,
                          Price=price,
                          Count=count,
                          ImageId=imageid, Category=cat)
    with open(f"./static/img/{imageid}.jpg", "wb") as f:
        f.write(image.data.stream.read())
    db_sess.add(new_product)
    db_sess.commit()


def add_to_cart(user, product):
    db_sess = db_session.create_session()
    if isinstance(user, User):
        cartId = db_sess.query(Cart.Id).filter(Cart.Owner == user.id).first()[0]
    elif isinstance(user, int):
        cartId = db_sess.query(Cart.Id).filter(Cart.Owner == user).first()[0]
    else:
        raise Exception("Недопустимый класс user")
    if isinstance(product, Product):
        product = product
    elif isinstance(product, int):
        product = db_sess.query(Product).filter(Product.Id == product).first()
    else:
        raise Exception("Недопустимый класс product")
    cartproduct = CartsProduct(OwnerCart=cartId,
                               ProductId=product.Id,
                               Status=0,
                               RealTimePrice=product.Price)
    db_sess.add(cartproduct)
    db_sess.commit()


def buy_product(user_or_cart):
    db_sess = db_session.create_session()
    if isinstance(user_or_cart, User):
        cart = db_sess.query(Cart).filter(Cart.Owner == user_or_cart.Id).first()
    elif isinstance(user_or_cart, Cart):
        cart = user_or_cart
    else:
        raise Exception("Недопустимый класс user_or_cart")
    all_prodCart = db_sess.query(CartsProduct).filter(CartsProduct.Status == 0,
                                                      CartsProduct.OwnerCart == cart.Id)
    return all_prodCart


if __name__ == '__main__':
    pass