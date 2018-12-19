from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, OAuth_User, Category, Category_Items
import json

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def getCategory(category=None, category_id=None):
    """
    getCategory(category = None, category_id = None)
            Will return all the categories if no parameters are provided
            Parameters
            category: Name of the category whose data is required (String)
                    Will return data of the category whose name is provided
            category_id: ID of the category whose data is required (Integer)
                    Will return data of the category whose ID is provided
    """
    session = DBSession()

    if category is None and category_id is None:
        data = session.query(Category).order_by(Category.name).all()
    else:
        if category_id is None:
            data = session.query(Category).filter_by(
                name=category).one_or_none()
        else:
            data = session.query(Category).filter_by(
                id=category_id).one_or_none()
    session.close_all()
    return data


def add_OAuthUser(user_data):
    """
    add_OAuthUser(user_data)
            Users who log in for first time using OAuth
            are added to the database.
            Parameter
            user_data: Dict
    """
    data = get_OAuthUser(user_data['email'])
    if not data:
        session = DBSession()
        user = OAuth_User(
            username=user_data['username'],
            email=user_data['email'],
            picture=user_data['picture'],
            oauth=user_data['OAuth']
        )
        session.add(user)
        session.commit()
        session.close_all()


def get_OAuthUser(email):
    """
    get_OAuthUser(email)
            Get detail of OAuth users
    """
    session = DBSession()
    data = session.query(OAuth_User).filter_by(email=email).one_or_none()
    session.close_all()
    return data


def get_User(email):
    """
    get_User(email)
            Get detail of local users
    """
    session = DBSession()
    data = session.query(User).filter_by(email=email).one_or_none()
    session.close_all()
    return data


def verify_UserPassword(email, password):
    """
    verify_UserPassword(email, password)
            Verify local users password at the time of login
    """
    session = DBSession()
    data = session.query(User).filter_by(email=email).one_or_none()
    result = data.verify_password(password)
    session.close_all()
    return result


def add_SignUp(user_data):
    """
    add_SignUp(user_data)
            Users who sign up as local user are added to the database
    """
    data = get_User(user_data['email'])
    if not data:
        session = DBSession()
        user = User(
            username=user_data['username'],
            email=user_data['email']
        )
        user.hash_password(user_data['password'])
        session.add(user)
        session.commit()
        session.close_all()


def addCategory(category):
    """
    addCategory(category)
            Add the category to the database
    """
    session = DBSession()
    if not getCategory(category):
        newCategory = Category(name=category)
        session.add(newCategory)
        session.commit()
    session.close_all()


def getItem(category=None, item_id=None, item_name=None):
    """
    getItem(category = None, item_id = None, item_name = None)
            Get the Item detail on the base of anyone
            of the above parameters or it will return 'Data Not Provided'
    """
    if category is None and item_id is None and item_name is None:
        return 'Data Not Provided'
    else:
        session = DBSession()
        data = None
        if item_id is None and item_name is None:
            category = getCategory(category)
            if category:
                data = session.query(Category_Items).filter_by(
                    category=category).all()

        else:
            if item_name is None:
                data = session.query(Category_Items).filter_by(
                    item_id=item_id).one_or_none()
            else:
                data = session.query(Category_Items).filter_by(
                    item=item_name).one_or_none()

        session.close_all()
        return data


def addItems(category, itemData):
    """
    addItems(category, itemData)
            Add the new Item to the database and
            link it to category it is related to.
    """
    category = getCategory(category=category)
    if category:
        if not getItem(item_name=itemData['name']):
            session = DBSession()
            item = Category_Items(
                item=itemData['name'],
                description=itemData['description'],
                author=itemData['author'],
                publisher=itemData['publisher'],
                category=category
            )
            session.add(item)
            session.commit()
            session.close_all()
            return getItem(item_name=itemData['name']).item_id
        else:
            return 'Item already exist'
    else:
        return 'Category doesnot exist'


def updateItem(form_data, item_id):
    """
    updateItem(form_data, item_id)
            Update the details of existing item
    """
    item = getItem(item_id=item_id)

    if item is not None:
        session = DBSession()

        if form_data['title']:
            item.item = form_data['title']

        if form_data['author']:
            item.author = form_data['author']

        if form_data['publisher']:
            item.publisher = form_data['publisher']

        if form_data['description']:
            item.description = form_data['description']

        if form_data['category'] != getCategory(
                category_id=item.category_id).name:
            print(item.category_id)
            item.category_id = getCategory(form_data['category']).id
            print(item.category_id)

        session.add(item)
        session.commit()
        session.close_all()
    else:
        return '''Item Don't Exist'''


def deleteItem(item_id):
    """
    deleteItem(item_id)
            Delete the Item and its details from the database
    """
    item = getItem(item_id=item_id)
    if item is not None:
        session = DBSession()
        session.delete(item)
        session.commit()
        session.close_all()
    else:
        return '''Item Don't Exist'''
    print(item)


def catalog_API():
    """
    catalog_API()
            returns all the data in JSON format
    """
    session = DBSession()
    result = []
    data = session.query(Category).all()
    for y in data:
        cat = y.serialize
        items = session.query(Category_Items).filter_by(category=y).all()
        cat['items'] = [item.serialize for item in items]
        result.append(cat)
    session.close_all()
    return result


def category_API():
    """
    category_API()
            returns all the categories data in JSON format
    """
    session = DBSession()
    categories = session.query(Category).all()
    result = [category.serialize for category in categories]
    session.close_all()
    return result


def item_API(category):
    """
    item_API()
            returns all the items related to a category JSON format
    """
    session = DBSession()
    category = getCategory(category)
    if category is None:
        return None
    items = getItem(category.name)
    category = category.serialize

    category['items'] = [item.serialize for item in items]
    result = category

    session.close_all()
    return result


def addAPI_key(api_key, login_session):
    """
    addAPI_key(api_key, login_session)
            Added the User's or OAuth_User's api_key to their details
    """
    session = DBSession()
    if login_session['OAuth'] == 'local':
        user = get_User(login_session['email'])
        user.api_key = api_key
        session.add(user)
        session.commit()
    else:
        user = get_OAuthUser(login_session['email'])
        user.api_key = api_key
        session.add(user)
        session.commit()
    session.close_all()


def verify_APIkey(api_key):
    """
    verify_APIkey(api_key)
            Verify the api_key of the User or OAuth_User
    """
    session = DBSession()
    local_User = session.query(User).filter_by(api_key=api_key).one_or_none()
    if local_User is not None:
        session.close_all()
        return True

    oauth_User = session.query(OAuth_User).filter_by(
        api_key=api_key).one_or_none()
    if oauth_User is not None:
        session.close_all()
        return True
    session.close_all()
    return False


def get_APIkey(login_session):
    """
    get_APIkey(login_session)
            Get the api_key of the User or OAuth_User
    """
    if login_session['OAuth'] == 'local':
        user = get_User(login_session['email'])
        if user is not None:
            return user.api_key
        return None
    else:
        user = get_OAuthUser(login_session['email'])
        if user is not None:
            return user.api_key
        return None
