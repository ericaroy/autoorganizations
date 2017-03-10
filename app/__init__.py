from flask import Flask, render_template, request
from app.forms.orgForm import OrgForm



app = Flask(__name__, instance_relative_config=True)


app.config.from_object('config')
#app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = OrgForm(request.form)

    else:

        form = OrgForm(csrf_enabled = False)
    return render_template('create.html', form=form)