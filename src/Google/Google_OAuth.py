from flask import Flask, Blueprint, render_template, make_response
from flask import request, redirect, jsonify, url_for, flash
import httplib2
import requests
import json
import crud
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

google = Blueprint('google', __name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Google OAuth Login

@google.route('/G_OAuth', methods=['POST'])
def googleLogin():
    # if request.args.get('state') != login_session['state']:
    #     flash('Invalid State Parameter')
    #     return redirect(url_for('login'))

    code = request.data.decode()

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf8'))
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        flash('''Token's user ID doesn't match given user ID.''')
        return redirect(url_for('login'))

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        flash('''Token's client ID does not match app's.''')
        return redirect(url_for('login'))

    # stored_access_token = login_session.get('access_token')
    # stored_gplus_id = login_session.get('gplus_id')
    # if stored_access_token is not None and gplus_id == stored_gplus_id:
    # 	response = make_response(
    #        json.dumps('Current user is already connected.'),
    #       200)
    # 	response.headers['Content-Type'] = 'application/json'
    # 	return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['OAuth'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['loggedIn'] = True
    crud.add_OAuthUser(login_session)
    return 'Logged In'


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
        return redirect('/')
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response