#!/usr/bin/env python3
import os
import fileHandling as fh
from fileHandling import path

# Sets the directory of connect.py
#path = fh.path# os.path.expanduser("~")+"/.ssh"

# Makes sure the username and domain combo
# is formated correctly
def valid(userAdomain):
    return("@" in userAdomain)

# Given the name of the connection and the
# username domain combo it either adds the
# new connection if it doesn't already exist
# or it updates the connection with additional
# ssh parameters
def update(connections, name, userAdomain, additionalFlags = ""):
    if(not(valid(userAdomain))):
        print("Error: invalid user and domain\nmake sure to use the following"+
            " format: [user]@[domain]")
        exit()
    
    if(name in connections):
        connections[name] = [userAdomain, additionalFlags]
        fh.saveConnections(connections)
        print("Connection successfully updated")
    else:
        connections[name] = [userAdomain, additionalFlags]
        fh.saveConnections(connections)
        print("Connection successfully added")
    getMACAddress(name, False, True)
    

# Given the name of the connection and a given flag
# it updates either the connects user, domain/ip, or
# ssh parameters, depending on which flag was passed
def updatePartial(connection, name, flag, sectionToUpdate):
    if(name in connections):
        if(flag=="-uf"):
            connections[name][1] = sectionToUpdate
        else:
            userADomain = connections[name][0].split("@")
            if(flag=="-uu"):
                userADomain[0] = sectionToUpdate
            else:
                userADomain[1] = sectionToUpdate
            result = userADomain[0]+"@"+userADomain[1]
            connections[name][0] = result

        fh.saveConnections(connections)
        print("Connection successfully updated")
        getMACAddress(name, False, True)
    else:
        print("Error: That connection name does not exist in your list of connections")

# If the connection exists, it deletes it
def delete(connections, name):
    if(name in connections):
        validate = input("Are you sure you would like to delete the conneciton "+name+" (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            del connections[name]
            print("Connection deleted successfully")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connection was not deleted")
        else:
            print("Error: Invalid Entry, connections were not deleted")
    else:
        print("Error: that connection does not exist")

# Deletes all connections
def deleteAll(connections):
    if(not(os.path.isfile(path+"/connections.dat"))):
        print("There are no connections to delete")
    else:
        validate = input("Are you sure you would like to delete all your connections (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            os.system("rm "+path+"/connections.dat")
            print("Connections deleted")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connections were not deleted")
        else:
            print("Error: Invalid Entry, connections were not deleted")

# If the connection exists, it renames it to the new name
def rename(connections, oldName, newName):
    if(oldName in connections):
        validate = input("Are you sure you would like to rename the conneciton "+oldName+" to "+newName+" (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            connections[newName] = connections.pop(oldName)
            print("Connection renamed successfully")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connection was not renamed")
        else:
            print("Error: Invalid Entry")
    else:
        print("Error: that connection does not exist")