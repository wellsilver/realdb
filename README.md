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
print(a.keyget("Hello World!")) # get the key "Hello World!" (returns 50:int)
a.close()
```
    
Its dead simple, the server itself consists of ``POST`` requests to a server, with the modifier "get" "set" or "new"

``get``

Get gets the data in ``data/<row>/<key>`` and returns it.


| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"row","mod":"set","name":"Users","values":values}`` | ``{"error":"none"}`` |

### read

Read all values from table ``<name>`` and row ``<value>``

| sent | recieved |
| ---- | -------- |
| ``{"key":"admin","type":"row","mod":"read","name":"Users","value":"5005"}`` | ``{"error":"none","data":{}}`` |