import os
from app.forms.orgForm import OrgForm
from app.auth import get_token
from app.organizations import createOrganization
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__, instance_relative_config=True)


app.config.from_object('config')
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = OrgForm(request.form, csrf_enabled=False)

        if form.validate_on_submit():

            getTitle = form.title.data
            netID = form.netID.data
            print(getTitle)
            print(netID)
            blackboard_token = get_token()
            createOrganization(getTitle, netID, blackboard_token)

        return redirect('/')

    else:
        form = OrgForm(csrf_enabled=False)
    return render_template('create.html', form=form)