#coding=utf-8
import requests

s = requests

data={"username":"zhangsan","password":"123",}
r = s.post('http://127.0.0.1:5000/login', data)

print r.status_code
print r.headers['content-type']
print r.encoding
print r.text