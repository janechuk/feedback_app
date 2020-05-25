from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, Length


class AddUserForm(FlaskForm):
    """Form for adding user for feedback app."""
    username = StringField("Username", validators=[
                           InputRequired(), Length(max=30, message=None)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
