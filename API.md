# API Endpoint

The Book Catalog API endpoint is for the developer's who wants to create a web app related to books categories or their details. The database of this API is updated frequently so developer's can get latest informations.


## Endpoint URL's
* http://localhost:5000/API/catalog.json
* http://localhost:5000/API/catalog/category.json
* http://localhost:5000/API/&lt;string:category&gt;/items.json

### Parameters
* **api_key** <br>
*Datatype* : string<br>
A set of random string which user can get from [Book Catalog API](http://localhost:5000/API) by logging in and generating the API key. **api_key** is required for all API request.
*  **category**<br>
*Datatype* : string<br>
Book category which user can get from [Book Category](http://localhost:5000/) or by sending a API request to [Book Category API](http://localhost:5000/API/catalog/category.json)

### Request
User has to send **GET** request to access API

## Response Format
* For http://localhost:5000/API/catalog.json?api_key=api_key

```
{
  "response": 200,
  "results": [
    {
      "category": "Combined Print and E-Book Fiction",
      "id": 1,
      "items": [
        {
          "author": "Bill Clinton and James Patterson",
          "description": "President Jonathan Duncan, a Gulf War veteran and widower, takes on adversaries at home and abroad.",
          "item": "THE PRESIDENT IS MISSING",
          "item_id": 1,
          "publisher": "Little, Brown and Knopf"
        },
        {
          "author": "Gillian Flynn",
          "description": "After a stay at a psychiatric hospital, a reporter returns (reluctantly) to her hometown to cover the murders of two girls.",
          "item": "SHARP OBJECTS",
          "item_id": 2,
          "publisher": "Broadway"
        }
      ]
    },
    {
      "category": "Combined Print and E-Book Nonfiction",
      "id": 2,
      "items": [
        {
          "author": "Tara Westover",
          "description": "The daughter of survivalists, who is kept out of school, educates herself enough to leave home for university.",
          "item": "EDUCATED",
          "item_id": 16,
          "publisher": "Random House"
        },
        {
          "author": "Anthony Bourdain",
          "description": "A memoir-expos\u00e9 of the restaurant world. Originally published in 2000.",
          "item": "KITCHEN CONFIDENTIAL",
          "item_id": 17,
          "publisher": "Ecco"
        }
      ]
    }
  }

```

* For http://localhost:5000/API/catalog/category.json?api_key=api_key

```
{
  "response": 200,
  "results": [
    {
      "category": "Combined Print and E-Book Fiction",
      "id": 1
    },
    {
      "category": "Combined Print and E-Book Nonfiction",
      "id": 2
    }
  ]
}
```

* For http://localhost:5000/API/Paperback+Nonfiction/items.json?api_key=api_key

```
{
  "response": 200,
  "results": {
    "category": "Paperback Nonfiction",
    "id": 7,
    "items": [
      {
        "author": "Malcolm Gladwell",
        "description": "Why some people succeed \u2014 it has to do with luck and opportunities as well as talent.",
        "item": "OUTLIERS",
        "item_id": 68,
        "publisher": "Back Bay/Little, Brown"
      },
      {
        "author": "Jeannette Walls",
        "description": "The author recalls a bizarre childhood during which she and her siblings were constantly moved from one bleak place to another.",
        "item": "THE GLASS CASTLE",
        "item_id": 69,
        "publisher": "Scribner"
      }
    ]
  }
}
```

#### Error Response
* For wrong API key

```
{
  "response": 403,
  "result": "Wrong API key"
}
```
* For wrong category

```
{
  "response": 404,
  "result": "Category doesn't Exist"
}
```


### Access via Python code

```
import requests
api_key = 'Your-API-KEY'
requests.get('http://localhost:5000/API/catalog.json', params={'api_key':api_key}).json()
```
