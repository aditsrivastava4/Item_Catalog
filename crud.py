from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, OAuth_User, Category, Category_Items
import json
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

def getCategory():
	session = DBSession()
	data = session.query(Category).all()
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
