from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, DecimalField, FloatField, PasswordField, BooleanField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    word = StringField('')
    submit = SubmitField('search')

class FilterForm(FlaskForm):
    pet_select_all = BooleanField('Select All')
    dogs = BooleanField('dogs')
    cats = BooleanField('cats')
    age1 = IntegerField('ages: from')
    age2 = IntegerField('to')#remember to add months in html
    others_select_all = BooleanField('Select All')
    foods = BooleanField('foods')
    keepers = BooleanField('keepers')
    others = BooleanField('others')
    price1 = IntegerField('price: from')
    price2 = IntegerField('to')
    submit = SubmitField('search')