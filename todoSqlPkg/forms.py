# todoSqlPkg/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, ValidationError

from .models import User, get_user, get_password

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[InputRequired(message='Password required')])
    submit = SubmitField('submit')



# def validate_password(form, field):
#     user = get_user(form.password.data)
#     if not any (user.username == field.data for user in users):
#         raise ValidationError('Invalid Password')


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    completed = SelectField('Completed', choices = [("False", "False"), ("True", "True")], validators = [DataRequired()])
    submit = SubmitField("Add todo")