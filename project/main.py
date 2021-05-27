from flask import Flask, url_for, render_template, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from data.tickets import Tickets
from data.reviews import Reviews
from data.animals import Animals
from data.souvenirs import Souvenirs
from data import db_session
from forms.tickets import TicketsForm
import os
from forms.register import RegisterForm
from forms.reviews import ReviewsForm
from forms.login import LoginForm
from flask import request
from data import reviews_resourses
from data import users_resources
from flask_restful import abort, Api

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(reviews_resourses.ReviewsListResource, '/api/v2/add_reviews')
api.add_resource(reviews_resourses.ReviewsResource, '/api/v2/add_reviews/<int:reviews_id>')
api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")  # главное окно
def enter():
    oct = url_for('static', filename='img/octopus2.png')
    file = url_for('static', filename='css/enter.css')
    return render_template("enter.html", oct=oct, file=file, title='Океанариум')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/inhabitants")  # окно с обитателями
def animals():
    ani = url_for('static', filename='img/octopus_back.png')
    db_sess = db_session.create_session()
    animals = db_sess.query(Animals).all()
    return render_template("inhabitants.html", title='Обитатели', ani=ani, animals=animals)


@app.route("/services")  # окно с услугами
def services():
    ser = url_for('static', filename='img/octopus_back.png')
    return render_template("services.html", title='Услуги', ser=ser)


@app.route("/tickets")  # окно с билетами
def tickets():
    tic = url_for('static', filename='img/octopus_back.png')
    db_sess = db_session.create_session()
    tickets = db_sess.query(Tickets).all()
    return render_template("tickets.html", title='Билеты', tic=tic, tickets=tickets)


@app.route("/buy_tickets", methods=['GET', 'POST'])  # покупка билета
def buy_tickets():
    form = TicketsForm()
    tic = url_for('static', filename='img/octopus_back.png')
    db_sess = db_session.create_session()
    tickets = db_sess.query(Tickets).all()
    if form.validate_on_submit():
        summa = 0
        if form.tickets_adult.data + form.tickets_4_7.data + form.tickets_7_18.data == 0:
            return render_template('buy_tickets.html', tic=tic,
                                   message="Укажите хотя бы один билет",
                                   form=form, title='Покупка')
        else:
            summa += form.tickets_adult.data * 730 + form.tickets_4_7.data * 430 + form.tickets_7_18.data * 630
            return redirect(f"/buy/{summa}/{form.date_v.data}")
    return render_template("buy_tickets.html", title='Покупка', tic=tic, tickets=tickets, form=form)


@app.route("/reviews")  # окно с отзывами
def reviews():
    rev = url_for('static', filename='img/octopus_back.png')
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).all()
    return render_template("reviews.html", reviews=reviews, title='Отзывы', rev=rev)


@app.route("/buy/<int:summa>/<date>")  # окно с оплатой заказа
def buy(summa, date):
    bu = url_for('static', filename='img/deniz-fuchidzhiev-Km9q4SOvzDw-unsplash.jpg')
    rev = url_for('static', filename='img/octopus_back.png')
    return render_template("buy.html", title='Покупка', rev=rev, summa=summa, date=date, bu=bu)


@app.route('/add_reviews', methods=['GET', 'POST'])  # добавление отзыва
@login_required
def add_review():
    form = ReviewsForm()
    rev = url_for('static', filename='img/paris-K3B6crImWj0-unsplash.jpg')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = Reviews()
        review.title = form.title.data
        review.content = form.content.data
        current_user.reviews.append(review)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/reviews')
    return render_template('add_reviews.html',
                           form=form, rev=rev, title='Добавление отзыва')


@app.route('/add_reviews/<int:id>', methods=['GET', 'POST'])  # изменение отзыва
@login_required
def edit_review(id):
    form = ReviewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        review = db_sess.query(Reviews).filter(Reviews.id == id,
                                               Reviews.user == current_user
                                               ).first()
        if review:
            form.title.data = review.title
            form.content.data = review.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = db_sess.query(Reviews).filter(Reviews.id == id,
                                               Reviews.user == current_user
                                               ).first()
        if review:
            review.title = form.title.data
            review.content = form.content.data
            db_sess.commit()
            return redirect('/reviews')
        else:
            abort(404)
    return render_template('add_reviews.html',
                           title='Редактирование отзыва',
                           form=form
                           )


@app.route('/reviews_delete/<int:id>', methods=['GET', 'POST'])  # удаление отзыва
@login_required
def reviews_delete(id):
    db_sess = db_session.create_session()
    review = db_sess.query(Reviews).filter(Reviews.id == id,
                                           Reviews.user == current_user
                                           ).first()
    if review:
        db_sess.delete(review)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/reviews')


@app.route("/souvenirs")  #
def souvenirs():
    ser = url_for('static', filename='img/octopus_back.png')
    db_sess = db_session.create_session()
    souvenirs = db_sess.query(Souvenirs).all()
    return render_template("souvenirs.html", title='Сувениры', souvenirs=souvenirs, ser=ser)


@app.route("/contacts")  #
def contacts():
    con = url_for('static', filename='img/octopus_back.png')
    return render_template("contacts.html", title='Контакты', con=con)


@app.route('/login', methods=['GET', 'POST'])  # вход пользователя
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])  # форма для регистраци
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают", title='Регистрация')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть", title='Регистрация')
        if db_sess.query(User).filter(User.hashed_password == form.password.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пароль уже есть", title='Регистрация')
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template("register.html", form=form, title='Регистрация')


def main():
    db_session.global_init("db/oceanarium.db")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()


if __name__ == '__main__':
    main()

