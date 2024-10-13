from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField  # Import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired  # Import the necessary validators
class LoginForm(FlaskForm):
    employee_number = StringField('Employee number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class AssignTableForm(FlaskForm):
    table_number = IntegerField('Table number', validators=[DataRequired()])
    employee=StringField('employee',  validators=[DataRequired()])
    submit = SubmitField('Assign')
