from flask import Flask, Blueprint, render_template, make_response
from flask import request, redirect, jsonify, url_for, flash
import requests
import json
import crud
from flask import session as login_session

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow

google = Blueprint('google', __name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Google OAuth Login

@google.route('/G_OAuth', methods=['POST'])
def googleLogin():
    if request.args.get('state') != login_session['state']:
        flash('Invalid State Parameter')
        return redirect(url_for('login'))

    code = request.data.decode()

    try:
        flow = Flow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 
                   'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri='postmessage'
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
    except Exception as e:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the token
    try:
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token, google_requests.Request(), CLIENT_ID)
        
        # Verify that the access token is used for the intended user.
        gplus_id = idinfo['sub']
        
    except ValueError:
        # Invalid token
        response = make_response(json.dumps('Invalid token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.token
    login_session['gplus_id'] = gplus_id

    # Get user info from the token
    login_session['OAuth'] = 'google'
    login_session['username'] = idinfo.get('name', '')
    login_session['picture'] = idinfo.get('picture', '')
    login_session['email'] = idinfo.get('email', '')
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

    # Revoke the token
    revoke_url = f'https://oauth2.googleapis.com/revoke?token={access_token}'
    result = requests.post(revoke_url)
    
    if result.status_code == 200:
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