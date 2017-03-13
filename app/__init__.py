import os
from flask import Flask, render_template, request, flash, redirect
from app.forms.orgForm import OrgForm
from app.auth import getToken


app = Flask(__name__, instance_relative_config=True)


app.config.from_object('config')
app.secret_key = os.environ['SECRET_KEY']
#app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = OrgForm(request.form, csrf_enabled=False)

        if form.validate_on_submit():
            flash('You have successfully created an organization', 'success')
            getTitle = form.title.data
            netID = form.netID.data
            print(getTitle)
            print(netID)
            #blackboard_token = getToken() #delay for now


            return redirect('/')

    else:
        form = OrgForm(csrf_enabled=False)
    return render_template('create.html', form=form)