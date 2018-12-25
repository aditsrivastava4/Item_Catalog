from flask import Flask, Blueprint, render_template, make_response
from flask import request, redirect, jsonify, url_for, flash
import httplib2
import requests
import json
import crud
import string
import random
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

google = Blueprint('google', __name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Google OAuth Login

@google.route('/G_OAuth', methods=['POST'])
def googleLogin():
    # Get user info
    user_data = request.data.decode()
    data = json.loads(user_data)

    # if data['csrfToken'] != login_session['state']:
    #     response = make_response(
    #         json.dumps({
    #             'response': 'Invaild State Token',
    #             'code': 400
    #         })
    #     )
    #     response.headers['Content-Type'] = 'application/json'
    #     return response

    login_session['OAuth'] = 'google'
    login_session['access_token'] = data['accessToken']
    login_session['gplus_id'] = data['profileObj']['googleId']
    login_session['username'] = data['profileObj']['name']
    login_session['picture'] = data['profileObj']['imageUrl']
    login_session['email'] = data['profileObj']['email']
    login_session['loggedIn'] = True
    state = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.digits) for x in range(64))
    login_session['state'] = state
    crud.add_OAuthUser(login_session)
    return jsonify({
            'LoggedIn': True,
            'csrfToken': state
        })


# Google OAuth Logout

@google.route('/G_Logout')
def googleLogout():
    access_token = login_session.get('access_token')
    if access_token is None:
        flash('Current user not connected.')
        return redirect(url_for('login'))

    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        login_session['access_token']
    )
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['OAuth']
        login_session['loggedIn'] = False
        return jsonify({
            'logout': True
        })
    else:
        response = make_response(
            json.dumps({
                'response': 'Failed to revoke token for given user.',
                'code': 400
            })
        )
        response.headers['Content-Type'] = 'application/json'
        return response