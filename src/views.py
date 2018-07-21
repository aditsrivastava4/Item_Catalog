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





@app.route('/signup', methods = ['GET','POST'])
def signup():
	if request.method == 'GET':
		if login_session['loggedIn']:
			return redirect('/')
		return render_template('signup.html', loggedIn = login_session['loggedIn'])
	if request.method == 'POST':
		data = request.form
		login_session['OAuth'] = 'local'
		login_session['username'] = data['username']
		login_session['password'] = data['password']
		login_session['email'] = data['email']
		login_session['loggedIn'] = True
		#print(login_session)
		crud.add_SignUp(login_session)
		del login_session['password']
		return redirect('/')


@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		if login_session['loggedIn']:
			return redirect('/')
		state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
		login_session['state'] = state
		return render_template('login.html', STATE=state)
	if request.method == 'POST':
		data = request.form
		if login_session['state'] != data['state']:
			response = make_response(json.dumps('Invalid state parameter.'), 401)
			response.headers['Content-Type'] = 'application/json'
			return redirect('/login')

		if not crud.get_User(data['email']):
			response = make_response(json.dumps('User Does not Exist'), 404)
			response.headers['Content-Type'] = 'application/json'
			return response

		if crud.verify_UserPassword(data['email'], data['password']):
			login_session['OAuth'] = 'local'
			login_session['username'] = crud.get_User(data['email']).username
			login_session['email'] = data['email']
			login_session['loggedIn'] = True
		
		return redirect('/')

# Google OAuth Login
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

		if login_session['OAuth'] == 'local':
			del login_session['username']
			del login_session['email']
			del login_session['OAuth']
			login_session['loggedIn'] = False
	return redirect('/')

# Google OAuth Logout
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
	#print('result is ')
	#print(result)
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


# Facebook OAuth Login
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


# Facebook OAuth Logout
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
def itemsList(category):
	category = category.replace('+', ' ')
	data = crud.getItem(category = category)

	return render_template(
		'itemsList.html',
		items = data, 
		category = category, 
		loggedIn = login_session['loggedIn']
	)

@app.route('/catalog/<string:category>/<int:item_id>')
def item(category, item_id):
	data = crud.getItem(item_id = item_id)

	return render_template(
		'item.html',
		item = data,
		loggedIn = login_session['loggedIn']
	)

@app.route('/catalog/<string:category>/<int:item_id>/edit', methods = ['GET','POST'])
def edit_items(category, item_id):
	if login_session['loggedIn']:
		data = crud.getItem(item_id = item_id)
		if request.method == 'GET':
			categories = crud.getCategory()

			return render_template(
				'editItem.html',
				item = data,
				categories = categories,
				selectedCategory = category,
				loggedIn = login_session['loggedIn']
			)

		if request.method == 'POST':
			form_data = request.form
			crud.updateItem(form_data, item_id)
			return redirect('/catalog/{}/{}'.format(category, item_id))
	else:
		return redirect('/login')


@app.route('/catalog/<string:category>/<int:item_id>/delete', methods = ['GET','POST'])
def delete_items(category, item_id):

	if login_session['loggedIn']:
		data = crud.getItem(item_id = item_id)
		if request.method == 'GET':
			return render_template(
				'deleteItem.html',
				item = data.item,
				loggedIn = login_session['loggedIn']
			)

		if request.method == 'POST':
			form_data = request.form
			crud.deleteItem(item_id)
			return redirect('/catalog/{}/items'.format(category))
	else:
		return redirect('/login')

@app.route('/catalog/<string:category>/new', methods = ['GET','POST'])
def new_item(category):
	category = category.replace('+', ' ')
	if login_session['loggedIn']:
		if request.method == 'GET':
			category = crud.getCategory(category = category)

			return render_template(
				'addItem.html',
				category = category.name,
				loggedIn = login_session['loggedIn']
			)

		if request.method == 'POST':
			form_data = request.form
			print(form_data)
			item_id = crud.addItems(category, form_data)
			return redirect('/catalog/{}/{}'.format(category, item_id))
	else:
		return redirect('/login')


@app.route('/API',methods = ['GET', 'POST'])
def api():
	if request.method == 'POST':
		form = request.form
		print(form)
		if crud.verify_APIkey(form['api_key']):
			if form['api_type'] == 'Catalog.json':
				return redirect(url_for('catalog_json', api_key = form['api_key']))

			if form['api_type'] == 'Category.json':
				return redirect(url_for('category_json', api_key = form['api_key']))

			if form['api_type'] == 'Category_Items.json':
				category = form['category'].replace(' ', '+')
				return redirect(url_for('item_json', category = category, api_key = form['api_key']))


	if request.method == 'GET':
		if login_session['loggedIn']:
			api_key = crud.get_APIkey(login_session)
			return render_template('api.html', loggedIn = login_session['loggedIn'], api_key = api_key)
		return render_template('api.html', loggedIn = login_session['loggedIn'])



@app.route('/API/register', methods = ['POST'])
def register():
	if login_session['loggedIn']:
		api_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
		crud.addAPI_key(api_key, login_session)
		print('api_key = ',api_key)
		return api_key
	else:
		return redirect('/login')



@app.route('/API/catalog.json')
def catalog_json():
	args = request.args
	if args:
		if crud.verify_APIkey(args['api_key']):
			results = {'response': 200, 'results': crud.catalog_API()}
			return jsonify(results)
	return jsonify({'response': 403, 'result':'Wrong API key'})

@app.route('/API/catalog/category.json', methods = ['GET','POST'])
def category_json():
	if request.method == 'POST':
		print(request.form)
		categories = jsonify(crud.category_API())
		return categories

	if request.method == 'GET':
		args = request.args
		if args:
			if crud.verify_APIkey(args['api_key']):
				results = {'response': 200, 'results': crud.category_API()}
				return jsonify(results)
		return jsonify({'response': 403, 'result':'Wrong API key'})

@app.route('/API/<string:category>/items.json')
def item_json(category):
	category = category.replace('+', ' ')
	args = request.args
	if args:
		if crud.verify_APIkey(args['api_key']):
			items = crud.item_API(category)
			if items == None:
				return jsonify({'response': 404, 'result':'''Category doesn't Exist'''})

			results = {'response': 200, 'results': items}
			return jsonify(results)
	return jsonify({'response': 403, 'result':'Wrong API key'})

if __name__ == '__main__':
	app.secret_key = '_5#y2Ldsfsdf'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)