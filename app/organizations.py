import requests
import json
import logging
import sys
from random import randint
from flask import Flask, redirect, flash, request, url_for, render_template
from app.logs.logfile import ContextFilter

create_organization_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/'
enroll_user_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/courses/{}/users/{}'
log = ContextFilter


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
            log.log_to_file(getTitle, netID, createdCourseID)

        r.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(e)
        if e.response.status_code == 404:
            print('404')
            # maybe redirect to a 404 page
            flash('Oops something went wrong, please try again later.', 'warning')
        if e.response.status_code == 400:
            flash('Please contact system admin - enroy@ualr.edu.', 'danger')
            # log
            # send log, redirect and emp

    except requests.exceptions.Timeout as e:
        print(e)
        flash('Connection Timed Out, Try Again.', 'warning')


def enroll_user(createdCourseID, netID, blackboard_token):  # not complete
    print('was called')
    r = requests.put(enroll_user_url_path,
                     headers={'Authorization': blackboard_token, 'Content-Type': 'application/json'})
    print(r.text)
    print(r.status_code)


