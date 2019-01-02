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

This module handles all database operations that Create Read Update and Delete(**CRUD**).


### 3. AddData.py

AddData.py is being used to get book data from [The New York Times Developer's](https://developer.nytimes.com/) Book API and adding it to the database.


### 4. views.py

It is the main module which is used to run the Flask server. All the routes of the website are defined in it.

## Dependencies

* **flask** version 1.0.2
* **oauth2client** version 4.1.2
* **httplib2** version 0.11.3
* **requests** version 2.19.1
* **SQLAlchemy** version 1.2.8
* **passlib** version 1.7.1
* **psycopg2** version 2.7.6.1


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


## To Run
To run the server open the terminal
First Clone the repo
```
$ git clone https://github.com/aditsrivastava4/Item_Catalog.git
$ cd Item_Catalog/src
$ python3 views.py
```
