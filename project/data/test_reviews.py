from requests import post, get, delete

print(get('http://localhost:5000/api/v2/add_reviews').json())

print(get('http://localhost:5000/api/v2/add_reviews/1').json())

print(get('http://localhost:5000/api/v2/add_reviews/999').json())

print(post('http://localhost:5000/api/v2/add_reviews',
           json={'id': 1}).json())

print(post('http://localhost:5000/api/v2/add_reviews/999',
           json={'id': 1, 'title': 'gregregre'}).json())

print(delete('http://localhost:5000/api/v2/add_reviews/1').json())

print(delete('http://localhost:5000/api/v2/add_reviews/999').json())
