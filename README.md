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
