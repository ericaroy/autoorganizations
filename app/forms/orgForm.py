from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, validators
from wtforms.validators import DataRequired


class OrgForm(FlaskForm):
    title = StringField('Title of Organization', [validators.Length(min=4, max=40),validators.Regexp('[A-Za-z0-9]+', message="Title must contain only letters") ])
    netID = StringField('Organization Manager NetID', [validators.Length(min=3, max=9)])