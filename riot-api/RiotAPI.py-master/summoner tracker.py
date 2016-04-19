# Compiles a database of if you've played with a player on the enemy team before.

from requests import get

true = True
false = False

def summ_id_lookup(summ_name, region, 
https://oce.api.pvp.net/api/lol/oce/v1.3/game/by-summoner/283723/recent?api_key=3b39cc75-4cb2-4a2e-9a46-a3f44ebcf532

test_data = {
   "games": [
      {
         "fellowPlayers": [
            {
               "championId": 126,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 24,
               "teamId": 200,
               "summonerId": 229382
            },
            {
               "championId": 25,
               "teamId": 200,
               "summonerId": 327082
            },
            {
               "championId": 236,
               "teamId": 200,
               "summonerId": 232612
            },
            {
               "championId": 55,
               "teamId": 200,
               "summonerId": 584265
            },
            {
               "championId": 201,
               "teamId": 100,
               "summonerId": 288499
            },
            {
               "championId": 238,
               "teamId": 100,
               "summonerId": 293509
            },
            {
               "championId": 254,
               "teamId": 200,
               "summonerId": 353585
            },
            {
               "championId": 119,
               "teamId": 100,
               "summonerId": 228161
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 9800,
            "item2": 1011,
            "goldEarned": 8510,
            "wardPlaced": 5,
            "totalDamageTaken": 15412,
            "item0": 3206,
            "trueDamageDealtPlayer": 7772,
            "physicalDamageDealtPlayer": 21154,
            "trueDamageDealtToChampions": 222,
            "visionWardsBought": 1,
            "killingSprees": 2,
            "totalUnitsHealed": 1,
            "level": 12,
            "neutralMinionsKilledYourJungle": 46,
            "magicDamageDealtToChampions": 6488,
            "turretsKilled": 1,
            "magicDamageDealtPlayer": 47918,
            "neutralMinionsKilledEnemyJungle": 15,
            "assists": 8,
            "magicDamageTaken": 3842,
            "numDeaths": 4,
            "totalTimeCrowdControlDealt": 172,
            "largestMultiKill": 1,
            "physicalDamageTaken": 11052,
            "sightWardsBought": 1,
            "team": 100,
            "win": true,
            "totalDamageDealt": 76845,
            "largestKillingSpree": 2,
            "totalHeal": 2794,
            "item4": 3020,
            "item3": 3136,
            "item6": 3340,
            "item5": 1026,
            "minionsKilled": 18,
            "timePlayed": 1246,
            "physicalDamageDealtToChampions": 3089,
            "championsKilled": 5,
            "trueDamageTaken": 518,
            "goldSpent": 7145,
            "neutralMinionsKilled": 61
         },
         "gameId": 49370535,
         "ipEarned": 76,
         "spell1": 11,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403844683168,
         "championId": 28
      },
      {
         "fellowPlayers": [
            {
               "championId": 101,
               "teamId": 100,
               "summonerId": 272888
            },
            {
               "championId": 126,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 53,
               "teamId": 100,
               "summonerId": 229731
            },
            {
               "championId": 238,
               "teamId": 200,
               "summonerId": 273778
            },
            {
               "championId": 92,
               "teamId": 200,
               "summonerId": 280860
            },
            {
               "championId": 81,
               "teamId": 200,
               "summonerId": 1912098
            },
            {
               "championId": 412,
               "teamId": 200,
               "summonerId": 228227
            },
            {
               "championId": 64,
               "teamId": 200,
               "summonerId": 455351
            },
            {
               "championId": 67,
               "teamId": 100,
               "summonerId": 228161
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 21230,
            "item2": 1052,
            "goldEarned": 14182,
            "item1": 3143,
            "wardPlaced": 10,
            "totalDamageTaken": 31177,
            "item0": 3206,
            "trueDamageDealtPlayer": 11812,
            "physicalDamageDealtPlayer": 45419,
            "trueDamageDealtToChampions": 350,
            "visionWardsBought": 1,
            "killingSprees": 2,
            "totalUnitsHealed": 1,
            "level": 18,
            "doubleKills": 1,
            "neutralMinionsKilledYourJungle": 77,
            "magicDamageDealtToChampions": 14937,
            "magicDamageDealtPlayer": 112986,
            "neutralMinionsKilledEnemyJungle": 6,
            "assists": 12,
            "magicDamageTaken": 4293,
            "numDeaths": 6,
            "totalTimeCrowdControlDealt": 627,
            "largestMultiKill": 2,
            "physicalDamageTaken": 25221,
            "sightWardsBought": 3,
            "team": 100,
            "win": false,
            "totalDamageDealt": 170218,
            "largestKillingSpree": 3,
            "totalHeal": 6339,
            "item4": 3116,
            "item3": 3255,
            "item6": 3340,
            "item5": 3151,
            "minionsKilled": 60,
            "timePlayed": 2441,
            "wardKilled": 1,
            "physicalDamageDealtToChampions": 5943,
            "championsKilled": 9,
            "trueDamageTaken": 1661,
            "goldSpent": 14785,
            "neutralMinionsKilled": 83
         },
         "gameId": 49361025,
         "ipEarned": 72,
         "spell1": 11,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403842000079,
         "championId": 28
      },
      {
         "fellowPlayers": [
            {
               "championId": 13,
               "teamId": 200,
               "summonerId": 498749
            },
            {
               "championId": 67,
               "teamId": 200,
               "summonerId": 569809
            },
            {
               "championId": 55,
               "teamId": 100,
               "summonerId": 347758
            },
            {
               "championId": 412,
               "teamId": 100,
               "summonerId": 271496
            },
            {
               "championId": 222,
               "teamId": 100,
               "summonerId": 626527
            },
            {
               "championId": 64,
               "teamId": 200,
               "summonerId": 229500
            },
            {
               "championId": 53,
               "teamId": 200,
               "summonerId": 473577
            },
            {
               "championId": 107,
               "teamId": 100,
               "summonerId": 351950
            },
            {
               "championId": 80,
               "teamId": 100,
               "summonerId": 281972
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 22642,
            "item2": 3136,
            "goldEarned": 11888,
            "item1": 3110,
            "wardPlaced": 5,
            "item0": 1056,
            "totalDamageTaken": 24879,
            "trueDamageDealtPlayer": 602,
            "physicalDamageDealtPlayer": 34932,
            "trueDamageDealtToChampions": 188,
            "killingSprees": 2,
            "totalUnitsHealed": 1,
            "level": 15,
            "doubleKills": 1,
            "neutralMinionsKilledYourJungle": 5,
            "magicDamageDealtToChampions": 17005,
            "turretsKilled": 1,
            "magicDamageDealtPlayer": 45527,
            "neutralMinionsKilledEnemyJungle": 1,
            "assists": 11,
            "magicDamageTaken": 7893,
            "numDeaths": 4,
            "totalTimeCrowdControlDealt": 1096,
            "largestMultiKill": 2,
            "physicalDamageTaken": 14482,
            "sightWardsBought": 1,
            "team": 200,
            "win": false,
            "totalDamageDealt": 81062,
            "largestKillingSpree": 8,
            "totalHeal": 1543,
            "item4": 3102,
            "item3": 3068,
            "item6": 3340,
            "item5": 3047,
            "minionsKilled": 116,
            "timePlayed": 1848,
            "physicalDamageDealtToChampions": 5448,
            "championsKilled": 10,
            "trueDamageTaken": 2503,
            "goldSpent": 12785,
            "neutralMinionsKilled": 6
         },
         "gameId": 49352892,
         "ipEarned": 58,
         "spell1": 3,
         "teamId": 200,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403826774966,
         "championId": 60
      },
      {
         "fellowPlayers": [
            {
               "championId": 41,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 77,
               "teamId": 100,
               "summonerId": 296513
            },
            {
               "championId": 222,
               "teamId": 200,
               "summonerId": 438637
            },
            {
               "championId": 412,
               "teamId": 200,
               "summonerId": 1092406
            },
            {
               "championId": 161,
               "teamId": 100,
               "summonerId": 431733
            },
            {
               "championId": 67,
               "teamId": 100,
               "summonerId": 283050
            },
            {
               "championId": 72,
               "teamId": 200,
               "summonerId": 433641
            },
            {
               "championId": 96,
               "teamId": 200,
               "summonerId": 926119
            },
            {
               "championId": 39,
               "teamId": 200,
               "summonerId": 364382
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 17111,
            "goldEarned": 11615,
            "item2": 2049,
            "item1": 3401,
            "wardPlaced": 16,
            "totalDamageTaken": 33377,
            "item0": 3190,
            "trueDamageDealtPlayer": 5025,
            "physicalDamageDealtPlayer": 10868,
            "visionWardsBought": 1,
            "totalUnitsHealed": 5,
            "level": 16,
            "magicDamageDealtToChampions": 12552,
            "magicDamageDealtPlayer": 33135,
            "assists": 23,
            "magicDamageTaken": 10278,
            "numDeaths": 7,
            "totalTimeCrowdControlDealt": 127,
            "largestMultiKill": 1,
            "physicalDamageTaken": 21272,
            "sightWardsBought": 1,
            "win": true,
            "team": 100,
            "totalDamageDealt": 49028,
            "totalHeal": 2810,
            "item4": 3111,
            "item3": 3068,
            "item6": 3340,
            "item5": 1011,
            "minionsKilled": 56,
            "timePlayed": 2178,
            "wardKilled": 1,
            "physicalDamageDealtToChampions": 4558,
            "championsKilled": 1,
            "trueDamageTaken": 1827,
            "goldSpent": 11980
         },
         "gameId": 49352501,
         "ipEarned": 101,
         "spell1": 3,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403824589393,
         "championId": 89
      },
      {
         "fellowPlayers": [
            {
               "championId": 5,
               "teamId": 100,
               "summonerId": 576245
            },
            {
               "championId": 133,
               "teamId": 200,
               "summonerId": 287449
            },
            {
               "championId": 14,
               "teamId": 100,
               "summonerId": 351583
            },
            {
               "championId": 84,
               "teamId": 100,
               "summonerId": 270407
            },
            {
               "championId": 201,
               "teamId": 200,
               "summonerId": 320959
            },
            {
               "championId": 24,
               "teamId": 200,
               "summonerId": 449752
            },
            {
               "championId": 67,
               "teamId": 100,
               "summonerId": 338442
            },
            {
               "championId": 134,
               "teamId": 200,
               "summonerId": 1282239
            },
            {
               "championId": 86,
               "teamId": 200,
               "summonerId": 1001226
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 10004,
            "item2": 1052,
            "goldEarned": 7729,
            "item1": 3136,
            "wardPlaced": 4,
            "totalDamageTaken": 14816,
            "item0": 3206,
            "trueDamageDealtPlayer": 7692,
            "physicalDamageDealtPlayer": 25001,
            "trueDamageDealtToChampions": 246,
            "visionWardsBought": 1,
            "killingSprees": 1,
            "totalUnitsHealed": 1,
            "level": 12,
            "neutralMinionsKilledYourJungle": 64,
            "magicDamageDealtToChampions": 6445,
            "turretsKilled": 2,
            "magicDamageDealtPlayer": 55416,
            "neutralMinionsKilledEnemyJungle": 7,
            "assists": 5,
            "magicDamageTaken": 2953,
            "numDeaths": 3,
            "totalTimeCrowdControlDealt": 158,
            "largestMultiKill": 1,
            "physicalDamageTaken": 11729,
            "sightWardsBought": 2,
            "team": 100,
            "win": true,
            "totalDamageDealt": 88110,
            "largestKillingSpree": 2,
            "totalHeal": 3612,
            "item3": 3020,
            "item6": 3340,
            "minionsKilled": 16,
            "timePlayed": 1264,
            "physicalDamageDealtToChampions": 3312,
            "championsKilled": 4,
            "trueDamageTaken": 134,
            "goldSpent": 5980,
            "neutralMinionsKilled": 71
         },
         "gameId": 49344571,
         "ipEarned": 226,
         "spell1": 11,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403814549052,
         "championId": 28
      },
      {
         "fellowPlayers": [
            {
               "championId": 157,
               "teamId": 200,
               "summonerId": 1251068
            },
            {
               "championId": 60,
               "teamId": 200,
               "summonerId": 311272
            },
            {
               "championId": 82,
               "teamId": 100,
               "summonerId": 705849
            },
            {
               "championId": 78,
               "teamId": 100,
               "summonerId": 317431
            },
            {
               "championId": 33,
               "teamId": 100,
               "summonerId": 341100
            },
            {
               "championId": 92,
               "teamId": 200,
               "summonerId": 276318
            },
            {
               "championId": 104,
               "teamId": 200,
               "summonerId": 306755
            },
            {
               "championId": 236,
               "teamId": 100,
               "summonerId": 228421
            },
            {
               "championId": 222,
               "teamId": 100,
               "summonerId": 452484
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 13532,
            "goldEarned": 10095,
            "item2": 2049,
            "item1": 3069,
            "wardPlaced": 16,
            "totalDamageTaken": 29767,
            "item0": 3117,
            "physicalDamageDealtPlayer": 7503,
            "visionWardsBought": 1,
            "totalUnitsHealed": 1,
            "level": 15,
            "magicDamageDealtToChampions": 11475,
            "turretsKilled": 2,
            "magicDamageDealtPlayer": 31690,
            "assists": 21,
            "magicDamageTaken": 12689,
            "numDeaths": 9,
            "totalTimeCrowdControlDealt": 229,
            "largestMultiKill": 1,
            "physicalDamageTaken": 16882,
            "sightWardsBought": 1,
            "win": true,
            "team": 200,
            "totalDamageDealt": 39194,
            "totalHeal": 868,
            "item4": 3211,
            "item3": 3068,
            "item6": 3340,
            "item5": 1028,
            "minionsKilled": 38,
            "timePlayed": 2126,
            "physicalDamageDealtToChampions": 2056,
            "championsKilled": 1,
            "trueDamageTaken": 196,
            "goldSpent": 8705
         },
         "gameId": 49117482,
         "ipEarned": 99,
         "spell1": 3,
         "teamId": 200,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403637290199,
         "championId": 412
      },
      {
         "fellowPlayers": [
            {
               "championId": 34,
               "teamId": 200,
               "summonerId": 498749
            },
            {
               "championId": 104,
               "teamId": 200,
               "summonerId": 575721
            },
            {
               "championId": 4,
               "teamId": 100,
               "summonerId": 336476
            },
            {
               "championId": 238,
               "teamId": 100,
               "summonerId": 361204
            },
            {
               "championId": 222,
               "teamId": 100,
               "summonerId": 294502
            },
            {
               "championId": 267,
               "teamId": 200,
               "summonerId": 296073
            },
            {
               "championId": 121,
               "teamId": 100,
               "summonerId": 223525
            },
            {
               "championId": 58,
               "teamId": 200,
               "summonerId": 228280
            },
            {
               "championId": 53,
               "teamId": 100,
               "summonerId": 237531
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 16806,
            "item2": 3068,
            "goldEarned": 9510,
            "item1": 3255,
            "wardPlaced": 9,
            "totalDamageTaken": 29154,
            "item0": 3207,
            "trueDamageDealtPlayer": 9352,
            "physicalDamageDealtPlayer": 32371,
            "trueDamageDealtToChampions": 726,
            "visionWardsBought": 1,
            "killingSprees": 1,
            "totalUnitsHealed": 1,
            "level": 14,
            "neutralMinionsKilledYourJungle": 56,
            "magicDamageDealtToChampions": 12889,
            "turretsKilled": 1,
            "magicDamageDealtPlayer": 55547,
            "neutralMinionsKilledEnemyJungle": 6,
            "assists": 6,
            "magicDamageTaken": 7752,
            "numDeaths": 11,
            "totalTimeCrowdControlDealt": 219,
            "largestMultiKill": 1,
            "physicalDamageTaken": 20567,
            "sightWardsBought": 1,
            "team": 200,
            "win": false,
            "totalDamageDealt": 97270,
            "largestKillingSpree": 2,
            "totalHeal": 2357,
            "item4": 1057,
            "item3": 3136,
            "item6": 3340,
            "minionsKilled": 14,
            "timePlayed": 1793,
            "wardKilled": 1,
            "physicalDamageDealtToChampions": 3191,
            "championsKilled": 7,
            "trueDamageTaken": 834,
            "goldSpent": 9350,
            "neutralMinionsKilled": 62
         },
         "gameId": 48996901,
         "ipEarned": 57,
         "spell1": 11,
         "teamId": 200,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403591445034,
         "championId": 60
      },
      {
         "fellowPlayers": [
            {
               "championId": 23,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 236,
               "teamId": 200,
               "summonerId": 293122
            },
            {
               "championId": 99,
               "teamId": 200,
               "summonerId": 345753
            },
            {
               "championId": 81,
               "teamId": 200,
               "summonerId": 345559
            },
            {
               "championId": 98,
               "teamId": 200,
               "summonerId": 456715
            },
            {
               "championId": 76,
               "teamId": 100,
               "summonerId": 293509
            },
            {
               "championId": 25,
               "teamId": 100,
               "summonerId": 279276
            },
            {
               "championId": 10,
               "teamId": 100,
               "summonerId": 298730
            },
            {
               "championId": 79,
               "teamId": 200,
               "summonerId": 235630
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 20099,
            "item2": 3151,
            "goldEarned": 15619,
            "item1": 3020,
            "wardPlaced": 8,
            "item0": 3207,
            "totalDamageTaken": 24680,
            "trueDamageDealtPlayer": 15934,
            "physicalDamageDealtPlayer": 27145,
            "trueDamageDealtToChampions": 454,
            "visionWardsBought": 1,
            "killingSprees": 1,
            "totalUnitsHealed": 1,
            "level": 18,
            "doubleKills": 1,
            "neutralMinionsKilledYourJungle": 100,
            "magicDamageDealtToChampions": 18542,
            "turretsKilled": 1,
            "magicDamageDealtPlayer": 153015,
            "neutralMinionsKilledEnemyJungle": 13,
            "assists": 13,
            "magicDamageTaken": 8426,
            "numDeaths": 8,
            "totalTimeCrowdControlDealt": 618,
            "largestMultiKill": 2,
            "physicalDamageTaken": 15969,
            "team": 100,
            "win": true,
            "totalDamageDealt": 196095,
            "largestKillingSpree": 6,
            "totalHeal": 8524,
            "item4": 3135,
            "item3": 3116,
            "item6": 3340,
            "item5": 3152,
            "minionsKilled": 58,
            "timePlayed": 2338,
            "physicalDamageDealtToChampions": 1102,
            "championsKilled": 9,
            "trueDamageTaken": 284,
            "goldSpent": 16750,
            "neutralMinionsKilled": 113
         },
         "gameId": 48989582,
         "ipEarned": 106,
         "spell1": 11,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403589175960,
         "championId": 82
      },
      {
         "fellowPlayers": [
            {
               "championId": 39,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 51,
               "teamId": 200,
               "summonerId": 320146
            },
            {
               "championId": 412,
               "teamId": 200,
               "summonerId": 552012
            },
            {
               "championId": 103,
               "teamId": 100,
               "summonerId": 408377
            },
            {
               "championId": 30,
               "teamId": 200,
               "summonerId": 221088
            },
            {
               "championId": 201,
               "teamId": 100,
               "summonerId": 550976
            },
            {
               "championId": 236,
               "teamId": 100,
               "summonerId": 588118
            },
            {
               "championId": 77,
               "teamId": 200,
               "summonerId": 485986
            },
            {
               "championId": 76,
               "teamId": 200,
               "summonerId": 221108
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 28171,
            "item2": 3020,
            "barracksKilled": 1,
            "goldEarned": 13830,
            "item1": 3151,
            "wardPlaced": 5,
            "item0": 3207,
            "totalDamageTaken": 28824,
            "trueDamageDealtPlayer": 17646,
            "physicalDamageDealtPlayer": 38351,
            "trueDamageDealtToChampions": 420,
            "killingSprees": 1,
            "totalUnitsHealed": 1,
            "level": 18,
            "doubleKills": 1,
            "neutralMinionsKilledYourJungle": 100,
            "magicDamageDealtToChampions": 25660,
            "turretsKilled": 2,
            "magicDamageDealtPlayer": 158375,
            "neutralMinionsKilledEnemyJungle": 12,
            "assists": 12,
            "magicDamageTaken": 9008,
            "numDeaths": 8,
            "totalTimeCrowdControlDealt": 431,
            "largestMultiKill": 2,
            "physicalDamageTaken": 19415,
            "team": 100,
            "win": false,
            "totalDamageDealt": 214373,
            "largestKillingSpree": 2,
            "totalHeal": 10036,
            "item4": 3116,
            "item3": 3152,
            "item6": 3340,
            "item5": 1026,
            "minionsKilled": 61,
            "timePlayed": 2160,
            "wardKilled": 2,
            "physicalDamageDealtToChampions": 2091,
            "championsKilled": 5,
            "trueDamageTaken": 400,
            "goldSpent": 14165,
            "neutralMinionsKilled": 112
         },
         "gameId": 48993437,
         "ipEarned": 67,
         "spell1": 11,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403586523900,
         "championId": 82
      },
      {
         "fellowPlayers": [
            {
               "championId": 126,
               "teamId": 100,
               "summonerId": 498749
            },
            {
               "championId": 120,
               "teamId": 200,
               "summonerId": 300374
            },
            {
               "championId": 76,
               "teamId": 200,
               "summonerId": 489202
            },
            {
               "championId": 77,
               "teamId": 100,
               "summonerId": 293509
            },
            {
               "championId": 67,
               "teamId": 200,
               "summonerId": 503767
            },
            {
               "championId": 76,
               "teamId": 100,
               "summonerId": 732496
            },
            {
               "championId": 4,
               "teamId": 200,
               "summonerId": 953860
            },
            {
               "championId": 40,
               "teamId": 200,
               "summonerId": 360675
            },
            {
               "championId": 110,
               "teamId": 100,
               "summonerId": 226841
            }
         ],
         "gameType": "MATCHED_GAME",
         "stats": {
            "totalDamageDealtToChampions": 35946,
            "item2": 3255,
            "goldEarned": 14584,
            "item1": 1058,
            "wardPlaced": 9,
            "item0": 3165,
            "totalDamageTaken": 24483,
            "trueDamageDealtPlayer": 1384,
            "physicalDamageDealtPlayer": 13673,
            "trueDamageDealtToChampions": 1012,
            "visionWardsBought": 1,
            "killingSprees": 4,
            "totalUnitsHealed": 1,
            "level": 17,
            "doubleKills": 1,
            "tripleKills": 1,
            "neutralMinionsKilledYourJungle": 7,
            "magicDamageDealtToChampions": 33501,
            "magicDamageDealtPlayer": 78746,
            "neutralMinionsKilledEnemyJungle": 1,
            "assists": 7,
            "magicDamageTaken": 9807,
            "numDeaths": 7,
            "totalTimeCrowdControlDealt": 132,
            "largestMultiKill": 3,
            "physicalDamageTaken": 13295,
            "team": 100,
            "win": false,
            "totalDamageDealt": 93803,
            "largestKillingSpree": 7,
            "totalHeal": 2784,
            "item4": 3135,
            "item3": 3089,
            "item6": 3341,
            "item5": 3001,
            "minionsKilled": 121,
            "timePlayed": 2265,
            "physicalDamageDealtToChampions": 1432,
            "championsKilled": 17,
            "trueDamageTaken": 1380,
            "goldSpent": 14380,
            "neutralMinionsKilled": 8
         },
         "gameId": 48982528,
         "ipEarned": 68,
         "spell1": 14,
         "teamId": 100,
         "spell2": 4,
         "gameMode": "CLASSIC",
         "mapId": 1,
         "level": 30,
         "invalid": false,
         "subType": "NORMAL",
         "createDate": 1403572255538,
         "championId": 7
      }
   ],
   "summonerId": 283723
}

for i in test_data["games"]:
    print str(i) + "\n"
