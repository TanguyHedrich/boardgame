# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 21:35:08 2020

@author: Tanguy
"""


def importData(folder):
    import csv, re
    

    # Games:
    #   - id
    #   - Name
    #   - ListPlays
    #   - year?
    #   - Coop / semi / comp?
    
    listGames = []
    with open(folder + 'GameRealm.csv','r',encoding='utf-8') as GameRealm:
        GameRealmReader = csv.reader(GameRealm)
        next(GameRealm) #skip the header
        for row in GameRealmReader:
            name = row[2]
            gamesPlayedRaw = row[7]
            m = re.search(r"{([\d ]+)}", gamesPlayedRaw)
            if m:
                gamesPlayed = list(map(int,m.group(1).split()))
            else:
                gamesPlayed = []
            yearPublished = row[24]
            listGames.append([GameRealmReader.line_num-2,name,gamesPlayed,yearPublished])


    # Players:
    #   - id
    #   - name
    #   - list games?
    listPlayers = []
    with open(folder + 'PlayerRealm.csv','r',encoding='utf-8') as PlayerRealm:
        PlayerRealmReader = csv.reader(PlayerRealm)
        next(PlayerRealmReader) #skip the header
        for row in PlayerRealmReader:
            name = row[3]
            
            m = re.search(r"{([\d ]+)}", row[5])
            gamesPlayed = list(map(int,m.group(1).split())) if m else []
                
            listPlayers.append([PlayerRealmReader.line_num-2,name,gamesPlayed])

    # PlayParticipantsRealm: 
    #   — player ID
    #   — score
    #   — Finishing place
    #
    # Just used for the listPlays after
    listPlayParticipants = []
    with open(folder + 'PlayParticipantsRealm.csv','r',encoding='utf-8') as PlayParticipantsRealm:
        PlayParticipantsRealmReader = csv.reader(PlayParticipantsRealm)
        next(PlayParticipantsRealmReader) #skip the header
        for row in PlayParticipantsRealmReader:
            m = re.search(r"{([\d]+)}", row[1])
            playerId = int(m.group(1)) if m else []
            
            score = int(row[3])
            finishPlace = int(row[4])
            listPlayParticipants.append([PlayParticipantsRealmReader.line_num-2,playerId,score,finishPlace])
     
    #Locations
    #   - Location ID
    #   - name
    listLoc = []
    with open(folder + 'LocationRealm.csv','r',encoding='utf-8') as LocationRealm:
        LocationRealmReader = csv.reader(LocationRealm)
        next(LocationRealmReader) #skip the header
        for row in LocationRealmReader:
            name = row[1]
            listLoc.append([LocationRealmReader.line_num-2,name])        
            
    # Plays:
    #   - id
    #   - id games
    #   - date
    #   - duration (in ms)
    #   - location name
    #   - participants id
    #   - participant scores
    #   - participants order
    listPlays = []
    with open(folder + 'PlayRealm.csv','r',encoding='utf-8') as PlayRealm:
        PlayRealmReader = csv.reader(PlayRealm)
        next(PlayRealmReader) #skip the header
        for row in PlayRealmReader:

            m = re.search(r"{([\d]+)}", row[2])
            gameId = int(m.group(1)) if m else []
            
            date = dt.datetime.fromtimestamp(int(row[9])/1000)
            
            duration = int(row[12])
            
            
            m = re.search(r"{([\d]+)}", row[5])
            locId = int(m.group(1)) if m else []
            locName = listLoc[locId][1]
            
            m = re.search(r"{([\d ]+)}", row[7])
            PlayParticipants = list(map(int,m.group(1).split())) if m else []
            
            
            playersId,score,finishPlace = [],[],[]
            
            for p in PlayParticipants:
                playersId.append(listPlayParticipants[p][1])
                score.append(listPlayParticipants[p][2])
                finishPlace.append(listPlayParticipants[p][3])
                

            listPlays.append([PlayRealmReader.line_num-2,gameId,date,duration,locName,playersId,score,finishPlace])




    return listGames,listPlayers,listPlays



import matplotlib.pyplot as plt
import datetime as dt
from math import floor

folder = 'db/tanguy/'

listGames,listPlayers,listPlays = importData(folder)


# First plot!
#   Time played every 7 days
#   bar plot
today = dt.datetime.today()
iDays = dt.datetime(2020,1,1) # starting 1st of Jan 2020
sevenDays = dt.timedelta(days=7)

diff = today - iDays

durWeek = []
for i in range(floor(diff.days / 7)):
    
    duration = 0 
    for play in listPlays:
        if iDays + i * sevenDays  <= play[2] < iDays + (i+1) * sevenDays:
            duration += play[3] / 1000 / 60 # convert to min
    
    durWeek.append(duration)


fig, ax = plt.subplots()
plt.bar(list(range(floor(diff.days / 7))), durWeek)
plt.xlabel("weeks")
plt.ylabel("Time played (min)")
plt.title("Weekly time played")
plt.savefig('figures/tanguy/weekly_time_played.png')
