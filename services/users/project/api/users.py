from flask import Blueprint, jsonify, request, render_template
import requests
from project.api import mainflux_client

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@users_blueprint.route('/users', methods=['POST'])
def add_user():
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
