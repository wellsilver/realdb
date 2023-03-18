# realdb
real, simple, database

# usage

download server.py and run in location of choosing, it will create a ``data folder`` and a ``settings.json`` with the settings

To connect the server, download realdb.py and use

realdb.py example: (showcases all functions)

```python
import realdb

a=realdb("localhost",4740,"admin") # connect to realdb
print(a.ack()) # {'error': 'none', 'implementation': 'wellsilver/RealDB py', 'version': 'beta 001', 'alivesince': 1678592736, 'extra': {}}
a.keyset("Hello World!","Yes.") # set the key "Hello World!" to "Yes."
print(a.keyget("Hello World!")) # get the key "Hello World!" (returns "Yes.":str)
a.keyset("Hello World!",50) # set the key "Hello World!" to an integer 50
print(a.keyget("Hello World!")) # get the key "Hello WOrld!" (returns 50:int)
a.close()
```

# docs

## info

both use socketio, its the only websocket api that worked, but I will change it later.

## keyvalue

### ack

Sends information about the server to the client

| sent | recieved |
| ---- | -------- |
| ``{"type":"ack"}`` | ``{'error': 'none', 'implementation': 'wellsilver/RealDB py', 'version': 'beta 001', 'alivesince': 1678592736, 'extra': {}}`` |

### verify

Verifies whether a key is valid or not

in both examples the only key is called "admin"

| sent | recieved |
| ---- | -------- |
| ``{"type":"{"type":"verify","key":"Im guessing the key"}`` | ``{'error':"none",'valid':False}`` |

| sent | recieved |
| ---- | -------- |
| ``{"type":"{"type":"verify","key":"admin"}`` | ``{'error':"none",'valid':True}`` |

### set

Set avalue in the valuestore to a value

in example there is a single key named "admin"

| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"keyvalue","mod":"set","name":"Hello World!","value":"Yes."}`` | ``{"error":"none"}`` |

### get

Get a value from the valuestore

In the example there is a single key named admin, and in the valuestore there is a value named ``Hello World!`` set to ``Yes.``

| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"keyvalue","mod":"set","name":"Hello World!"}`` | ``{"error":"none","value":"Yes."}`` |

## rows

### new

Create a new table

Primary key size may be limited by host machine, all other keys expand in size infinitely

| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"row","mod":"new","name":"Users","values":{"id":"int","name":"str"}}`` | ``{"error":"none"}`` |

### set

Set values in a table


| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"row","mod":"set","name":"Users","values":values}`` | ``{"error":"none"}`` |

### read

Read all values from table ``<name>`` and row ``<value>``

| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"row","mod":"read","name":"Users","value":"5005"}`` | ``{"error":"none","data":{}}`` |