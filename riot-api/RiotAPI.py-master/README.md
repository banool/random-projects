RiotAPI.py 0.0.1
======
RiotAPI.py is a python wrapper for the newly released [Riot Games developers API][1] For League of legends. It is loosely based on [Elophant.py][2]

Getting Started
----------------

To start using this python package you first need to get at API key, from [The official sign-up page][3]
Also, you need to install the [Requests module][5], you can do this via pip

    pip install requests

After that, you are ready to use RiotAPI.py

    #First you need to import it     
    from riotapi import RiotAPI
    #Then initialize it, remember to add your apikey here
    riot_api = RiotAPI("Your-APIkey-Here")
    
    #now you can use all the official features. e.g.
    #List all free to play champions, 
    print riot_api.get_champions(free_to_play=True)
    
    #Lookup a summoner by name
    print riot_api.get_summoner_by_name('fireproof', 'euw')
    #note that all functions return json, so if you wanted 
    #the summonerId you would need something like this
    print riot_api.get_summoner_by_name('fireproof', 'euw')['id']

    #Check their match history, note most functions need summonerId
    print riot_api.get_recent_games(20689391, 'euw')

    #Check their ranked stats for season 3
    print riot_api.get_stats_ranked(20689391, 'euw', season='SEASON3')

A full documentation will be created soon, right now you can find all functions [here][4]


  [1]: https://developer.riotgames.com
  [2]: https://github.com/bryanveloso/elophant.py
  [3]: https://developer.riotgames.com/sign-in
  [4]: https://developer.riotgames.com/api/methods
  [5]: https://pypi.python.org/pypi/requests

RiotAPI.py isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
