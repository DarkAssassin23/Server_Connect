#!/usr/bin/env python3
import os, shutil
# Sets the directory of connect.py
path = os.path.expanduser("~")+"/.ssh"

connectionsFile = path+"/connections"
deprecatedFile = False
# If the file exists, it reads in all the connections
def loadConnections(connections):
    global connectionsFile
    global deprecatedFile
    try:
        if(os.path.exists(connectionsFile+".dat")):
            connectionsFile += ".dat"
        elif(os.path.exists(connectionsFile+".txt")):
            deprecatedFile = True
            connectionsFile += ".txt"
        else:
            connectionsFile += ".dat"

        contents = []
        with open(connectionsFile,"r") as f:
            contents = f.readlines()
        for x in contents:
            # Legacy support for older connection.txt format, 
            # this format is deprecated as of version 3.0
            if(not("\0" in x)):
                temp = x.split()
                if(len(temp) == 2):
                    connections[temp[0]] = [temp[1], ""]
                elif(len(temp) > 2):
                    additionalFlags = ""
                    for x in range(2,len(temp)):
                        additionalFlags += temp[x] + " "
                    connections[temp[0]] = [temp[1], additionalFlags]
                else:
                    print("An error occured reading in your connection \""+temp[0]+"\". check your ~/.ssh/connections.txt file")
            # Current standard, as of version 3.0
            else:
                temp = x.split("\0")
                if(len(temp) == 4):
                    connections[temp[0]] = [temp[1], temp[2], temp[3].strip()]
                else:
                    print("An error occured reading in your connection \""+temp[0]+"\". check your ~/.ssh/connections.txt file")

    except:
        pass

# Saves all the connections to connections.txt
# sorted by the name of the connection
def saveConnections(connections):
    global deprecatedFile
    global connectionsFile
    try:
        if(deprecatedFile):
            connectionsFile = connectionsFile[:len(connectionsFile)-4]+".dat"
        with open(connectionsFile+".tmp","w") as file:
            for key,val in sorted(connections.items()):
                # Legacy support for old connections.txt files
                while(len(val)<3):
                    val.append("")

                file.write(key+"\0"+val[0]+"\0"+val[1]+"\0"+val[2]+"\n")
        shutil.move(connectionsFile+".tmp", connectionsFile)
    except:
        print("An error occured saving your connections.\nAborting...")
        exit()
    if(deprecatedFile):
        print("Your connections were read in from an older format with a deprecated filetype.\n"+
            "Your connections have been automatically updated to the new standard and new\nfile format. "+
            "What would you like to do with the old file?")
        print("1. Delete it")
        print("2. Save it as a backup (default)")
        try:
            choice = int(input("Select an option: "))
            if(choice == 1):
                os.remove(connectionsFile[:len(connectionsFile)-4]+".txt")
                print("Old file deleted")
            else:
                shutil.move(connectionsFile[:len(connectionsFile)-4]+".txt", connectionsFile[:len(connectionsFile)-4]+".txt.bak")
                print(f"Old connections file renamed to \'connections.txt.bak\'")
        except:
            shutil.move(connectionsFile[:len(connectionsFile)-4]+".txt", connectionsFile[:len(connectionsFile)-4]+".txt.bak")
            print(f"Old connections file renamed to \'connections.txt.bak\'")
        deprecatedFile = False
