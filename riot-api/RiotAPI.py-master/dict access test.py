from ast import literal_eval

dict = {"edward132":{"id":276318,"name":"edward132","profileIconId":664,"summonerLevel":30,"revisionDate":1402049193000}}
swag = dict["edward132"]["id"]
print swag

# more dict tests

new_content = ""
new_content.join(dict)
print new_content

# pickle test
import cPickle as pickle
favorite_color = {"lion": "yellow", "kitty": "red"}
pickle.dump(favorite_color, open("save.p", "wb" ))

favorite_color = pickle.load(open("save.p", "rb"))
print favorite_color
favorite_color["eel"] = "green"
pickle.dump(favorite_color, open("save.p", "wb" ))
favorite_color = pickle.load(open("save.p", "rb"))
print favorite_color

known = {'edward132': 276318, 'banool': 283723, 'xhkxsilence': 311272}
pickle.dump(known, open("known_ids.p", "wb"))

ids_test = '["id":266:{"active":True,"botEnabled":False,"freeToPlay":False,"botMmEnabled":False,"rankedPlayEnabled":True}]'
dict_ids = literal_eval(ids_test)
