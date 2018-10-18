from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
import requests
from project.api import mainflux_client

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    pwd = post_data.get('password')
    if not pwd:
        return jsonify(response_object), 400
    try:
        status = mainflux_client.create_account(email, pwd)
        if status == 201:
            response_object = {
                'status': 'success',
                'message': '{email} was added!'.format(email=email)
            }
        elif status == 200:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object)
        elif status == 409:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object)
    except requests.exceptions.HTTPError as errh:
        response_object['message'] = errh
        return jsonify(response_object), 404
    except requests.exceptions.ConnectionError as errc:
        response_object['message'] = errc
        return jsonify(response_object), 404
    except requests.exceptions.Timeout as errt:
        response_object['message'] = errt
        return jsonify(response_object), 404
    except requests.exceptions.RequestException as err:
        response_object['message'] = err
        return jsonify(response_object), 500

    return jsonify(response_object), status

@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    post_data = request.get_json()
    response_object = { 'status': 'fail',  'message': 'Invalid payload.'  }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        r = mainflux_client.get_token(email,password)
        try:
            auth_token = r.json()['token']
        except:
            response_object['message'] = 'Sorry. That user does not exist.'
            return jsonify(response_object), r.status_code
        if auth_token:
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully logged in.'
            response_object['auth_token'] = auth_token
            return jsonify(response_object), r.status_code
    except requests.exceptions.HTTPError as errh:
        response_object['message'] = errh
        return jsonify(response_object), 404
    except requests.exceptions.ConnectionError as errc:
        response_object['message'] = errc
        return jsonify(response_object), 404
    except requests.exceptions.Timeout as errt:
        response_object['message'] = errt
        return jsonify(response_object), 404
    except requests.exceptions.RequestException as err:
        response_object['message'] = err
        return jsonify(response_object), 500