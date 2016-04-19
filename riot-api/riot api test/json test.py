
import json
from urllib import urlopen
from ast import literal_eval

key = "3b39cc75-4cb2-4a2e-9a46-a3f44ebcf532"

query = "https://oce.api.pvp.net/api/lol/oce/v1.3/game/by-summoner/283723/recent?api_key=" + key
raw_data = urlopen(query)
json_data = json.loads(raw_data.readlines()[0]) #Becomes dict
#out = json.dumps(json_data) #Becomes string
out = json_data 
print out, type(out)

for i in out:
    print i

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
print 'DATA:', repr(data)

data_string = json.dumps(data)
print 'JSON:', data_string


"""
import json

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
data_string = json.dumps(data)
print 'ENCODED:', data_string

decoded = json.loads(data_string)
print 'DECODED:', decoded

print 'ORIGINAL:', type(data[0]['b'])
print 'DECODED :', type(decoded[0]['b'])
"""
