#!/usr/bin/python3
import os, sys, platform
from requests import get
if(platform.system() == "Windows"):
    from pyreadline import Readline
else:
    import readline

version = "2.0"
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
# sorted by the name of the connection
def saveConnections():
    with open(path+"/connections.txt","w") as file:
        for key,val in sorted(connections.items()):
            file.write(key+" "+val+"\n")

# Prints the help menu with all the commands
# as well as what they do
def printHelp():
    print("Server Connect interface, allows you to easily connect to "+
        "and manage all your \nssh connecitons\n")

    whiteSpace = ' '
    print("%s[name]%sName of one of your connections your trying to\n%sconnect to" % 
        (whiteSpace*8, whiteSpace*18, whiteSpace*32))
    print("%sEx. connect vpn_server\n" % (whiteSpace*32))

    print("%s-h,--help%sBrings up list of commands" % (whiteSpace*8, whiteSpace*15))
    print("%sEx. connect -h\n" % (whiteSpace*32))

    print("%s-v,--view%sView the list of all your connections" % (whiteSpace*8, whiteSpace*15))
    print("%sEx. connect -v\n" % (whiteSpace*32))

    print("%s-a,--add%sAdds a new connection to your list of current\n%sconnections" % 
        (whiteSpace*8, whiteSpace*16, whiteSpace*32))
    print("%sEx. connect -a [name] [user]@[domain]\n\n" % (whiteSpace*32))

    print("%s-r,--rename%sRenames a connection in your list" % (whiteSpace*8, whiteSpace*13))
    print("%sEx. connect -r [currentName] [newName]\n" % (whiteSpace*32))

    print("%s-d,--delete%sDeletes a current connection based on the name\n%sof that connection" % 
        (whiteSpace*8, whiteSpace*13, whiteSpace*32))
    print("%sEx. connect -d [name]\n" % (whiteSpace*32))

    print("%s-D,--delete-all%sDeletes all connections" % (whiteSpace*8, whiteSpace*9))
    print("%sEx. connect -D\n" % (whiteSpace*32))

    print("%s-u,--update%sUpdates a current connection based on the name\n%sand new user and domain/ip" % 
        (whiteSpace*8, whiteSpace*13, whiteSpace*32))
    print("%sEx. connect -u [name] [user]@[domain]\n" % (whiteSpace*32))

    print("%s-U,--upgrade%sChecks to see if there is a newer version and\n%sand will automatically update for you" % 
        (whiteSpace*8, whiteSpace*12, whiteSpace*32))
    print("%sEx. connect -U\n" % (whiteSpace*32))

    print("%s--version%sShows what version of Server Connect you're\n%srunning" % 
        (whiteSpace*8, whiteSpace*15, whiteSpace*32))
    print("%sEx. connect --version\n" % (whiteSpace*32))

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

# If the connection exists, it renames it to the new name
def rename(oldName, newName):
    if(oldName in connections):
        validate = input("Are you sure you would like to rename the conneciton "+oldName+" to "+newName+" (y/n)? ")
        if(validate.lower()=="y" or validate.lower()=="yes"):
            connections[newName] = connections.pop(oldName)
            print("Connection renamed sucessfully")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connection was not renamed")
        else:
            print("Error: Invalid Entry")
    else:
        print("Error: that connection does not exist")

def upgrade():
    globalVersion = get("https://darkassassinsinc.com/software/server-connect/version.txt").text
    if(globalVersion>version):
        response = input("There is a new version available: version "+globalVersion+"\nWould you like to update? (y/n) ")
        if(response.lower()=="y" or response.lower()=="yes"):
            try:
                update = get("https://darkassassinsinc.com/software/server-connect/connect.py")
                open(path+"/connect.py", 'wb').write(update.content)
                if(platform.system() != "Windows"):
                    os.system("sudo mv "+path+"/connect.py /usr/local/bin/connect && sudo chown -R $(whoami) /usr/local/bin/connect && chmod +x /usr/local/bin/connect")
                print("Update to version "+globalVersion+" was sucessful")
            except:
                print("Error: Update failed")

        else:
            print("Update not downloaded")
    else:
        print("You are up to date!")

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
        print("Server Connect version "+version)
        exit()
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
        upgrade()
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
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
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
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
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
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
        rename(sys.argv[2],sys.argv[3])
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
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
        print("Error: too many arguments given, type connect -h for help")
        exit()
else:
    print("Error: unrecognized command, type connect -h for help")
