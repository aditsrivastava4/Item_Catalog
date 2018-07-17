from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, OAuth_User, Category, Category_Items
import json

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

def getCategory(category = None, category_id = None):
	session = DBSession()

	if category == None and category_id == None:
		data = session.query(Category).order_by(Category.name).all()
	else:
		if category_id == None:
			data = session.query(Category).filter_by(name = category).one_or_none()
		else:
			data = session.query(Category).filter_by(id = category_id).one_or_none()
	session.close_all()
	return data

def add_OAuthUser(user_data):
	data = get_OAuthUser(user_data['email'])
	if not data:
		session = DBSession()
		#print(user_data['username'],' = ',user_data['email'],' = ',user_data['picture'])
		user = OAuth_User(
			username = user_data['username'],
			email = user_data['email'],
			picture = user_data['picture'],
			oauth = user_data['OAuth']
		)
		session.add(user)
		session.commit()
		session.close_all()

def get_OAuthUser(email):
	session = DBSession()
	data = session.query(OAuth_User).filter_by(email = email).one_or_none()
	session.close_all()
	return data

def get_User(email):
	session = DBSession()
	data = session.query(User).filter_by(email = email).one_or_none()
	session.close_all()
	return data

def verify_UserPassword(email, password):
	session = DBSession()
	data = session.query(User).filter_by(email = email).one_or_none()
	result = data.verify_password(password)
	session.close_all()
	return result

def add_SignUp(user_data):
	data = get_User(user_data['email'])
	if not data:
		session = DBSession()
		#print(user_data['username'],' = ',user_data['email'],' = ',user_data['password'])
		user = User(
			username = user_data['username'],
			email = user_data['email']
		)
		user.hash_password(user_data['password'])
		session.add(user)
		session.commit()
		session.close_all()


def addCategory(category):
	session = DBSession()
	if not getCategory(category):
		newCategory = Category(name = category)
		session.add(newCategory)
		session.commit()
	session.close_all()






def getItem(category = None, item_id = None, item_name = None):
	if category == None and item_id == None and item_name == None:
		return 'Data Not Provided'
	else:
		session = DBSession()
		data = None
		if item_id == None and item_name == None:
			category = getCategory(category)
			if category:
				data = session.query(Category_Items).filter_by(category = category).all()

		else:
			if item_name == None:
				data = session.query(Category_Items).filter_by(item_id = item_id).one_or_none()
			else:
				data = session.query(Category_Items).filter_by(item = item_name).one_or_none()

		session.close_all()
		return data




def addItems(category, itemData):
	session = DBSession()
	category = getCategory(category)
	if category:
		if not getItem(item_name = itemData['name']):
			item = Category_Items(
				item = itemData['name'],
				description = itemData['description'],
				author = itemData['author'],
				publisher = itemData['publisher'],
				category = category
			)
			session.add(item)
			session.commit()
		else:
			session.close_all()
			return 'Item already exist'
	else:
		session.close_all()
		return 'Category doesnot exist'
	session.close_all()



def updateItem(form_data, item_id):
	item = getItem(item_id = item_id)

	if item != None:
		session = DBSession()

		if form_data['title']:
			item.item = form_data['title']

		if form_data['author']:
			item.author = form_data['author']

		if form_data['publisher']:
			item.publisher = form_data['publisher']

		if form_data['description']:
			item.description = form_data['description']

		#print(form_data['category'])
		# print(getCategory(category_id = item.category_id).name)

		if form_data['category'] != getCategory(category_id = item.category_id).name:
			print(item.category_id)
			item.category_id = getCategory(form_data['category']).id
			print(item.category_id)


		session.add(item)
		session.commit()
		session.close_all()
	else:
		return '''Item Don't Exist'''

def deleteItem(item_id):
	item = getItem(item_id = item_id)
	if item != None:
		session = DBSession()
		session.delete(item)
		session.commit()
		session.close_all()
	else:
		return '''Item Don't Exist'''
	print(item)

# def dataA():
# 	session = DBSession()
# 	result = {'response': 200, 'result': []}
# 	data = session.query(Category).all()
# 	for y in data:
# 		cat = y.serialize
# 		it = session.query(Category_Items).filter_by(category = y).all()

# 		cat['items'] = [item.serialize for item in it]
# 		result['result'].append(cat)
# 	session.close_all()
# 	return result