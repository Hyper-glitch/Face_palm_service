from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField(label=('Username'), validators=[DataRequired()])
    submit = SubmitField('Submit')
