# Item Catalog Project

This project is to create a website that shows the list of categories(Book Categories) and each category has a list of Items related to it. User's can modify(edit/delete) those items and also add new items. The site has [API Endpoint](API.md) for developers.

## Modules
* models.py
* crud.py
* AddData.py
* views.py

### 1. models.py
* **User**
> class User will store data of users how sign up or login without any OAuth.
>
> 	**Parameters**
>
> 	**username**: Store Username(String)
>
> 	**email**: Store user Email(String)
>
> 	**password_hash**: Store hashed password(String)
>
> 	**api_key**: Store API key(String)
>
> 	**Functions**
>
> 	**hash_password(password)**
>
> 		Takes a parameter password(String) as input and
> 		hash it using passlib.hash.pbkdf2_sha256 and store it in password_hash.
> 	**verify_password(password)**
>
> 		Takes a parameter password(String) as input and
> 		verify it if matches the stored password_hash using passlib.hash.pbkdf2_sha256.
<br>

* **OAuth_User**
> class OAuth_User will store data of users how login with any OAuth service.
>
> 	**Parameters**
>
> 	**username**: Store Username(String)
>
> 	**email**: Store user Email(String)
>
> 	**picture**: Store the link to user profile picture(String)
>
> 	**oauth**: Store the OAuth service user used(String)
>
> 	**api_key**: Store API key(String)
>
<br>

* **Category**
> class Category will store the category name.
>
> 	**Parameters**
>
> 	**name**: Store the name of category(String)
>
> 	**Functions**
>
> 	**serialize()**
>
> 		Used to convert data in JSON format.
>
<br>

* **Category_Item**
> class Category_Item will store the items detail.
>
> 	**Parameters**
>
> 	**item**: Store the name of the item(String)
>
> 	**description**: Store the description of the item(String)
>
> 	**author**: Store the author of the item(String)
>
> 	**publisher**: Store the publisher of the item(String)
>
> 	**category_id**: Store the Foreign Key from the Category the item is related to(Integer)
>
> 	**category**: Will create the relationship between Category_Item and Category
>
> 	**Functions**
>
> 	**serialize()**
>
> 		Used to convert data in JSON format.
>


### 2. crud.py

* **getCategory(category = None, category_id = None)**: Will return all the categories if no parameters are provided.

* **add_OAuthUser(user_data)**: Users who log in for first time using OAuth are added to the database.

* **get_OAuthUser(email)**: Get detail of OAuth users.

* **get_User(email)**: Get detail of local users.

* **verify_UserPassword(email, password)**: Verify local users password at the time of login.

* **add_SignUp(user_data)**: Users who sign up as local user are added to the database.

* **addCategory(category)**: Add the category to the database.

* **getItem(category = None, item_id = None, item_name = None)**: Get the Item detail on the base of anyone of the above parameters or
it will return 'Data Not Provided'.

* **addItems(category, itemData)**: Add the new Item to the database and link it to category it is related to.

* **updateItem(form_data, item_id)**: Update the details of existing item.

* **deleteItem(item_id)**: Delete the Item and its details from the database.

* **catalog_API()**: returns all the data in JSON format.

* **category_API()**: returns all the categories data in JSON format.

* **item_API(category)**: returns all the items related to a category JSON format.

* **addAPI_key(api_key, login_session)**: Added the User's or OAuth_User's api_key to their details.

* **verify_APIkey(api_key)**: Verify the api_key of the User or OAuth_User.

* **get_APIkey(login_session)**: Get the api_key of the User or OAuth_User.


### 3. AddData.py

AddData.py is being used to get book data from [The New York Times Developer's](https://developer.nytimes.com/) Book API and adding it to the database.


### 4. views.py

It is the main module which is used to run the Flask server. All the routes of the website are defined in it.

#### Routes
* ```/``` : Home/Index page(Request type GET).
* ```/signup``` : Sign up page(Request type GET, POST).
* ```/login``` : Login page(Request type GET, POST).
* ```/logout``` : To Logout user(Request type GET.
* ```/G_OAuth``` : Login user with Google OAuth(Request type POST).
* ```/G_Logout``` : Logout Google OAuth user(Request type GET).
* ```/fb_OAuth``` : Login user with Facebook OAuth(Request type POST).
* ```/fb_Logout``` : Logout Facebook OAuth user(Request type GET).
* ```/catalog/<string:category>/items``` : Items List page(Request type GET).
* ```/catalog/<string:category>/<int:item_id>``` : Items Detail page(Request type GET).
* ```/catalog/<string:category>/<int:item_id>/edit``` : Edit Items Detail page(Request type GET, POST).
* ```/catalog/<string:category>/<int:item_id>/delete``` : Delete Item(Request type GET, POST).
* ```/catalog/<string:category>/new``` : Add New Item page(Request type GET, POST).
* ```/API``` : API key and request page(Request type GET, POST).
* ```/API/register``` : Register users API key(Request type POST).
* ```/API/catalog.json``` : Request catalog.json API(Request type GET).
* ```/API/catalog/category.json``` : Request category.json API(Request type GET, POST).
* ```/API/<string:category>/items.json``` : Request item.json API(Request type GET).
* ```/API-doc``` : API Documentation page(Request type GET).


## Dependencies

* **flask** version 1.0.2
* **oauth2client** version 4.1.2
* **httplib2** version 0.11.3
* **requests** version 2.19.1
* **SQLAlchemy** version 1.2.8
* **passlib** version 1.7.1


## Templates
* **index.html** : Base Template for all web pages.
* **catalog.html** : Home template.
* **itemsList.html** : List of Items template.
* **item.html** : Item Detail template.
* **editItem.html** : Edit item template.
* **deleteItem.html** : Delete item template
* **addItem.html** : Add item template.
* **signup.html** : Sign Up page template.
* **login.html** : Login page template.
* **apiDoc.html** : API Endpoint Documentation template.
* **api.html** : API endpoint template.


## Static
### Javascript
* **api_doc.js** : Javascript for API Documentation.
* **api.js** : Javascript for API Endpoint request page.
