# Nooly "Nools" Noolsworth
# Date Created: 06/06/2014
# Date Modified: 07/06/2014
# PEP8 compliant save for line length in places

"""
Originally used someone else's python calls for the Riot API, but
that was outdated based on region specific endpoints and version numbers.

Can get the summoner ID for a summoner name and use it for future operations.
It also saves it to a database so if further requests are made for that
summoner, the ID is already there, avoiding another call to the API.

Currently it only tells you one specific piece of information, at this stage
being their maximum time played in a ranked game on a specific champ.
However this can be easily changed just by using a different dictionary index
in the data pulled from the inital stats API call.
"""

#from riotapi import RiotAPI
from requests import get
from ast import literal_eval
import cPickle as pickle
import json
from urllib import urlopen

summ_version = "v1.4"
stats_version = "v1.3"
stat_dat_version = "v1.2"
game_version = "v1.3"
key = "3b39cc75-4cb2-4a2e-9a46-a3f44ebcf532"


def summoner_id_find(summoner, region, call_start):

    known_ids_dict = pickle.load(open("known_ids.p", "rb"))

    summ_id = 0

    if known_ids_dict.get(summoner) is not None:
        summ_id = known_ids_dict.get(summoner)
        print "Using summoner ID value in database: " + str(summ_id)
    else:
        print "Searching up summoner ID, not in database."
        url_call_summ_id = call_start + summ_version + "/" + "summoner/by-name/" + summoner + "?api_key=" + key
        summ_id_data = get(url_call_summ_id)
        summ_id_code = summ_id_data.status_code
        if summ_id_code == 200:
            print "Good call, got response code 200."
            # Now we know we have good data, we can append the new summoner and respective ID to the dictionary.
            summ_id = literal_eval(str(summ_id_data.text))[summoner]["id"]
            print "Summoner ID retrieved for " + str(summoner) + ": " + str(summ_id)
            known_ids_dict[summoner] = summ_id
            # This then writes the dictionary back to the file as a string
            pickle.dump(known_ids_dict, open("known_ids.p", "wb"))
        else:
            print "Receieved error " + str(summ_id_code) + ", perhaps a non-existent Summoner. Starting again..."
            summoner_id_find()

    return summ_id


def summoner_ranked_champ_stats(summ_id, region, season, call_start):
    # Starts the call for the players data on all champs.
    url_call = call_start + stats_version + "/stats/by-summoner/" + str(summ_id) + "/ranked?season=SEASON" + str(season) + "&api_key=" + key
    stats_data = get(url_call)
    stats_code = stats_data.status_code
    if stats_code == 200:
        # No need for good call message as this is a static call, should work 100% of the time.
        # Starts call for a champ to ID translation.
        champ = str(raw_input("Which champ did you want your stats for? ")).lower().title()
        url_call = "https://" + region + ".api.pvp.net/api/lol/static-data/" + region + "/" + stat_dat_version + "/champion?api_key=" + key
        stat_dat_data = get(url_call)
        stat_dat_code = stat_dat_data.status_code
        champ_id = 0
        if stat_dat_code == 200:
            # If the request was made properly, this finds the champ ID from the data.
            print "Another good call, got response code 200."
            try:
                print str(champ) + ", " + literal_eval(stat_dat_data.text)["data"][champ]["title"]
                champ_id = literal_eval(stat_dat_data.text)["data"][champ]["id"]
                print "ID: " + str(champ_id)
            except KeyError:
                print "That champion doesn't exist, try again."
                summoner_stats_func(summ_id, summoner, region, season, call_start)
            except:
                sys.exit("Something went wrong, terminating...")
        else:
            print "Receieved error " + str(stat_dat_code) + ", perhaps a non-existent Summoner. Starting again..."
            summoner_ranked_champ_stats()
        found = 0
        for i in literal_eval(stats_data.text)["champions"]:
            if i["id"] == champ_id:
                found = 1
                done = 0
                again = "yes"
                while done != 1:
                    if again == "yes" or again == "y":
                        try:
                            print "Options: " + str(i["stats"].keys())
                            stat_wanted = str(raw_input("What data did you want to know?\n(Or just say: all stats) "))
                            print stat_wanted + ": " + str(i["stats"][stat_wanted])
                        except KeyError:
                            print "That was an invalid stat call, try something else."
                            pass
                        except:
                            print "Dat shit dun fukt"
                        again = str(raw_input("Do you want to know more for this champ? ")).lower()
                    else:
                        again = "no"
                        done = 1
        if found == 0:
            print "You have not played this champ in ranked this season.\nTry again."
            summoner_ranked_champ_stats(summ_id, region, season, call_start)
    else:
        print "Receieved error " + str(stats_code) + ", perhaps a non-existent Summoner. Starting again..."
        summoner_stats_func()
    print "Thanks for using, re-run the program for a different champion if you want.\nTry typing 'main()' without the quotation marks."


