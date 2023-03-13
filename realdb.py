import socketio
import json

global recv
recv = None

def siomsg(msg): # this is a workaround, socketio has no recieve, only recieve events.
  global recv
  recv = msg

class realdb:
  def __init__(self,where:str,port:int,auth:str):
    global recv
    self.auth=auth
    self.sio = socketio.Client()
    self.sio.connect('http://'+where+":"+str(port))
    self.sid = self.sio.get_sid()
    self.sio.on("message",siomsg)
    self.sio.send(json.dumps({"type":"verify","key":auth}))
    while recv == None:
      pass
    resp = json.loads(recv)
    if resp["valid"] == False:
      recv=None
      self.sio.disconnect()
      raise PermissionError('Invalid key') 
    recv=None
  
  def close(self): # close the connection
    self.sio.disconnect()
  
  def ack(self) -> dict: # send a ACK request to the server with the server implementation, its version, and how long it has been on, along with extra info that may or may not be included
    global recv
    self.sio.send(json.dumps({"type":"ack"}))
    while recv==None:
      pass
    resp = json.loads(recv)
    recv = None
    return resp

  def set(self,name:str,value:any) -> None: # set a key in the valuestore
    global recv
    self.sio.send(json.dumps({"key":self.auth,"type":"keyvalue","mod":"set","name":name,"value":value}))
    while recv == None:
      pass
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response "+resp["error"])
    recv = None

  def get(self,name:str) -> any: # get a key from the valuestore
    global recv
    self.sio.send(json.dumps({"key":self.auth,"type":"keyvalue","mod":"get","name":name}))
    while recv == None:
      pass
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response "+resp["error"])
    return resp["value"]
