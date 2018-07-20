# API Endpoint

The Book Catalog API endpoint is for the developer's who wants to create a web app related to books categories or their details. The database of this API is updated frequently so developer's can get latest informations.


## Endpoint URL's
* http://localhost:5000/API/catalog.json
* http://localhost:5000/API/catalog/category.json
* http://localhost:5000/API/&lt;string:category&gt;/items.json

### Parameters
* **api_key** <br>
*Datatype* : string<br>
A set of random string which user can get from [Book Catalog API](http://localhost:5000/API) by logging in and generating. **api_key** is required for all API request
*  **category**<br>
*Datatype* : string<br>
Book category which user can get from [Book Category](http://localhost:5000/) or by sending a API request to [Book Category API](http://localhost:5000/API/catalog/category.json)
