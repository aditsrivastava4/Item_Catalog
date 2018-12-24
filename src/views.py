from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from flask import session as login_session
import crud
import random
import string

from Google.Google_OAuth import google
# from Facebook.FB_OAuth import facebook

import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__, static_folder='ic_react/build/static', template_folder='ic_react/build')

# registering blueprint
app.register_blueprint(google)
# app.register_blueprint(facebook)


# Home/Index Page
# @app.route('/')
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # categories = crud.getCategory()
    if not login_session:
        login_session['loggedIn'] = False
        login_session['adit'] = 'Sri'
    return render_template('index.html')


# Sign Up local user
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = json.loads(request.data.decode())
        login_session['OAuth'] = 'local'
        login_session['username'] = data['username']
        login_session['password'] = data['password']
        login_session['email'] = data['email']
        login_session['loggedIn'] = True
        crud.add_SignUp(login_session)
        del login_session['password']
        return jsonify({'LoggedIn': True})


# Login page
@app.route('/login', methods=['POST'])
def login():
    # POST request
    if request.method == 'POST':
        data = json.loads(request.data.decode())
        # if login_session['state'] != data['state']:
        #     flash('Invalid State Parameter')
        #     return redirect(url_for('login'))

        if not crud.get_User(data['email']):
            return jsonify({
                'LoggedIn': False,
                'user_exist': False
            })

        if crud.verify_UserPassword(data['email'], data['password']):
            login_session['OAuth'] = 'local'
            login_session['username'] = crud.get_User(data['email']).username
            login_session['email'] = data['email']
            login_session['loggedIn'] = True

        return jsonify({
                'LoggedIn': True,
                'username': login_session['username']
            })


# logout user
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
    return jsonify({
            'logout': True
        })


# Items List Page
@app.route('/catalog/<string:category>/items')
def itemsList(category):
    category = category.replace('+', ' ')
    data = crud.getItem(category=category)

    return render_template(
        'itemsList.html',
        items=data,
        category=category,
        loggedIn=login_session['loggedIn']
    )


# Items Deatil Page
@app.route('/catalog/<string:category>/<int:item_id>')
def item(category, item_id):
    data = crud.getItem(item_id=item_id)

    return render_template(
        'item.html',
        item=data,
        loggedIn=login_session['loggedIn']
    )


# Edit Items Detail Page
@app.route(
    '/catalog/<string:category>/<int:item_id>/edit',
    methods=[
        'GET',
        'POST'])
def edit_items(category, item_id):
    if login_session['loggedIn']:
        data = crud.getItem(item_id=item_id)
        if request.method == 'GET':
            categories = crud.getCategory()

            return render_template(
                'editItem.html',
                item=data,
                categories=categories,
                selectedCategory=category,
                loggedIn=login_session['loggedIn']
            )

        if request.method == 'POST':
            form_data = request.form
            crud.updateItem(form_data, item_id)
            category = form_data['category'].replace(' ', '+')
            return redirect('/catalog/{}/{}'.format(category, item_id))
    else:
        return redirect('/login')


# Delete Item Page
@app.route(
    '/catalog/<string:category>/<int:item_id>/delete',
    methods=[
        'GET',
        'POST'])
def delete_items(category, item_id):

    if login_session['loggedIn']:
        data = crud.getItem(item_id=item_id)
        if request.method == 'GET':
            return render_template(
                'deleteItem.html',
                item=data.item,
                loggedIn=login_session['loggedIn']
            )

        if request.method == 'POST':
            form_data = request.form
            crud.deleteItem(item_id)
            return redirect('/catalog/{}/items'.format(category))
    else:
        return redirect('/login')


# Add new Item page
@app.route('/catalog/<string:category>/new', methods=['GET', 'POST'])
def new_item(category):
    category = category.replace('+', ' ')
    if login_session['loggedIn']:
        if request.method == 'GET':
            category = crud.getCategory(category=category)

            return render_template(
                'addItem.html',
                category=category.name,
                loggedIn=login_session['loggedIn']
            )

        if request.method == 'POST':
            form_data = request.form
            item_id = crud.addItems(category, form_data)
            return redirect('/catalog/{}/{}'.format(category, item_id))
    else:
        return redirect('/login')


# API key and request page
@app.route('/API', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        form = request.form
        if crud.verify_APIkey(form['api_key']):
            if form['api_type'] == 'Catalog.json':
                return redirect(
                    url_for(
                        'catalog_json',
                        api_key=form['api_key']))

            if form['api_type'] == 'Category.json':
                return redirect(
                    url_for(
                        'category_json',
                        api_key=form['api_key']))

            if form['api_type'] == 'Category_Items.json':
                category = form['category'].replace(' ', '+')
                return redirect(
                    url_for(
                        'item_json',
                        category=category,
                        api_key=form['api_key']))

    if request.method == 'GET':
        if login_session['loggedIn']:
            api_key = crud.get_APIkey(login_session)
            return render_template(
                'api.html',
                loggedIn=login_session['loggedIn'],
                api_key=api_key)
        return render_template('api.html', loggedIn=login_session['loggedIn'])


# Register users API key
@app.route('/API/register', methods=['POST'])
def register():
    if login_session['loggedIn']:
        api_key = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in range(32))
        crud.addAPI_key(api_key, login_session)
        return api_key
    else:
        return redirect('/login')


# Request catalog.json API
@app.route('/API/catalog.json')
def catalog_json():
    # args = request.args
    # if args:
        # if crud.verify_APIkey(args['api_key']):
    results = {'response': 200, 'results': crud.catalog_API()}
    return jsonify(results)
    # return jsonify({'response': 403, 'result': 'Wrong API key'})


# Request category.json API
@app.route('/API/catalog/category.json', methods=['GET', 'POST'])
def category_json():
    # if request.method == 'POST':
    #     print(request.form)
    #     categories = jsonify(crud.category_API())
    #     return categories

    if request.method == 'GET':
        # args = request.args
        # if args:
        #     if crud.verify_APIkey(args['api_key']):
        results = {'response': 200, 'results': crud.category_API()}
        # print(crud.category_API())
        return jsonify(results)
        # return jsonify({'response': 403, 'result': 'Wrong API key'})


#  Request item.json API
@app.route('/API/<string:category>/items.json')
def item_json(category):
    category = category.replace('+', ' ')
    args = request.args
    if args:
        if crud.verify_APIkey(args['api_key']):
            items = crud.item_API(category)
            if items is None:
                return jsonify({'response': 404,
                                'result': '''Category doesn't Exist'''})

            results = {'response': 200, 'results': items}
            return jsonify(results)
    return jsonify({'response': 403, 'result': 'Wrong API key'})


# API Documentation page
@app.route('/API-doc')
def api_doc():
    return render_template('apiDoc.html', loggedIn=login_session['loggedIn'])


if __name__ == '__main__':
    app.secret_key = '_5#y2Ldsfsdf'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
