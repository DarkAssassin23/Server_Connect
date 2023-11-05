#!/usr/bin/env python3
import os

# Takes the list of arguments as input and then
# parses them to construct an scp command to copy files
# it searches your arguments for the name of a connection
# and if found replaces it, otherwise tells you it no connection
# exists by that name
def scp(connections, command):
    nameOfConnection = ""
    indexLocationOfFiles = len(command)-1
    fileLocations = command[indexLocationOfFiles].split()
    colon = command[indexLocationOfFiles].find(":")
    if(colon == -1 ):
         print("Error: Invalid formating of server connection. It should look like [connection]:/path/to/file")
         exit()
    else: 
        nameWithExtras = command[indexLocationOfFiles][:colon].split()
        nameOfConnection = nameWithExtras[len(nameWithExtras)-1]
               
    try:
        command[indexLocationOfFiles] = command[indexLocationOfFiles].replace(nameOfConnection+":", connections[nameOfConnection][0]+":",1)
        additionalCommands = connections[nameOfConnection][1]
        additionalCommands = additionalCommands.replace("-p","-P")
        scpCommand = ""
        if(indexLocationOfFiles==3):
            scpCommand = "scp "+command[2]+" "+additionalCommands+" "+command[indexLocationOfFiles]
        else:
            scpCommand = "scp "+additionalCommands+" "+command[indexLocationOfFiles]
        os.system(scpCommand)
    except:
        if(indexLocationOfFiles==3):
            print("Unable to connect to: \""+nameOfConnection+"\" in \"scp "+command[2]+" "+command[indexLocationOfFiles]+"\"\nMake sure it is in"+
                    " the list of connections and try again")
        else:
            print("Unable to connect to: \""+nameOfConnection+"\" in \"scp "+command[indexLocationOfFiles]+"\"\nMake sure it is in"+
                    " the list of connections and try again")