#!/bin/python3

import json
import requests
import os.path
import time
import sys

TEMP_FILE = "/tmp/fs2pxo.txt"

GAME_TAGS = {}
GAME_TAGS["ALL"] = ""
GAME_TAGS["FSO"] = "?tag=fs2open"
GAME_TAGS["Retail2"] = "?tag=freespace2"
GAME_TAGS["Retail1"] = "?tag=freespace"
GAME_TAGS["FSPORT"] = "?tag=fsport"

URL = "https://pxo.nottheeye.com/api/v1/games/active" + GAME_TAGS["FSO"]

# Shorthands for specific occurences of
# values in the json to not clutter the output too much

GAME_TYPES = {}
GAME_TYPES["FreeSpace 2 Open"] = "FS2O"

MODES = {}
MODES["Open"] = "O"
MODES["Rank above"] = "R"
MODES["Private"] = "P"

TYPES = {}
TYPES["Cooperative"] = "Coop"
TYPES["Team vs. Team"] = "TvT"
TYPES["Dogfight"] = "DF"

STATES = {}
STATES["Forming"] = "New"
STATES["Mission Sync"] = "Sync"
STATES["Briefing"] = "Brf"
STATES["Debrief"] = "DBrf"


def fetchNewList():
    gameListStr = ""
    # GET and parse JSON into j
    r = requests.get(URL)
    j = json.loads(r.text)
    
    # loop over game type array
    for gtID in range(len(j)):
        gameType = j[gtID]["Game"]
        if (gameType in GAME_TYPES):
            gameType = GAME_TYPES[gameType]
        
        servers = j[gtID]["Servers"]
        
        # loop over servers (games) for that gametype
        # ex. all the fs2 servers for fs2
        for srvID in range(len(servers)):
            # game object holds data about the game on the server
            game = servers[srvID]["Game"]
            
            # name as entered by the host
            name = game["Name"]
            
            # access restrictions (open, rank, private)
            mode = game["Mode"]
            if (mode in MODES):
                mode = MODES[mode]
            
            # what state the game is in (mission selection, brief, playing, debrief, sync)
            state = game["State"]
            if (state in STATES):
                state = STATES[state]
            
            # what type of mission it is (coop, tvt, dogfight)
            type = game["Type"]
            if (type in TYPES):
                type = TYPES[type]
            
            numPlayers = game["NumPlayers"]
            maxPlayers = game["MaxPlayers"]
            
            # print in one concise string per game found
            # print (name + " [" + gameType + "] (" + mode + "|" + type + "|" + state + ")")
            gameListStr = gameListStr + "\n" + f"{(srvID + 1)}/{len(servers)} - {name} ({numPlayers}/{maxPlayers}) ({mode}|{type}|{state})"
            
    return gameListStr
    


def main():
    printout = 0
    if (len(sys.argv) >= 2):
        try:
            printout = int(sys.argv[1])
        except:
            print("Usage: " + os.path.basename(__file__) + " [Number]")
            print("  Number: Print game line N % NumberOfGames")
            print("          use 0 to print all games.")
            exit(-1)
    
    gameListStr = ""
    
    # check if it is time to get a new list from file
    # to do that check if file exists
    # if not, fetch a new list and save to file
    # if yes, fetch datetime from file
    # if datetime older than 5 minutes, fetch new list and save to file
    # else just get the list from the file
    
    # minutes since start of year
    now = time.gmtime().tm_yday * 24 * 60 + time.gmtime().tm_hour * 60 + time.gmtime().tm_min
    
    # if this is set to true, we will fetch a new game list
    fetchNew = True
    
    if (os.path.isfile(TEMP_FILE)):
        with open(TEMP_FILE, "r") as file:
            ln = 0
            for line in file:
                if (ln == 0):
                    timeStamp=int(line)
                    # if more than 5 minutes or new year (now = 0)
                    if (abs(now - timeStamp) > 5):
                        fetchNew = True
                        break
                    else:
                        fetchNew = False
                else:
                    gameListStr += line + "\n"
                ln += 1
    
    if (fetchNew):
        gameListStr = fetchNewList()
        # overwrite file with new timestamp and all games found
        with open(TEMP_FILE, "w") as file:
            file.write(str(now))
            file.write(gameListStr)
    
    # print requested lines
    gameList = gameListStr.splitlines()
    gameList = list(filter(lambda x: len(x) > 0, gameList))
    
    if (len(gameList) == 0):
        print("No Games")
    elif (printout == 0):
        for game in gameList:
            print(game)
    else:
        print(gameList[printout % len(gameList)])

# execute main
main()
