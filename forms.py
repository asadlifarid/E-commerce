from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, IntegerField, SubmitField, Form
from wtforms.validators import DataRequired, Email, Length, EqualTo  
from flask_wtf.csrf import CSRFProtect


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    
class ReviewForm(FlaskForm):
    message = TextAreaField('message', validators=[DataRequired()])
    user_id =IntegerField('user_id')
    
class ContactsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=30)])
    email = StringField('email', validators=[DataRequired(), Email()])
    subject = StringField('subject', validators=[DataRequired()])
    message = TextAreaField('message')
    
class FavoriteForm(FlaskForm):
    image = StringField('image', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    products_name = StringField('name', validators=[DataRequired()])
    
    
class SearchForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    

class NewsletterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])