import os
import time
import websocket_server
import json
import logging

if "data" not in os.listdir(os.getcwd()):
  os.mkdir("data")

if "storage keyvalue" not in os.listdir(os.getcwd()+"/data"):
  os.mkdir("data/storage keyvalue")

if "storage rows" not in os.listdir(os.getcwd()+"/data"):
  os.mkdir("data/storage rows")

startedon=int(time.time())

jsondefault___ = """
{
"keys":["server"],
"sync":"sync",
"Connection":{
  "Host":"localhost",
  "Port":4740
},
"syncmode":"replicate",
"syncwith":{
  "localhost":4741
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

if settings["keys"][0] == "admin":
  print("default key is present, change in settings.json")

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

def sync():
  pass

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

def _rowsparsedefaultsraw(txt) -> dict:
  lines = txt.split("\n")
  ret = {}

  for i in lines:
    types = i.split(chr(4))
    if len(types)<2:
      continue
    ret[types[0]] = types[1]
  
  return ret

class rows:
  def new(name:str,values:dict):
    name = safeify(name)
    dir = os.listdir("data/storage rows")

    for n,key in values.items():
      if key == "int":
        continue
      if key == "str":
        continue
      return {"error":f"invalid type {key}"}

    try:
      os.mkdir("data/storage rows/"+name)
    except FileExistsError:
      return {"error":"table allready exists"}
    
    f=open("data/storage rows/"+name+"/defaults","x") #idk what file extension to put so 🤷‍♀️

    for n,key in values.items():
      f.write(f"{n}{chr(4)}{key}\n")
    f.close()

    return {"error":"none"}
  def set(name:str,values:dict):
    name=safeify(name)

    try:
      f=open(f"data/storage rows/{name}/defaults","r")
    except FileNotFoundError:
      return {"error":"doesnt exist"}
    r=_rowsparsedefaultsraw(f.read())
    n=list(r.items())[0] # get primary key
    f.close()

    if n[0] not in values:
      return {"error":"primary key required"}
    
    primarykey = values.get(n[0])
    if n[1] == "str":
      primarykey=safeify(primarykey)
    try:
      os.mkdir(f"data/storage rows/{name}/{primarykey}") # make the directory if it doesnt exist
    except FileExistsError:
      pass

    for nam,i in r.items():
      if nam == n[0]: # first key is the folder name
        continue
      try:
        open(f"data/storage rows/{name}/{primarykey}/{nam}.raw","x").close() # make files if they dont exist
      except FileExistsError: #nothing to be done
        pass
    
    for nam,val in values.items():
      if nam == n[0]: # first key is the folder name, nothing special
        continue
      if r.get(nam)!=None: # for some reason "if x in a:" doesnt work
        f=open(f"data/storage rows/{name}/{primarykey}/{nam}.raw","w")
        f.write(str(val))
        f.close()
    
    return {"error":"none"}
  def read(name:str,value):
    name=safeify(name)
    try:
      f=open(f"data/storage rows/{name}/defaults","r")
    except FileNotFoundError:
      return {"error":"doesnt exist"}
    
    r=_rowsparsedefaultsraw(f.read())

    if type(value) == str:
      value=safeify(value)
    else:
      value = str(value)
    
    if value not in os.listdir(f"data/storage rows/{name}"):
      return {"error":"none","data":{}}
    
    primarykey = list(r.items())[0]
    ret = {"error":"none","data":{}}

    for nam,key in r.items():
      if nam == primarykey[0]: continue # ignore primary key
      f=open(f"data/storage rows/{name}/{value}/{nam}.raw","r")
      ret["data"][nam] = f.read()
      f.close()
    
    return ret

sio = websocket_server.WebsocketServer(host=settings["Connection"]["Host"],port=settings["Connection"]["Port"])

@sio.set_fn_message_received
def handlemsg(cli,srvr,msg):
  out = index(json.loads(msg))
  outj = json.dumps(out)

  if out["error"] != None:
    sio.send_message(cli,outj)
  else:
    sync(out)
    sio.send_message(cli,outj)

def index(c:dict): # handle requests self.handler_to_client(handler), self, msg
  if "type" not in c: return {'error':"invalid request"}

  if c['type'] == "ack": # give some info to client
    return {'error':"none",'implementation':"wellsilver/RealDB py",'version':"dev.0",'alivesince':startedon,"extra":{}}

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
  
  if c['type'] == "row":
    if "mod" not in c: return {'error':"invalid request"}

    if c['mod'] == "new":
      if "name" not in c or "values" not in c: return {'error':"invalid request"}
      return rows.new(c['name'],c['values'])
    
    if c['mod'] == "set":
      if "name" not in c or "values" not in c: return {'error':"invalid request"}
      return rows.set(c['name'],c['values'])

    if c['mod'] == "read":
      if "name" not in c or "value" not in c: return {'error':"invalid request"}
      return rows.read(c['name'],c['value'])

  return {'error':"none"}

sio.run_forever()