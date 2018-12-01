Django and Django REST API JWT example
===
Example with Django+Django REST API with bot for demonstrate 

#### Installation
```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Using bot
Modify `test_bot_settings.py`
Also you need chromium driver installed
```bash
sudo apt-get install chromium-chromedriver
source venv/bin/activate
python test_bot.py
```

#### Access to API
```bash
>>> curl -X GET http://localhost:8000/api/users/
["testuser","testuser2","testuser3"]

>>> curl -X POST -d 'username=testuser4&password=testpass&email=example@mail.com' http://localhost:8000/api/users/
"User created successfully!"

>>> curl -X DELETE -d 'username=testuser4&password=testpass&email=example@mail.com' http://localhost:8000/api/users/
"User deleted successfully!"

>>> curl -X POST -d 'username=testuser4&password=testpass' http://127.0.0.1:8000/api/token/obtain/
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0Mzc0MjI2OCwianRpIjoiNzU5NGQxMzRhODhhNDIyYmIxOTdmOGE5ODRkMzMyZDQiLCJ1c2VyX2lkIjo1OH0.bfqGCNg5Vcytbl0Xstm1eC09Kc6-1YNqnRoR0YYpfQk","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4"}

>>> curl -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4" http://127.0.0.1:8000/api/posts/
["title article","title article2", "title article3"]

>>> curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4" -d 'title=some_article&text=asdasd' http://127.0.0.1:8000/api/posts/
"Post created successfully!"

>>> curl -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4" -d 'title=some_article' http://127.0.0.1:8000/api/posts/
"Post deleted successfully!"

>>> curl -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4" http://127.0.0.1:8000/api/posts/some_article/
"Post have 0 like"

>>> curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4"  http://127.0.0.1:8000/api/posts/some_article/
"Post liked"

>>> curl -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQzNjYzMDY4LCJqdGkiOiJkMjcyYThjODAyNDc0YzgwYjMyZDU5MmVkZDA0MDcwZiIsInVzZXJfaWQiOjU4fQ.UrjvhKStAozXQPOvQo4sHUca-EiAJQHrp7i2RcPxGO4"  http://127.0.0.1:8000/api/posts/some_article/
"Post unliked"
```