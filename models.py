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

class Category(Base):
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
	__tablename__ = 'items'

	item_id = Column(Integer, primary_key = True)
	item = Column(String)
	description = Column(String)

	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

	@property
	def serialize(self):
		return {
			'category_id': self.category.id,
			'category': self.category.name,
			'items': {
				'item_id': self.item_id,
				'item': self.item,
				'description': self.description,
			}
		}

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.create_all(engine)