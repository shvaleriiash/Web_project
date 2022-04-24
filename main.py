import flask_login
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import redirect
import data
from data import db_session, Category, Product, CartsProduct, Cart
from data.users import User
from forms import RegisterForm, LoginForm, ProfileForm, ProductForm, PaymentForm
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
db_session.global_init("db/database.db")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/img'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = "lerochka"
login_manager = LoginManager()
login_manager.init_app(app)

summ = 0


@app.route('/')
def base():
    db_sess = db_session.create_session()
    res = db_sess.query(Category.Name).all()
    categories = [category[0] for category in res]
    return render_template('main.html', title='Главная страница', categories=categories)


#регистрация
@app.route('/<site>', methods=['GET', 'POST'])
def reg(site):
    name = str(request.url).split('/')[-1]
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if flask_login.current_user.is_anonymous:
            return redirect('/registration')
        elif not flask_login.current_user.is_anonymous:
            user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
            data.add_to_cart(user, int(request.form['add']))
    ID = db_sess.query(Category.Id).filter(Category.Name == name).first()[0]
    products = db_sess.query(Product.Name, Product.Price, Product.ImageId, Product.Id,
                             Product.Count).filter(
        Product.Category == int(ID)).all()
    return render_template('category.html', title=f'{str(site).capitalize()}', products=products,
                           cat=f'{str(site).capitalize()}')


@app.route('/<site>/<int:prod>', methods=['GET', 'POST'])
def prod(site, prod):
    db_sess = db_session.create_session()
    ID = int(str(request.url).split('/')[-1])
    if request.form.get("add"):
        if flask_login.current_user.is_anonymous:
            return redirect('/registration')
        elif not flask_login.current_user.is_anonymous:
            user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
            data.add_to_cart(user, ID)
    if request.form.get("delete"):
        product = db_sess.query(Product).filter(Product.Id == ID).first()
        img = db_sess.query(Product.ImageId).filter(Product.Id == ID).first()
        try:
            os.remove(f'./static/img/{img[0]}.jpg')
        except Exception:
            pass
        db_sess.delete(product)
        db_sess.commit()
        return redirect(f'/{site}')
    res = db_sess.query(Product.Name, Product.Price, Product.Description, Product.ImageId,
                        Product.Count).filter(
        Product.Id == ID).all()[0]
    return render_template('product.html', title=res[0], product=res, Cate=site)


@app.route('/cart')
def cart():
    global summ
    summ = 0
    db_sess = db_session.create_session()
    res = db_sess.query(Cart.Id).filter(Cart.Owner == flask_login.current_user.id).first()
    prdcts = db_sess.query(CartsProduct.ProductId, CartsProduct.Id).filter(
        CartsProduct.OwnerCart == res[0]).all()
    products = []
    for prd in prdcts:
        product = db_sess.query(Product).filter(Product.Id == prd[0]).first()
        price = db_sess.query(Product.Price).filter(Product.Id == prd[0]).first()
        summ += price[0]
        ID = prd[1]
        products.append([product, ID])
    return render_template('cart.html', title='Коризна', products=products, summ=summ)


#оплата
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    global summ
    form = PaymentForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        owner = db_sess.query(Cart.Id).filter(Cart.Owner == flask_login.current_user.id).first()
        res = db_sess.query(CartsProduct).filter(CartsProduct.OwnerCart == owner[0]).all()
        for product in res:
            db_sess.delete(product)
            db_sess.commit()
        summ = 0
        return redirect('/u')
    return render_template('payment.html', title='Оплата', form=form, summ=summ)


#успешная оплата
@app.route('/success')
def success():
    return render_template('success.html', title='Успешная оплата')


@app.route('/delete/<product>')
def delete_c_p(product):
    global summ
    db_sess = db_session.create_session()
    res = db_sess.query(CartsProduct).filter(CartsProduct.Id == product).first()
    db_sess.delete(res)
    db_sess.commit()
    summ = 0
    return redirect('/cart')


@app.route('/delete_product')
def delete_product():
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter().first()
    db_sess.delete(product)
    db_sess.commit()
    return redirect('/')


#регистрация
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        data.create_user(id=form.email.data,
                         name=form.name.data,
                         status=0,
                         password=form.password.data)
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


#вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


#просмотр профиля
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Профиль')


#удалить профиль
@login_required
@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
    Id = db_sess.query(Cart.Id).filter(Cart.Owner == flask_login.current_user.id).first()
    car_t = db_sess.query(Cart).filter(Cart.Owner == flask_login.current_user.id).first()
    prd = db_sess.query(CartsProduct).filter(CartsProduct.OwnerCart == Id[0]).all()
    for i in prd:
        db_sess.delete(i)
    db_sess.delete(car_t)
    db_sess.delete(user)
    db_sess.commit()
    return redirect('/')


@app.route('/change_profile', methods=['GET', 'POST'])
@login_required
def change_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('change_profile.html', title='Изменение профиля',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == form.email.data).first():
            if form.email.data == flask_login.current_user.id:
                pass
            else:
                return render_template('change_profile.html', title='Изменение профиля',
                                       form=form,
                                       message="Такой пользователь уже есть")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
        user.id = form.email.data
        user.set_password(form.password.data)
        user.Name = form.name.data
        db_sess.commit()
        login_user(user, remember=False)
        return redirect('/profile')
    return render_template('change_profile.html', title='Изменение профиля', form=form)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    db_sess = db_session.create_session()
    res = db_sess.query(Category.Id, Category.Name).all()
    form.category.choices = [category[1] for category in res]
    if form.validate_on_submit():
        data.add_product(form.name.data,
                         form.description.data,
                         form.price.data,
                         form.count.data,
                         form.image,
                         form, res)
        return redirect("/add_product")
    return render_template('add_product.html', title='Добавление товара', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


#информация
@app.route('/about')
def about():
    return render_template('about.html', title='О @buussina')


@app.route('/developers')
def developers():
    return render_template('developers.html', title='Создатель')


if __name__ == '__main__':
    app.run()