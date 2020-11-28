import requests

from clientManager.config import service_ip, service_port, api_version, headers


def getstudies():
    url = "http://{}:{}/{}/studies".format(service_ip, service_port, api_version)
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))

    return r


def getstudy(studyid):
    url = "http://{}:{}/{}/study/{}".format(service_ip, service_port, api_version, studyid)
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        print("request failed with status: {}".format(r.status_code))
    return r
