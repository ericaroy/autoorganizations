import json
import os
import requests
from random import randint
from flask import flash
from app.logfile import ContextFilter
from flask.ext.mail import Mail, Message
from flask import Flask


app = Flask(__name__)


create_organization_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/'

log = ContextFilter()

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.environ['UALR_USERNAME'],
    MAIL_PASSWORD=os.environ['UALR_PASSWORD'],
))


def createOrganization(getTitle, netID, blackboard_token):
    # generate org ID
    f = randint(1, 1000)
    sep = '_'
    x = getTitle.split()
    createdCourseID = sep.join(x) + '_' + str(f)

    payload = {'courseId': '', 'name': '', 'organization': 'true', 'enrollment': {'type': 'SelfEnrollment'}}
    payload['name'] = getTitle
    payload['courseId'] = createdCourseID

    try:
        r = requests.post(create_organization_url_path, data=json.dumps(payload),
                          headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})
        if r.status_code == 201 or r.status_code == 200:
            flash('Thank you. Your request is being processed.', 'success')
            # testing logging
            # log.log_to_file(getTitle, netID, createdCourseID)
            send_mail(getTitle, netID, createdCourseID)
            enroll_user(createdCourseID, netID, blackboard_token)

        r.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(e)
        if e.response.status_code == 404:
            print('404')
            # maybe redirect to a 404 page
            flash('Oops something went wrong, please try again later.', 'warning')
        if e.response.status_code == 400:
            flash('Please contact system admin or try again later - enroy@ualr.edu.', 'danger')
            # log
            # send log, redirect and emp

    except requests.exceptions.Timeout as e:
        print(e)
        flash('Connection Timed Out, Try Again.', 'warning')


def enroll_user(createdCourseID, netID, blackboard_token):  # not complete
    payload = {'courseRoleId': 'orgmanager'}
    #make a call to api to check if user is valid, if so, go ahead and enroll, if not send email to admin with info as the org will still be created.

    enroll_user_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/externalId:{}/users/userName:{}'.format(
        createdCourseID, netID)

    r = requests.put(enroll_user_url_path, data=json.dumps(payload),
                     headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})

mail = Mail(app) # might pull this out in its own file later, working now

def send_mail(organization_name, net_id, organization_id):
	msg = Message(
        'Automatic Blackboard Organization Created',
	       sender='enroy@ualr.edu',
	       recipients=
               ['enroy@ualr.edu'])
	msg.body = "An organization was just created named {} by {}, organization id is {}".format(organization_name,net_id,organization_id)
	mail.send(msg)
	return "Sent"
