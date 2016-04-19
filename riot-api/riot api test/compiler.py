import cPickle as pickle
start_dict = {"banool": {"summ_id": 283723, "region": "oce", "played_with": {311272: 0, 276318: 0}}, "jompie": {"summ_id": 293509, "region": "oce", "played_with": {276318: 0}}}
# format is summoner: their id and region, then who they played with. that has a summ_name: [their id, times played]
pickle.dump(start_dict, open("player_tracker_db.p", "wb"))

import urllib2
response = urllib2.urlopen("https://oce.api.pvp.net/api/lol/oce/v1.3/game/by-summoner/293509/recent?api_key=3b39cc75-4cb2-4a2e-9a46-a3f44ebcf532")
html = response.read()
print html.decode('utf-8')
print type(html.decode('utf-8'))