def summoner_general_stats(summ_id, summoner, region, season, call_start):
    mode_wanted_dict = {"ranked solo 5s": "RankedSolo5x5", "unranked 5s": "Unranked", "unranked 3s": "Unranked3x3", "urf": "URF"}
    url_call = call_start + stats_version + "/stats/by-summoner/" + str(summ_id) + "/summary?season=SEASON" + str(season) + "&api_key=" + key
    stats_data = get(url_call)
    stats_code = stats_data.status_code
    if stats_code == 200:
        print "Good call, got response code 200."
        mode_wanted = str(raw_input("\nWhich game mode did you want data for?\nOptions: ranked solo 5s, unranked 5s, unranked 3s, urf: "))
        if mode_wanted_dict.get(mode_wanted) is not None:
            print "Good game mode selection: " + mode_wanted_dict[mode_wanted]
            for mode in literal_eval(stats_data.text)["playerStatSummaries"]:
                if mode['playerStatSummaryType'] == mode_wanted_dict[mode_wanted]:
                    done = 0
                    while done != 1:
                        stat_wanted = str(raw_input("\nWhat stat did you want to know about your overall summoner profile?\nOptions: wins, " + str(mode["aggregatedStats"].keys()) + "\nStat wanted: "))
                        try:
                            if stat_wanted == "wins":
                                print mode["wins"]
                            else:
                                print mode['aggregatedStats'][stat_wanted]
                            again = str(raw_input("Did you want to know something else? (yes or no)")).lower()
                            if again == "yes" or done == "y":
                                done = 0
                            else:
                                done = 1
                        except KeyError:
                            print "That was an invalid stat, try again."
        else:
            print "That was an invalid mode, try again."
            summoner_general_stats(summ_id, summoner, region, season, call_start)
        print "Thanks for using, re-run the program for another summoner if you want.\nTry typing 'main()' without the quotation marks."

def team_stats(summ_id, region, season, call_start):
    print "yolo"


# Takes the summ_id
def player_tracker():
    player_tracker_dict = pickle.load(open("player_tracker_db.p", "rb"))
    for summ in player_tracker_dict:
        region = player_tracker_dict[summ]["region"]
        summ_id = player_tracker_dict[summ]["summ_id"]
        url_call = "https://" + region + ".api.pvp.net/api/lol/" + region + "/" + game_version + "/game/by-summoner/" + str(summ_id) + "/recent?api_key=" + key
        raw_data = urlopen(url_call)
        game_data = json.loads(raw_data.readlines()[0])
        out = game_data
        #game_code = raw_data.status_code
        game_code = 200
        if game_code == 200:
            print "Running tracker on %s." % summ
            for game in out["games"]:
                for j in game:
                    print j
        else:
            print "Receieved error " + str(stats_code) + ", something went wrong with this summoner: " + summ

def player_tracker_add():
    # Make sure all data is good before adding it to the database. Use the adder to check for correct data, so the tracker doesn't have to.
    pass                   

def player_tracker_lookup():
    #inc something to do with date (haven't played with this cunt since lalal)
    pass

def main():
    print "Running player tracker..."
    player_tracker()

    type_call = int(raw_input("\n0. Quit (0)\n1. Did you want your stats for a specific champ (ranked only for this function) (1)\n2. Overall stats on your summoner profile (2)\n3. Stats for you ranked team (3)\n4. To add a new summoner to the enemy player tracker (4)\nChoose an option: "))

    if type_call != 0:
        if type_call == 4:
            question = "Enter summoner name to add to Player Tracker: "
        else:
            question = "Enter summoner name to look up: "
        summoner = (str(raw_input(question))).lower()
        region = (str(raw_input("What region? "))).lower()

        if type_call != 4:
            season = str(raw_input("Which season? (3 or 4) "))
            ok = 0
            while ok != 1:
                try:
                    if 3 <= int(season) <= 4:
                        ok = 1
                        break
                    else:
                        season = str(raw_input("Invalid season. Which season? (3 or 4) "))
                except:
                    print "You probably entered a letter, you done fucked it."
                    season = str(raw_input("Invalid season. Which season? (3 or 4) "))

        call_start = "https://" + region + ".api.pvp.net/api/lol/" + region + "/"

        summ_id_m = summoner_id_find(summoner, region, call_start) #summ_id_main
    
    if type_call == 0:
        print "kk, bai"
    if type_call == 1:
        # If they called for their specific stats on a champ.
        summoner_ranked_champ_stats(summ_id_m, region, season, call_start)
    if type_call == 2:
        # If they called for general stats.
        summoner_general_stats(summ_id_m, summoner, region, season, call_start)
    if type_call == 3:
        team_stats(summ_id, region, season, call_start)
    if type_call == 4:
        player_tracker_add(summ_id_m, region, season, call_start)
    if type_call == 5:
        player_tracker_lookup(summ_id_m)
    else:
        print "That was an invalid choice, choose 1 or 2 please."
        main()

main()

# Inital write of pickle file
"""
start_dict = {"banool": {"summ_id": 283723, "region": "oce", "date_added": 28.07.2014, "played_with": {"xhkxsilence": [311272, 0], "edward132": [276318, 0]}}, "jompie": {"summ_id": 293509, "region": "oce", "date_added": 24.07.2014, "played_with": {"edward132": [276318, 0]}}}
# format is summoner: their id and region and date added, then who they played with. that has a summ_name: [their id, times played]
pickle.dump(start_dict, open("player_tracker_db.p", "wb"))
"""

"""
old shit
riot_api = RiotAPI(key)

get_req = ("https://oce.api.pvp.net/api/lol/oce/v1.4/summoner/by-name/Banool?api_key=" + key)
print get_req

swag = get(get_req)
print swag

print riot_api.get_summoner_by_name("Banool", "oce")
"""
