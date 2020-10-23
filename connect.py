#!/usr/bin/python3
import os, readline, sys

connections = {}

# Sets the directory of connect.py
path = os.path.expanduser("~")+"/.ssh"

# If the file exists, it reads in all the connections
def loadConnections():
    try:
        contents = []
        with open(path+"/connections.txt","r") as f:
            contents = f.readlines()
        for x in contents:
            temp = x.split()
            connections[temp[0]] = temp[1]
    except:
        pass

# Saves all the connections to connections.txt
def saveConnections():
    with open(path+"/connections.txt","w") as file:
        for key,val in connections.items():
            file.write(key+" "+val+"\n")

# Prints the help menu with all the commands
# as well as what they do
def printHelp():
    print("Server Connect interface, allows you to easily connect to "+
        "and manage all your \nssh connecitons\n")
    print("\t[name] \t\t\tName of one of your connections your trying to\n\t\t\t\t"+
    "connect to")
    print("\t\t\t\tEx. connect vpn_server\n")
    print("\t-h,--help\t\tBrings up list of commands")
    print("\t\t\t\tEx. connect -h\n")
    print("\t-v,--view\t\tView the list of all your connections")
    print("\t\t\t\tEx. connect -v\n")
    print("\t-a,--add \t\tAdds a new connection to your list of "+
        "current \n\t\t\t\tconnections")
    print("\t\t\t\tEx. connect -a [name] [user]@[domain]\n")
    print("\t-d,--delete \t\tDeletes a current connection based on the name "+
        "\n\t\t\t\tof that connection")
    print("\t\t\t\tEx. connect -d [name]\n")
    print("\t-D,--delete-all \tDeletes all connections")
    print("\t\t\t\tEx. connect -D\n")
    print("\t-u,--update \t\tUpdates a current connection based on the name "+
        "\n\t\t\t\tand new user and domain/ip")
    print("\t\t\t\tEx. connect -u [name] [user]@[domain]\n")
    print("\t--version \t\tShows what version of Server Connect you're "+
        "\n\t\t\t\trunning")
    print("\t\t\t\tEx. connect --version\n")
    print()
    
# Checks if there are any connections saved
# if there are some it prints them out
# otherwise it tells the user there are none
def viewConnections():
    if(not bool(connections)):
        print("No saved connections")
        exit()
    for key,val in connections.items():
        print("Name: "+key+", Username and domain/ip: "+val)

# Makes sure the username and domain combo
# is formated correctly
def valid(userAdomain):
    return("@" in userAdomain)

# Given the name of the connection and the
# username domain combo it either adds the
# new connection if it doesn't already exist
# or it updates the connection
def update(name, userAdomain):
    if(not(valid(userAdomain))):
        print("Error: invalid user and domain\nmake sure to use the following"+
            " fromat: [user]@[domain]")
        exit()
    if(name in connections):
        connections[name] = userAdomain
        print("Connection sucessfully updated")
    else:
        connections[name] = userAdomain
        print("Connection sucessfully added")
    saveConnections()

# If the connection exists, it deletes it
def delete(name):
    if(name in connections):
        validate = input("Are you sure you would like to delete the conneciton "+name+" (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            del connections[name]
            print("Connection deleted sucessfully")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connection was not deleted")
        else:
            print("Error: Invalid Entry, connections were not deleted")
    else:
        print("Error: that connection does not exist")

# Deletes all connections
def deleteAll():
    if(not(os.path.isfile(path+"/connections.txt"))):
        print("There are no connections to delete")
    else:
        validate = input("Are you sure you would like to delete all your connections (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            os.system("rm "+path+"/connections.txt")
            print("Connections deleted")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connections were not deleted")
        else:
            print("Error: Invalid Entry, connections were not deleted")

# Makes sure the proper number of arguments were given
if(len(sys.argv)<2 or len(sys.argv)>4):
    print("Invalid number of arguments, type connect -h for help")
    exit()
    
loadConnections()

if(len(sys.argv)==2):
    if(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        printHelp()
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        viewConnections()
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        deleteAll()
        exit()
    elif(sys.argv[1]=="--version"):
        print("Server Connect version 1.2")
        exit()
    elif("-" not in sys.argv[1]):
        print("connecting...")
        
        try:
            os.system("ssh "+connections[sys.argv[1]])
        except:
            print("Unable to connect to: \""+sys.argv[1]+"\"\nmake sure it is in"+
                  " the list of connections and try again")
        print("closing connection...")
        exit()
    
    elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        print("Error: no name given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        print("Error: no name or user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        print("Error: no name or user and domain given, type connect -h for help")
        exit()
        
if(len(sys.argv)==3):
    if(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        delete(sys.argv[2])
        saveConnections()
        exit()
        
    elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        print("Error: no user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        print("Error: no user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
if(len(sys.argv)==4):
    if(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        update(sys.argv[2],sys.argv[3])
        saveConnections()
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        update(sys.argv[2],sys.argv[3])
        saveConnections()
        exit()
    
    elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
else:
    print("Error: unrecognized command, type connect -h for help")
