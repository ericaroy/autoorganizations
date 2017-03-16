import json
import requests
from random import randint
from flask import flash
from app.logfile import ContextFilter

create_organization_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/'

log = ContextFilter()


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
            flash('You have successfully created an organization', 'success')
            # testing logging
            # log.log_to_file(getTitle, netID, createdCourseID)
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

    enroll_user_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/externalId:{}/users/userName:{}'.format(
        createdCourseID, netID)

    r = requests.put(enroll_user_url_path, data=json.dumps(payload),
                     headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})

    #do some error catching/response




