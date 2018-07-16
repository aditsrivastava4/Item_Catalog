import requests
import json
import crud


params = {}
params['api_key'] = '981f2af9b62d4e3eac4c8aa4e2ccb8b3'
#Combined+Print+and+E-Book+Fiction
bookCategory_url = '''https://api.nytimes.com/svc/books/v3/lists/names.json'''#?api-key={}'''.format(api_key)
print(params)
bookList_url = '''https://api.nytimes.com/svc/books/v3/lists.json'''

print(bookCategory_url)
data = requests.get(bookCategory_url, params = params)
js = json.loads(data.text)['results']
for x in js:
	print('\n\n',x['list_name'])
	#crud.addCategory(x['list_name'])
	params['list'] = x['list_name']
	

	# d = crud.getItem(category = params['list'])
	# for z in d:
	# 	print(z.item)




	book = requests.get(bookList_url, params = params)
	bJS = json.loads(book.text)['results']
	for y in bJS:
		bookData = {}
		bookData['name'] = y['book_details'][0]['title']
		print(bookData['name'])
		bookData['description'] = y['book_details'][0]['description']
		bookData['author'] = y['book_details'][0]['author']
		bookData['publisher'] = y['book_details'][0]['publisher']
		#crud.addItems(params['list'], bookData)
