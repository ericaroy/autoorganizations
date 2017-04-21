import json
import os
import requests
from random import randint
from flask import flash
from app.logfile import ContextFilter
from flask_mail import Mail, Message
from flask import Flask


app = Flask(__name__)


create_organization_url_path = 'https://blackboard.ualr.edu/learn/api/public/v1/courses/'

log = ContextFilter()

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.environ['UALR_USERNAME'],
    MAIL_PASSWORD=os.environ['UALR_PASSWORD'],
))


def create_organization(get_title, net_id, blackboard_token, user_email):
    # generate org ID
    f = randint(1, 1000)
    sep = '_'
    x = get_title.split()
    created_courseid = sep.join(x) + '_' + str(f)

    payload = {'courseId': '', 'name': '', 'organization': 'true', 'enrollment': {'type': 'SelfEnrollment'}}
    payload['name'] = get_title
    payload['courseId'] = created_courseid

    try:
        r = requests.post(create_organization_url_path, data=json.dumps(payload),
                          headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})
        if r.status_code == 201 or r.status_code == 200:
            flash('Thank you. Your request is being processed. Please check Blackboard in the next 30 minutes - 1 hour.', 'success')
            # testing logging
            # log.log_to_file(getTitle, netID, createdCourseID)
            send_mail(get_title, net_id, created_courseid, user_email)
            enroll_user(created_courseid, net_id, blackboard_token)

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


def enroll_user(created_courseid, net_id, blackboard_token):  # not complete
    payload = {'courseRoleId': 'orgmanager'}

    enroll_user_url_path = 'https://blackboard.ualr.edu/learn/api/public' \
                           '/v1/courses/externalId:{}/users/userName:{}'.format(created_courseid, net_id)

    r = requests.put(enroll_user_url_path, data=json.dumps(payload),
                     headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})

mail = Mail(app)  # might pull this out in its own file later, working now


def send_mail(organization_name, net_id, organization_id, user_email):

        msg = Message(
            'Automatic Blackboard Organization Created',
            sender='enroy@ualr.edu',
            recipients=
            ['enroy@ualr.edu'])  # send this to log eventually
        msg.body = "An organization was just created named {} by {}, " \
                   "organization id is {}, contact {}."\
            .format(organization_name,net_id,organization_id, user_email)
        mail.send(msg)
        return "Sent"


def check_netid(net_id, blackboard_token, get_title):
    check_user_path_url = 'https://blackboard.ualr.edu/learn/api/public/v1/users/userName:{}'.format(net_id)
    try:
        r = requests.get(check_user_path_url, headers={'Authorization': blackboard_token})
        if r.status_code == 200:
            x = json.loads(r.text)
            user_email = x['contact']['email']
            create_organization(get_title, net_id, blackboard_token, user_email)

        if r.status_code == 404:
            flash('User not found, please try again later', 'danger')

    except requests.exceptions.HTTPError as e:

        if e.response.status_code == 400:
            flash('Invalid ID, a message has been sent to the system admin', 'warning')






