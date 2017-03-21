from flask_wtf import FlaskForm
from wtforms import StringField, validators



class OrgForm(FlaskForm):
    title = StringField('Title of Organization', [validators.Length(min=4, max=40),
                                                  validators.Regexp('[A-Za-z0-9]+', message="Title must contain only letters") ])
    netID = StringField('Organization Manager NetID', [validators.Length(min=3, max=4), validators.Regexp('[A-Za-z0-9]+', message="Please Enter you NETID")])
