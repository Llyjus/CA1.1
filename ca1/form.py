from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, DecimalField, FloatField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    user_id = StringField('User ID',
                            validators=[InputRequired()])
    password = PasswordField('Password',
                            validators=[InputRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    user_id = StringField('User ID',
                            validators=[InputRequired()])
    password = PasswordField('Password',
                            validators=[InputRequired()])
    password2 = PasswordField('Password Confirm',
                            validators=[InputRequired(),
                                        EqualTo('password')])
    securityQ = RadioField('Choose one to answer',
                            choice=['''What's your mother's name?''',
                                    '''your first girlfriend's/boyfriend's name?''',
                                    '''your father's birthday is?''',
                                    '''What's the brand of your first cars?'''],
                                    default='''What's your mother's name?''')
    securityA = PasswordField('Answer',
                            validators=[InputRequired()])
    submit = SubmitField('Submit')

class SecurityForm1(FlaskForm):
    user_id = StringField('Your User ID',
                            validators=[InputRequired()])
    submit = SubmitField('Next')

class SecurityForm2(FlaskForm):
    securityA = PasswordField('Answer',
                            validators=[InputRequired()])
    submit = SubmitField('Next')

class ResetPassForm(FlaskForm):
    password = PasswordField('New password',
                            validators=[InputRequired()])
    submit = SubmitField('Submit')

class AdminLoginForm(FlaskForm):
    user_id = StringField('Admin ID',
                            validators=[InputRequired()])
    password = PasswordField('Password',
                            validators=[InputRequired()])
    submit = SubmitField('Submit')




