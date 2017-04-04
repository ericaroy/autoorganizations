import os
import sys
import logging
import flask
import urllib
from urllib.parse import urlparse
import argparse
from app.forms.orgForm import OrgForm
from app.auth import get_token
from app.organizations import createOrganization, check_netid
from flask import Flask, render_template, request, redirect
from flask_cas import CAS, login_required

app = Flask(__name__, instance_relative_config=True)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
cas = CAS(app)


app.config.from_object('config')
app.secret_key = os.environ['SECRET_KEY']
app.config['CAS_SERVER'] = 'https://netid.test.ualr.edu'
app.config['CAS_AFTER_LOGIN'] = 'archive'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = OrgForm(request.form, csrf_enabled=True)

        if form.validate_on_submit():

            getTitle = form.title.data.title()
            netID = form.netID.data
            blackboard_token = get_token()
            check_netid(netID, blackboard_token, getTitle)

            return redirect('/')

    else:
        form = OrgForm(csrf_enabled=True)
    return render_template('create.html', form=form)


@app.route('/login/')
def route_login():

    if 'ticket' in Flask:
        flask.session['_cas_token'] = flask.request.args['ticket']

    if '_cas_token' in flask.session:

        if validate(flask.session['_cas_token']):
            redirect_url = flask.url_for('create')
        else:
            redirect_url = create_cas_login_url(app.config['cas_server'])
            del flask.session['_cas_token']
    else:
        redirect_url = create_cas_login_url(app.config['cas_server'])

    app.logger.debug('Redirecting to: {}'.format(redirect_url))

    return flask.redirect(redirect_url)

def create_cas_login_url(cas_url):
    service_url = urllib.quote(
        flask.url_for('route_login',_external=True))
    return urlparse.urljoin(
        cas_url,
        '/cas/?service={}'.format(service_url))


def validate(ticket):

    app.logger.debug("validating token {}".format(ticket))

    cas_validate_url = create_cas_validate_url(
        app.config['cas_server'], ticket)

    app.logger.debug("Making GET request to {}".format(
        cas_validate_url))

    try:
        (isValid, username) = urllib.urlopen(cas_validate_url).readlines()
        isValid = True if isValid.strip() == 'yes' else False
        username = username.strip()
    except ValueError:
        app.logger.error("CAS returned unexpected result")
        isValid = False

    if isValid:
        app.logger.debug("valid")
        flask.session['username'] = username
    else:
        app.logger.debug("invalid")

    return isValid

def create_cas_validate_url(cas_url, ticket):
    service_url = urllib.quote(
        flask.url_for('route_login',_external=True))
    ticket = urllib.quote(ticket)
    return urlparse.urljoin(
        cas_url,
        '/cas/validate?service={}&ticket={}'.format(service_url, ticket))