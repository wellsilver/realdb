key_file=open("keys.txt","r")
keys=key_file.readlines()
key_file.close()

from flask import Flask,request
import os
app = Flask('app')

"""
doci doci

send:
mod: 
get (ret is the value, dat ignored),
set (set row,key to dat),
or new (add a new row)
{
  "pswd":"",
  "mod":"get",
  "row":"",
  "key":"",
  "dat":""
}
{"pswd":"","mod":"get","row":"","key":"","dat":""}

return:
error: noret,file_fail,invalid_key,success
{
  "error":"",
  "ret":""
}
{"error":"", "ret":""}
"""

@app.route('/',methods=['GET','POST'])
def index():
  if request.method == "GET":
    f=open("index.html","r")
    a=f.read()
    f.close()
    return a
  c=request.get_json()
  global keys
  if c['pswd'] not in keys:
    return {'error':"invalid_key","ret":""}
  if c['mod']=="get":
    try:
      f=open("data/"+c['row']+'/'+c['key'],"r")
      dat=f.read()
      f.close()
    except:
      return {"error":"file_fail","ret":""}
    return {"error":"success","ret":dat}
  if c['mod']=="set":
    try:
      f=open("data/"+c['row']+'/'+c['key'],"w")
      f.write(c['dat'])
      f.close()
    except:
      return {"error":"file_fail","ret":""}
    return {"error":"success","ret":"Modified succesfully"}
  if c['mod']=="new":
    o=os.listdir("data/default")
    os.mkdir("data/"+c['dat'])
    for i in o:
      open("data/"+c['dat']+'/'+i,"x").close()
  return {'error':"noret","ret":""}

app.run(host='0.0.0.0', port=80)
