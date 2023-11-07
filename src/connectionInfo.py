#!/usr/bin/env python3
whiteSpace = ' '

# Checks if there are any connections saved
# if there are some it prints them out
# otherwise it tells the user there are none
def viewConnections(connections):
    if(not bool(connections)):
        print("No saved connections")
        exit()
    for key,val in connections.items():
        print("Name: "+key)
        print("%sUsername and domain/ip: %s" % (whiteSpace*4, val[0]))
        if(val[1]==""):
            print("%sAdditional Flags: N/A" % (whiteSpace*4))
        else:
            print("%sAdditional Flags: %s" % (whiteSpace*4, val[1]))
        # Legacy check for older connection.txt files that have
        # not been updated to the 3.0 and later standard
        if(len(val)==2):
            print("%sMAC Address: N/A" % (whiteSpace*4))
        elif(val[2]==""):
            print("%sMAC Address: N/A" % (whiteSpace*4))
        else:
            print("%sMAC Address: %s" % (whiteSpace*4, val[2]))
        print()

def viewSingleConnection(connections, connName):
    if(not bool(connections)):
        print("No saved connections")
        exit()
    if(connName in connections):
        print("Name: "+connName)
        print("%sUsername and domain/ip: %s" % (whiteSpace*4, connections[connName][0]))
        if(connections[connName][1]==""):
            print("%sAdditional Flags: N/A" % (whiteSpace*4))
        else:
            print("%sAdditional Flags: %s" % (whiteSpace*4, connections[connName][1]))
        # Legacy check for older connection.txt files that have
        # not been updated to the 3.0 and later standard
        if(len(connections[connName])==2):
            print("%sMAC Address: N/A" % (whiteSpace*4))
        elif(connections[connName][2]==""):
            print("%sMAC Address: N/A" % (whiteSpace*4))
        else:
            print("%sMAC Address: %s" % (whiteSpace*4, connections[connName][2]))
        exit()
    else:
        print("Error: The connection \'"+connName+"\' does not exist in your list of connections")
        exit()

# Lists the names of all your connections
def listConnections(connections):
    for k in connections.keys():
        print(k)