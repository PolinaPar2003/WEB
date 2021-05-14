from requests import post, get, delete

print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users/999').json())

print(post('http://localhost:5000/api/v2/users',
           json={'id': 1, 'surname': 'Pupkin'}).json())

print(post('http://localhost:5000/api/v2/users/999',
           json={'id': 1, 'surname': 'Pupkin'}).json())

print(delete('http://localhost:5000/api/v2/users/2').json())

print(delete('http://localhost:5000/api/v2/users/999').json())
