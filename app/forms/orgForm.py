from flask_wtf import FlaskForm
from wtforms import StringField, validators


class OrgForm(FlaskForm):
    title = StringField([validators.Length(min=4, max=40),
                                                  validators.Regexp('[A-Za-z0-9]+',
                                                                    message="Title must contain only letters")], render_kw={'placeholder': 'Title of Organization'})
    net_id = StringField([validators.Length(min=3, max=4),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please Enter you NETID")], render_kw={'placeholder':'Organization Manager NETID'})
