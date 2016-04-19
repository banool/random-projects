#coding: utf8
from __future__ import unicode_literals
from requests import get
'''
RiotAPI.py isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games
or anyone officially involved in producing or managing League of Legends.
League of Legends and Riot Games are trademarks or registered trademarks of
Riot Games,Inc. League of Legends © Riot Games, Inc.
'''

class RiotAPI(object):

    def __init__(self, key=None):
        self.key = key

    v1_api_url = 'https://prod.api.pvp.net/api/lol/%s/v1.1/'
    v2_api_url = 'https://prod.api.pvp.net/api/%s/v2.1/'
    v4_api_url = 'https://%s.api.pvp.net/api/lol/%s/'

    def _get(self, url, region='oce', api_level='v1', payload={}):

       
        payload['api_key'] = self.key

        if api_level == 'v1':
            api_url = self.v1_api_url
        elif api_level == 'v2':
            api_url = self.v2_api_url

        api_url = self.v4_api_url
        
        uri = api_url % (region.lower(), region.lower()) + url
        return get(uri, params=payload).json()

    def get_champions(self, free_to_play=None):
        return self._get('champion', payload={'freeToPlay': free_to_play})

    def get_recent_games(self, summoner_id, region):
        return self._get('game/by-summoner/%s/recent' % summoner_id, region=region)

    def get_league(self, summoner_id, region):
        return self._get('league/by-summoner/%s' % summoner_id, region=region, api_level='v2')

    ####STATS####
    def get_stats_summary(self, summoner_id, region, season=None):
        return self._get('stats/by-summoner/%s/summary' % summoner_id, region=region, payload={'season': season})

    def get_stats_ranked(self, summoner_id, region, season=None):
        return self._get('stats/by-summoner/%s/ranked' % summoner_id, region=region, payload={'season': season})

    ##SUMMONER##
    def get_summoner_by_name(self, name, region):
        #TODO: fix non ascii names
        return self._get('summoner/by-name/%s' % name.replace(' ', ''), region=region)

    def get_summoner_by_id(self, summoner_id, region):
        return self._get('summoner/%s' % summoner_id, region=region)

    def get_summoner_masteries(self, summoner_id, region):
        return self._get('summoner/%s/masteries' % summoner_id, region=region)

    def get_summoner_runes(self, summoner_id, region):
        return self._get('summoner/%s/runes' % summoner_id, region=region)

    def get_summoner_name(self, summoner_id, region):
        return self._get('summoner/%s/name' % summoner_id, region=region)

    ##TEAMS##
    def get_teams_by_summoner(self, summoner_id, region):
        return self._get('team/by-summoner/%s' % summoner_id, region=region, api_level='v2')
