from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha256

Base = declarative_base()


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String)
	email = Column(String)
	password_hash = Column(String(64))
	api_key = Column(String(32), nullable=True)

	def hash_password(self, password):
		self.password_hash = pbkdf2_sha256.hash(password)

	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password_hash)


class OAuth_User(Base):
	__tablename__ = 'oauth_user'
	id = Column(Integer, primary_key=True)
	username = Column(String)
	email = Column(String)
	picture = Column(String(250))
	oauth = Column(String)
	api_key = Column(String(32), nullable=True)

class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key = True)
	name = Column(String)
	#items = relationship('Category_Items', backref = 'category')

	@property
	def serialize(self):
		return {
			'id': self.id,
			'category': self.name,
		}


class Category_Items(Base):
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

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.create_all(engine)