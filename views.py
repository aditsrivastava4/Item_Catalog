from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import session as login_session
import crud
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']


app = Flask(__name__)


@app.route('/')
def index():
	categories = crud.getCategory()
	if not login_session:
		login_session['loggedIn'] = False
	#print(login_session)
	return render_template('catalog.html', categories = categories, loggedIn = login_session['loggedIn'])







@app.route('/login')
def login():
	if login_session['loggedIn']:
		return redirect('/')
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


@app.route('/G_OAuth', methods=['GET','POST'])
def googleLogin():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return redirect('/login')

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
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print("Token's client ID does not match app's.")
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								 200)
		response.headers['Content-Type'] = 'application/json'
		return response

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
	#print(login_session)
	crud.add_OAuthUser(login_session)
	return 'Logged In'




@app.route('/logout')
def logout():
	if login_session['loggedIn']:
		if login_session['OAuth'] == 'google':
			return redirect('/G_Logout')
		if login_session['OAuth'] == 'facebook':
			return redirect('/fb_Logout')
	return redirect('/')

@app.route('/G_Logout')
def googleLogout():
	access_token = login_session.get('access_token')
	if access_token is None:
		print('Access Token is None', access_token)
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return redirect('/login')
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print('result is ')
	print(result)
	if result['status'] == '200':
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['OAuth']
		login_session['loggedIn'] = False
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return redirect('/')
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


# Facebook OAuth
@app.route('/fb_OAuth', methods=['POST'])
def facebookLogin():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return redirect('/login')

	access_token = request.data.decode()
	#print("access token received %s " % access_token)


	app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
		'web']['app_id']
	app_secret = json.loads(
		open('fb_client_secrets.json', 'r').read())['web']['app_secret']
	url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
		app_id, app_secret, access_token)
	h = httplib2.Http()
	result = h.request(url, 'GET')[1].decode()


	#print(app_id,' =============== ', app_secret,' =============== ', access_token)

	# Use token to get user info from API
	userinfo_url = "https://graph.facebook.com/v2.8/me"
	token = result.split(',')[0].split(':')[1].replace('"', '')

	url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]
	# print "url sent for API access:%s"% url
	# print "API JSON result: %s" % result
	data = json.loads(result.decode('utf8'))
	#print(data)
	login_session['OAuth'] = 'facebook'
	login_session['username'] = data["name"]
	login_session['email'] = data["email"]
	login_session['facebook_id'] = data["id"]

	# The token must be stored in the login_session in order to properly logout
	login_session['access_token'] = token

	# Get user picture
	url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]
	data = json.loads(result.decode())

	login_session['picture'] = data["data"]["url"]
	login_session['loggedIn'] = True
	crud.add_OAuthUser(login_session)
	return 'Logged In'



@app.route('/fb_Logout')
def fbdisconnect():
	facebook_id = login_session['facebook_id']
	# The access token must me included to successfully logout
	access_token = login_session['access_token']
	url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
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




@app.route('/catalog/<string:category>/items')
def items(category):
	return category

@app.route('/catalog/<string:category>/newItem')
def new_item(category):
	return category

@app.route('/catalog/<string:category>/<string:item>')
def itemsList(category, item):
	return '{} = {}'.format(category,item)

@app.route('/catalog/<string:category>/<string:item>/edit')
def edit_items(category, item):
	return '{} = {}'.format(category,item)

@app.route('/catalog/<string:category>/<string:item>/delete')
def delete_items(category, item):
	return '{} = {}'.format(category,item)

# @app.route('/API')
# @app.route('/API/catalog.json')


if __name__ == '__main__':
	app.secret_key = '_5#y2Ldsfsdf'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)