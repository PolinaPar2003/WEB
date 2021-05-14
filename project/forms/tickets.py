from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import NumberRange, DataRequired


class TicketsForm(FlaskForm):
    date_v = DateField('Дата', validators=[DataRequired()])
    tickets_adult = IntegerField("Билеты для взрослых", validators=[NumberRange(min=0, max=100)])
    tickets_4_7 = IntegerField("Билеты для детей от 4 до 7 лет", validators=[NumberRange(min=0, max=100)])
    tickets_7_18 = IntegerField("Билеты для детей от 7 до 18 лет", validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Купить')
