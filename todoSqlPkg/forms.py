# todoSqlPkg/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, ValidationError

from .models import User




def check_validate_credentials(form, field):
    """ username and password checker"""

    username_entered = form.username.data
    password_enter = form.password.data

    # check username is valid
    user_object = User.query.filter_by(username=username_entered).first()

    if user_object is None:
        raise ValidationError('Username or password is invalid!')
    elif password_enter != user_object.password:
        raise ValidationError('Password is incorrect!')

class UserForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), check_validate_credentials])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired(message='Password required'), check_validate_credentials])
    submit = SubmitField('submit')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object is None:
            raise ValidationError('Username or password is incorrect!')
        
    # def validate_password(self, password):
    #     user_object = User.query.filter_by(password=password.data).first()
    #     if user_object is None:
    #         raise ValidationError('Password is invalid!')



class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    completed = SelectField('Completed', choices = [("False", "False"), ("True", "True")], validators = [DataRequired()])
    submit = SubmitField("Add todo")