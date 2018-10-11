import requests
import urllib
from flask import current_app

"""
Supporting  module  for  mainflux queries
"""


def create_account(username, pwd):
    r = requests.post(
        urllib.parse.urljoin(current_app.config['MAINFLUX_ADDRESS'], 'users'),
        json=({'email': username, 'password': pwd}),
        verify=current_app.config['VERIFY_HTTPS'])
    return r.status_code


def get_token(username, pwd):
    r = requests.post(urllib.parse.urljoin(
        current_app.config['MAINFLUX_ADDRESS'], 'tokens'),
                      json=({'email': username, 'password': pwd}),
                      verify=current_app.config['VERIFY_HTTPS'])
    return r
