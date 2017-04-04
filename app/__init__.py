import os
import sys
import logging
from app.forms.orgForm import OrgForm
from app.auth import get_token
from app.organizations import create_organization, check_netid
from flask import Flask, render_template, request, redirect


app = Flask(__name__, instance_relative_config=True)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


app.config.from_object('config')
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = OrgForm(request.form, csrf_enabled=True)

        if form.validate_on_submit():

            get_title = form.title.data.title()
            net_id = form.net_id.data
            blackboard_token = get_token()
            check_netid(net_id, blackboard_token, get_title)

            return redirect('/')

    else:
        form = OrgForm(csrf_enabled=True)
    return render_template('create.html', form=form)
