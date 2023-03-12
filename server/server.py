import os
import time
import socketio # pip install python-socketio
import eventlet # pip install eventlet
import json
import logging

if "data" not in os.listdir(os.getcwd()):
  os.mkdir("data")

if "storage keyvalue" not in os.listdir(os.getcwd()+"/data"):
  os.mkdir("data/storage keyvalue")

startedon=int(time.time())

jsondefault___ = """
{
"keys":["admin"],
"Connection":{
  "Host":"localhost",
  "Port":4740
}
}
"""

try:
  f=open("settings.json","r")
  settings = json.loads(f.read())
  f.close()
except FileNotFoundError:
  f=open("settings.json","x")
  f.write(jsondefault___)
  f.close()
  settings = json.loads(jsondefault___)
    
def safeify(string:str) -> str:
  newstr = ""
  allowedcharacters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_"]
  for i in string:
    i=i.lower()
    if i in allowedcharacters:
      newstr += i
    else:
      newstr += "_" # replace non normal characters with _
  return newstr

class data:
  def newtable(name:str) -> bool:
    name=safeify(name)
    dir=os.listdir("data")
    if name in dir: return False
    os.mkdir("data/"+name)

class keyvalue:
  def set(name:str,value) -> dict:
    name=safeify(name)
    try:
      f=open("data/storage keyvalue/"+name,"w")
    except FileNotFoundError:
      f=open("data/storage keyvalue/"+name,"x")
    if type(value) is int:
      f.write(chr(2)+"\r"+str(value))
    elif type(value) is str:
      f.write(chr(1)+"\r"+value)
    f.close()
    return {"error":"none"}
  
  def get(name:str) -> dict:
    name=safeify(name)
    try:
      f=open("data/storage keyvalue/"+name,"r")
    except FileNotFoundError:
      return {"error":"doesnt exist"}
    is_ = f.read(1)
    f.read(1) # ignore the \r
    val = f.read()
    f.close()
    if is_ == chr(2): # if its an int
      ret = int(val)
    elif is_ == chr(1):
      ret = str(val)
    return {"error":"none","value":ret}

sio = socketio.Server()

@sio.on("message")
def handlemsg(sid:socketio.Client,msg):
  sio.emit('message',json.dumps((index(json.loads(msg)))))

def index(c:dict): # handle requests self.handler_to_client(handler), self, msg
  if "type" not in c: return {'error':"invalid request"}

  if c['type'] == "ack": # give some info to client
    return {'error':"none",'implementation':"wellsilver/RealDB py",'version':"beta 001",'alivesince':startedon,"extra":{}}

  if c['type'] == "verify": # verify password
    if "key" not in c: return {'error':"invalid request"}
    if c['key'] in settings["keys"]:
      return {'error':"none",'valid':True}
    else:
      return {'error':"none",'valid':False}
  
  if "key" not in c: return {'error':"no key"}
  if c['key'] not in settings["keys"]:
    return {'error':"invalid key"}
  
  if c['type'] == "keyvalue":

    if c['mod'] == "set": # set
      if "name" not in c or "value" not in c: return {'error':"invalid request"}
      return keyvalue.set(c['name'],c['value'])
    
    if c['mod'] == "get": # get
      if "name" not in c: return {'error':"invalid request"}
      return keyvalue.get(c['name'])
  
  return {'error':"none"}

app = socketio.WSGIApp(sio)
eventlet.wsgi.server(eventlet.listen((settings["Connection"]["Host"], settings["Connection"]["Port"])), app)