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
