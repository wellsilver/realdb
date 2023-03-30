from websocket import create_connection
import json

class realdb:
  def __init__(self,where:str,port:int,auth:str):
    self.auth=auth
    self.sio = create_connection("ws://"+where+":"+str(port))
    self.sio.send(json.dumps({"type":"verify","key":auth}))
    recv = self.sio.recv()
    resp = json.loads(recv)
    if resp["valid"] == False:
      recv=None
      self.sio.disconnect()
      raise PermissionError('Invalid key') 
  
  def close(self): # close the connection
    self.sio.close()
  
  def ack(self) -> dict: # send a ACK request to the server with the server implementation, its version, and how long it has been on, along with extra info that may or may not be included
    self.sio.send(json.dumps({"type":"ack"}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    return resp

  def keyset(self,name:str,value:any) -> None: # set a key in the valuestore
    self.sio.send(json.dumps({"key":self.auth,"type":"keyvalue","mod":"set","name":name,"value":value}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response: \""+resp["error"]+"\"")
    recv = None

  def keyget(self,name:str) -> dict: # get a key from the valuestore
    self.sio.send(json.dumps({"key":self.auth,"type":"keyvalue","mod":"get","name":name}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response: \""+resp["error"]+"\"")
    return resp["value"]

  def tablenew(self,name:str,values:dict) -> None: # rownew("Users",{"id":"int","name":"str","password":"str"})
    self.sio.send(json.dumps({"key":self.auth,"type":"row","mod":"new","name":name,"values":values}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response: \""+resp["error"]+"\"")

  def rowset(self,table:str,values:dict) -> None: # rowset("Users",{"id":5005,"name":"Lucky"})
    global recv
    self.sio.send(json.dumps({"key":self.auth,"type":"row","mod":"set","name":table,"values":values}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response: \""+resp["error"]+"\"")
  
  def rowread(self,name:str,value) -> dict:
    self.sio.send(json.dumps({"key":self.auth,"type":"row","mod":"read","name":name,"value":value}))
    recv= self.sio.recv()
    resp = json.loads(recv)
    if resp["error"]!="none":
      raise ValueError("Server sent error response: \""+resp["error"]+"\"")
    return resp["data"]