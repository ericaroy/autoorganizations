import os
from app.forms.orgForm import OrgForm
from app.auth import get_token
from app.organizations import createOrganization
from flask import Flask, render_template, request, redirect
from flask_cas import CAS, login_required

app = Flask(__name__, instance_relative_config=True)
CAS(app)


app.config.from_object('config')
app.secret_key = os.environ['SECRET_KEY']
app.config['CAS_SERVER'] = 'https://netid.test.ualr.edu'
app.config['CAS_AFTER_LOGIN'] = 'create'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        form = OrgForm(request.form, csrf_enabled=False)

        if form.validate_on_submit():

            getTitle = form.title.data
            netID = form.netID.data
            blackboard_token = get_token()
            createOrganization(getTitle, netID, blackboard_token)

        return redirect('/')

    else:
        form = OrgForm(csrf_enabled=False)
    return render_template('create.html', form=form)


@app.route('/archive')
@login_required
def archive():
    return render_template('archive.html')


@app.route('/about')
def about():
    return render_template('about.html')