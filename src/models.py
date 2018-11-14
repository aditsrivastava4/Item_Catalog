from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha256

Base = declarative_base()


class User(Base):
	"""
	class User will store data of users how sign up or login without any OAuth.

	Parameters

	username: Store Username(String)

	email: Store user Email(String)

	password_hash: Store hashed password(String)

	api_key: Store API key(String)

	Functions

	hash_password(password)

	  Takes a parameter password(String) as input and
	  hash it using passlib.hash.pbkdf2_sha256 and store it in password_hash.
	verify_password(password)

	  Takes a parameter password(String) as input and
	  verify it if matches the stored password_hash using passlib.hash.pbkdf2_sha256.

	"""
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String)
	email = Column(String)
	password_hash = Column(String(200))
	api_key = Column(String(32), nullable=True)

	def hash_password(self, password):
		self.password_hash = pbkdf2_sha256.hash(password)

	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password_hash)


class OAuth_User(Base):
	"""
	class OAuth_User will store data of users how login with any OAuth service.

	Parameters

	username: Store Username(String)

	email: Store user Email(String)

	picture: Store the link to user profile picture(String)

	oauth: Store the OAuth service user used(String)

	api_key: Store API key(String)
	"""
	__tablename__ = 'oauth_user'
	id = Column(Integer, primary_key=True)
	username = Column(String)
	email = Column(String)
	picture = Column(String(250))
	oauth = Column(String)
	api_key = Column(String(32), nullable=True)

class Category(Base):
	"""
	class Category will store the category name.

	Parameters

	name: Store the name of category(String)

	Functions

	serialize()

	  Used to convert data in JSON format.
	"""
	__tablename__ = 'category'
	id = Column(Integer, primary_key = True)
	name = Column(String)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'category': self.name,
		}


class Category_Items(Base):
	"""
	class Category_Item will store the items detail.

	Parameters

	item: Store the name of the item(String)

	description: Store the description of the item(String)

	author: Store the author of the item(String)

	publisher: Store the publisher of the item(String)

	category_id: Store the Foreign Key from the Category the item is related to(Integer)

	category: Will create the relationship between Category_Item and Category

	Functions

	serialize()

	  Used to convert data in JSON format.
	"""
	__tablename__ = 'category_items'

	item_id = Column(Integer, primary_key = True)
	item = Column(String)
	description = Column(String)
	author = Column(String)
	publisher = Column(String)

	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship('Category')

	@property
	def serialize(self):
		return {
			'item_id': self.item_id,
			'item': self.item,
			'author': self.author,
			'publisher': self.publisher,
			'description': self.description,
		}

engine = create_engine('postgresql://testDemo2:{}@localhost/demoDB'.format('94532@dit'))
Base.metadata.create_all(engine)