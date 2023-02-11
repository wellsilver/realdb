# realdb
real, simple, database

To try out clone the server and run server.py then connect to it from http and you will see this 

![image](https://user-images.githubusercontent.com/67511181/205740385-a74e9ea9-9966-4a9e-8c96-4e0bea0cefcb.png)

The default password is ``admin`` you can set this to whatever you like and add more in keys.txt (they are separated by newline)

### how??

Heres a little class (client.py) in python that connects to it for you

```python
import requests

class real_db:
  def __init__(self,connect:str,key:str):
    self.connect=connect
    self.key=key
  # get the data in row/key, returns this https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
  def get(self,row,key):
    return requests.post(self.connect,json={"pswd":self.key,"mod":"get","row":row,"key":key})
  # set the data in row/key to data, returns this https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
  def set(self,row,key,data):
    return requests.post(self.connect,json={"pswd":self.key,"mod":"set","row":row,"key":key,"dat":data})
  # uses the "default" row to make a new row with name as data
  def new(self,data):
    return requests.post(self.connect,json={"pswd":self.key,"mod":"set","dat":data})
    
```
    
Its dead simple, the server itself consists of ``POST`` requests to a server, with the modifier "get" "set" or "new"

``get``

Get gets the data in ``data/<row>/<key>`` and returns it.

``set``

Set sets the data in ``data/<row>/<key>`` to ``dat`` and returns a success message

``new``

New makes a new row in the database with the name of ``dat``
