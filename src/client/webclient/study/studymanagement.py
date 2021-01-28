import requests
from flask import session

from webclient.config import service_ip, service_port, api_version, headers
from requests.auth import HTTPBasicAuth


def getstudies():
    url = "http://{}:{}/{}/studies".format(service_ip, service_port, api_version)
    r = requests.get(url=url, headers=headers, auth=HTTPBasicAuth('admin', 'superadmin'))
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def getstudy(studyid):
    url = "http://{}:{}/{}/study/{}".format(service_ip, service_port, api_version, studyid)
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))
    return r


def update_module(study_id, module):
    url = "http://{}:{}/{}/study/{}/module".format(service_ip, service_port, api_version, study_id)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['studyapi_token']

    r = requests.put(url=url, headers=headers_token, json=module)

    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))
    return r


def update_lecture(study_id, module_id, lecture):
    url = "http://{}:{}/{}/study/{}/module/{}/lecture".format(service_ip, service_port, api_version, study_id, module_id)

    headers_token = headers
    headers_token["Authorization"] = "Bearer " + session['studyapi_token']

    r = requests.put(url=url, headers=headers_token, json=lecture)

    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))
    return r