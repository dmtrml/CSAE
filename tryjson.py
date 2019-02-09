import json


user = json.loads('{"__type__": "User", "name": "John Smith", "username": "jsmith"}')
print(type(user))
print(user['username'])