  var wrong_category = {
    "response": 404,
    "result": "Category doesn't Exist"
  }
  $('#wrong_category').text(JSON.stringify(wrong_category, null, 4));

  var wrong_api = {
    "response": 403,
    "result": "Wrong API key"
  }
  $('#wrong_api').text(JSON.stringify(wrong_api, null, 4));





  var items_json = {
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
  items_json = JSON.stringify(items_json, null, 4)
  $('#items_json').append(items_json);


  var category_json = {
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
  category_json = JSON.stringify(category_json, null, 4)
  $('#category_json').append(category_json);


  var catalog_json = {
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
     ]
    }
  catalog_json = JSON.stringify(catalog_json, null, 4)
  $('#catalog_json').append(catalog_json);