from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField, validators

class RegistrationForm(Form):
    first_name = TextField('first_name', [validators.Length(min=4, max=25)])
    last_name = TextField('last_name', [validators.Length(min=6, max=35)])
    telephone = IntegerField('telephone', [validators.Required(message='Please enter 7 digit phone number.')])
    
    """password = PasswordField('password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])"""