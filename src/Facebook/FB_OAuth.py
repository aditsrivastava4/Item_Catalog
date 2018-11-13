from flask import Flask, Blueprint, render_template
from flask import request, redirect, jsonify, url_for, flash
import httplib2
import requests
import json
import crud
from flask import session as login_session

facebook = Blueprint('facebook', __name__)

# Facebook OAuth Login
@facebook.route('/fb_OAuth', methods=['POST'])
def facebookLogin():
    if request.args.get('state') != login_session['state']:
        flash('Invalid State Parameter')
        return redirect(url_for('login'))

    access_token = request.data.decode()

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': access_token,
    }
    result = requests.get(url, params=params).json()

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result['access_token']

    url = 'https://graph.facebook.com/v2.8/me'
    params = {
        'access_token': token,
        'fields': 'name,id,email'
    }
    data = requests.get(url, params=params).json()

    login_session['OAuth'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture'
    params = {
        'access_token': token,
        'redirect': 0,
        'height': 200,
        'width': 200
    }
    data = requests.get(url, params=params).json()

    login_session['picture'] = data["data"]["url"]
    login_session['loggedIn'] = True
    crud.add_OAuthUser(login_session)
    return 'Logged In'


# Facebook OAuth Logout
@facebook.route('/fb_Logout')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['access_token']
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['OAuth']
    login_session['loggedIn'] = False
    return redirect('/')