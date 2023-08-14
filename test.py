import realdb
import random

s = realdb.realdb("localhost",4740,"server")

print(s.ack())
s.keyset("T3st.ea", str(random.randbytes(100) ))
print(s.keyget("T3st.ea"))
try:
  s.tablenew("test", {"ID":"int","Name":"str"} )
except ValueError:
  print("table allready existed")
s.rowset("test", {"ID":500,"Name":"Epic"})
print(s.rowread("test", 500))

s.close()