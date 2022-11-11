#!/usr/bin/env python3
import os, sys, platform, socket, re, shutil
from requests import get
from subprocess import Popen, PIPE
if(platform.system() == "Windows"):
    from pyreadline import Readline
else:
    import readline

version = "3.0"
whiteSpace = ' '
connections = {}
# Sets the directory of connect.py
path = os.path.expanduser("~")+"/.ssh"

connectionsFile = path+"/connections"
deprecatedFile = False

# If the file exists, it reads in all the connections
def loadConnections():
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
def saveConnections():
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
        print("Your connections were read in from an older format with a deprecated filetype. "+
            "Your connections have been automatically updated to the new standard and new file format. "+
            "What would you like to do with the old file?")
        print("1. Delete it")
        print("2. Save it as a backup (default)")
        try:
            choice = int(input("Select an options: "))
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

# Prints the help menu with all the commands
# as well as what they do
def printHelp():
    print("Server Connect allows you to easily connect to "+
        "and manage all your \nssh connections. Below is a list of the supported commands and functionality\n")

    print("%s[name]%sName of one of your connections you're trying to\n%sconnect to. Additionaly, you can append regular ssh\n%sflags in quotes" % 
        (whiteSpace*4, whiteSpace*19, whiteSpace*29, whiteSpace*29))
    print("%sEx. connect vpn_server" % (whiteSpace*29))
    print("%sEx. connect vpn_server \"-i ~/.ssh/id_rsa -p 2653\"\n" % (whiteSpace*29))

    print("%s-h,--help%sBrings up the list of commands" % (whiteSpace*4, whiteSpace*16))
    print("%sEx. connect -h\n" % (whiteSpace*29))

    print("%s-v,--view%sView the list of all your connections or a\n%ssingle connection by typing its name" % (whiteSpace*4, whiteSpace*16, whiteSpace*29))
    print("%sEx. connect -v" % (whiteSpace*29))
    print("%sEx. connect -v web_server\n" % (whiteSpace*29))

    print("%s-l,--list%sLists the names of all your connections" % (whiteSpace*4, whiteSpace*16))
    print("%sEx. connect -l\n" % (whiteSpace*29))

    print("%s-a,--add%sAdds a new connection to your list of current\n%sconnections with any additional ssh flags" % 
        (whiteSpace*4, whiteSpace*17, whiteSpace*29))
    print("%sEx. connect -a [name] [user]@[domain]" % (whiteSpace*29))
    print("%sEx. connect -a [name] [user]@[domain] \"[sshFlags]\"\n" % (whiteSpace*29))

    print("%s-r,--rename%sRenames a connection in your list" % (whiteSpace*4, whiteSpace*14))
    print("%sEx. connect -r [currentName] [newName]\n" % (whiteSpace*29))

    print("%s-d,--delete%sDeletes a current connection based on the name\n%sof that connection" % 
        (whiteSpace*4, whiteSpace*14, whiteSpace*29))
    print("%sEx. connect -d [name]\n" % (whiteSpace*29))

    print("%s-D,--delete-all%sDeletes all connections" % (whiteSpace*4, whiteSpace*10))
    print("%sEx. connect -D\n" % (whiteSpace*29))

    print("%s-u,--update%sUpdates a current connection based on the name,\n%snew user, domain/ip, and ssh flags" % 
        (whiteSpace*4, whiteSpace*14, whiteSpace*29))
    print("%sEx. connect -u [name] [user]@[domain]" % (whiteSpace*29))
    print("%sEx. connect -u [name] [user]@[domain] \"[sshFlags]\"\n" % (whiteSpace*29))

    print("%s-um,--update-mac%sUpdates/adds the MAC Address for the specified\n%sconnection, for use with Wake-on-LAN" % 
        (whiteSpace*4, whiteSpace*9, whiteSpace*29))
    print("%sEx. connect -um [name]" % (whiteSpace*29))
    print("%sEx. connect -um [name] [MAC Address]\n" % (whiteSpace*29))

    print("%s-uu,--update-user%sUpdates a current connection\'s user based\n%son the name" % 
        (whiteSpace*4, whiteSpace*8, (whiteSpace*29)))
    print("%sEx. connect -uu [name] [user]" % (whiteSpace*29))
    print("%sEx. connect -uu webserver webadmin\n" % (whiteSpace*29))

    print("%s-uf,--update-flags%sUpdates a current connection\'s ssh flags based\n%son the name" % 
        (whiteSpace*4, whiteSpace*7, whiteSpace*29))
    print("%sEx. connect -uf [name] \"[ssh flags]\"" % (whiteSpace*29))
    print("%sEx. connect -uf nas \"-p 34521 -i ~/.ssh/id_rsa\"\n" % (whiteSpace*29))

    print("%s-ui,--update-ipdomain%sUpdates a current connection\'s domain/ip based\n%son the name" % 
        (whiteSpace*4, whiteSpace*4, whiteSpace*29))
    print("%sEx. connect -ui [name] [ip/domain]" % (whiteSpace*29))
    print("%sEx. connect -ui vpn 192.164.1.146\n" % (whiteSpace*29))

    print("%s-U,--upgrade%sChecks to see if there is a newer version and\n%sand will automatically update for you" % 
        (whiteSpace*4, whiteSpace*13, whiteSpace*29))
    print("%sEx. connect -U\n" % (whiteSpace*29))

    print("%s--version%sShows what version of Server Connect you're\n%srunning" % 
        (whiteSpace*4, whiteSpace*16, whiteSpace*29))
    print("%sEx. connect --version\n" % (whiteSpace*29))

    print("%s-scp%sAllows you to enter optional scp flags, in addition\n%sto your normal scp command utilzing the name of one\n%sof your connections" % 
        (whiteSpace*4, whiteSpace*21, whiteSpace*29, whiteSpace*29))
    print("%sEx. connect -scp \"Documents/data.txt nas:~/Data\"" % (whiteSpace*29))
    print("%sEx. connect -scp \"-r\" \"Documents/Data/ nas:~/Data\"\n"  % (whiteSpace*29))

    print("%s-wol%sSends a Wake-on-LAN signal to the given connection" % 
        (whiteSpace*4, whiteSpace*21))
    print("%sEx. connect -wol [name]" % (whiteSpace*29))
    print("%sEx. connect -wol plex_server\n" % (whiteSpace*29))

# Checks if there are any connections saved
# if there are some it prints them out
# otherwise it tells the user there are none
def viewConnections():
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

def viewSingleConnection(connName):
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
def listConnections():
    for k in connections.keys():
        print(k)

# Makes sure the username and domain combo
# is formated correctly
def valid(userAdomain):
    return("@" in userAdomain)

# Given the name of the connection and the
# username domain combo it either adds the
# new connection if it doesn't already exist
# or it updates the connection with additional
# ssh parameters
def update(name, userAdomain, additionalFlags = ""):
    if(not(valid(userAdomain))):
        print("Error: invalid user and domain\nmake sure to use the following"+
            " format: [user]@[domain]")
        exit()
    
    if(name in connections):
        connections[name] = [userAdomain, additionalFlags]
        saveConnections()
        print("Connection successfully updated")
    else:
        connections[name] = [userAdomain, additionalFlags]
        saveConnections()
        print("Connection successfully added")
    getMACAddress(name, False, True)
    

# If the connection exists, it deletes it
def delete(name):
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
            print("Connection renamed successfully")
        elif(validate.lower()=="n" or validate.lower()=="no"):
            print("Connection was not renamed")
        else:
            print("Error: Invalid Entry")
    else:
        print("Error: that connection does not exist")

# Reaches out to check and see if there are any
# new versions of Server Connect. If so, it will
# prompt the user if they would like to update.
# If they do, the new version will be downloaded and
# installed
def upgrade():
    try:
        globalVersion = get("https://darkassassinsinc.com/software/server-connect/version.txt").text
        if(globalVersion>version):
            response = input("There is a new version available: version "+globalVersion+"\nWould you like to update? (y/n) ")
            if(response.lower()=="y" or response.lower()=="yes"):
                try:
                    update = get("https://darkassassinsinc.com/software/server-connect/connect.py")
                    open(path+"/connect.py", 'wb').write(update.content)
                    if(platform.system() != "Windows"):
                        os.system("sudo mv "+path+"/connect.py /usr/local/bin/connect && sudo chown -R $(whoami) /usr/local/bin/connect && chmod +x /usr/local/bin/connect")
                    print("Update to version "+globalVersion+" was successful")
                except:
                    print("Error: Update failed")

            else:
                print("Update not downloaded")
        else:
            print("You are up to date!")
    except:
        print("Error: Unable to check for updates at this time...")

# Takes the list of arguments as input and then
# parses them to construct an scp command to copy files
# it searches your arguments for the name of a connection
# and if found replaces it, otherwise tells you it no connection
# exists by that name
def scp(command):
    nameOfConnection = ""
    indexLocationOfFiles = len(command)-1
    fileLocations = command[indexLocationOfFiles].split()
    colon = command[indexLocationOfFiles].find(":")
    if(colon == -1 ):
         print("Error: Invalid formating of server connection. It should look like [connection]:/path/to/file")
         exit()
    else: 
        if(" " in command[indexLocationOfFiles][:colon]):
            reverse = command[indexLocationOfFiles][:colon]
            spaceIndex = len(command[indexLocationOfFiles][:colon]) - reverse.index(" ")
        else:
            spaceIndex = 0
        
        nameOfConnection = command[indexLocationOfFiles][spaceIndex:colon].strip()
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

# Given the name of the connection and a given flag
# it updates either the connects user, domain/ip, or
# ssh parameters, depending on which flag was passed
def updatePartial(name, flag, sectionToUpdate):
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

        saveConnections()
        print("Connection successfully updated")
        getMACAddress(name, False, True)
    else:
        print("Error: That connection name does not exist in your list of connections")

# Ping the remote host, based on the given IP, to 
# ensure the host is in the ARP table, if it is 
# on the same LAN, and or, responding to pings
def pingHost(ip):
    cmd = ['ping', '-c', '1', '-t', '1', ip]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return process.returncode == 0 # code=0 means available

# Dynamically pull MAC Address of the given IP from
# the systems ARP table
def getMAC(ip):
    if(platform.system() == "Darwin"):
        arpflag = "-n"
    else:
        arpflag = "-a"
    process = Popen(["arp", arpflag, ip], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    # Make sure command succeeded
    if(process.returncode == 0):
        output = stdout.decode()
        if("no entry" in output 
            or "(incomplete)" in output
            or "no match" in output
            or "No ARP Entries" in output):
            return "N/A"
        else:
            # Strip MAC Address
            for x in output.split():
                if(re.match("[0-9a-f]{1,2}([-:])[0-9a-f]{1,2}(\\1[0-9a-f]{1,2}){4}$", x.lower())):
                    mac = x.replace("-",":")
                    break
            # Check to see if any octets are missing a leading 0
            if(len(mac)<17):
                octets = mac.split(":")
                mac = ""
                for o in octets:
                    # If current octet is missing a leading 0
                    # add it
                    if(not len(o) == 2):
                        mac += "0"
                    mac += o+":"
                # Remove the extra ':' at the end
                mac = mac[:len(mac)-1]
            return mac
    return "N/A"

# Checks to see if the given MAC Address is valid
def validMACAddress(macAddress):
    if(re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower())):
        return True
    else:
        return False

# If the MAC Address failed to be retrieved automatically 
# and the prompt flag was passed, or the user manually 
# specified a MAC Address this funciton will be called.
# it checks to make sure the MAC Address is valid before 
# adding it to the connection
def addMACAddress(name, macaddr=""):
    if(validMACAddress(macaddr)):
        while(len(connections[name])<3):
            connections[name].append("")
        connections[name][2] = macaddr
        saveConnections()
        print("MAC Address successfully added to the connection")
        exit()
    elif(not macaddr==""):
        print("Error: Invalid MAC Address")
        print("MAC Address should be formated like so: 00:11:22:33:44:55")
        exit()
    else:
        choice = input("Would you like to manually add it? (y/n) ")
    if(choice.lower() == "y"):
        mac = input(f"Enter the MAC Address for the connection \'{name}\': ")
        if(validMACAddress(mac)):
            connections[name][2] = mac
            saveConnections()
            print("MAC Address successfully added to the connection")
            exit()
        else:
            print("Error: Invalid MAC Address")
            print("MAC Address should be formated like so: 00:11:22:33:44:55")
            exit()
    elif(choice.lower() == "n"):
        print("No MAC Address added")
        exit()
    else:
        print("Invalid Choice. No MAC Address Added.\nAborting...")
        exit()

    return "N/A"

# Automatically tries to pull the MAC Address from the connection
# if it fails to do so, it will prompt the user if they would like
# to manually add the MAC Address, if the prompt flag is set to True
def getMACAddress(name, prompt=False, quiet=False):
    gotmac = False
    while(len(connections[name])<3):
        connections[name].append("")
    ip = connections[name][0].split("@")[1]
    mac = getMAC(ip)
    if(mac == "N/A"):
        if(not pingHost(ip)):
            if(prompt):
                print("Unable to dynamically pull MAC Address.")
                addMACAddress(name)
        else:
            mac = getMAC(ip)
            if(mac == "N/A"):
                if(prompt):
                    print("Unable to dynamically pull MAC Address. The given IP is not on the LAN.")
                    addMACAddress(name)
            else:
                connections[name][2] = mac
                gotmac = True 
    else:
        connections[name][2] = mac
        gotmac = True
    
    if(gotmac):
        saveConnections()
        if(not quiet):
            print("MAC Address successfully added to the connection")

def runWOL(name):
    if(len(connections[name])<3):
        print("Error: This connection does not support Wake-on-LAN")
        print("Your connection has not been updated to the latest "+
            "Server Connect 3.0\nconnection standard. You can fix this by running the "+
            "-um or --update-mac\ncommand to add a MAC Address to this connection "+
            "and bring all your\nconnections up to the Server Connect 3.0 connection standard")
    else:
        if(connections[name][2]==""):
            print("Error: There is no MAC Address associated with this connection")
            print(f"You can add it with the following command 'connect -um {name}'")
        else:    
            WOL(connections[name][2])
            print("Wake-on-LAN signal sent.")

def WOL(macAddress):
    braodcastIP = "255.255.255.255"
    # Default WOL port is 9
    wolPort = 9
    # The format of a Wake-on-LAN (WOL) magic packet is 
    # defined as a byte array with 6 bytes of value 255 (0xFF) 
    # and 16 repetitions of the target machine’s 48-bit (6-byte) MAC address.
    # ref: https://en.wikipedia.org/wiki/Wake-on-LAN#Magic_packet 
    msg = 'ff' * 6 + macAddress.replace(":","") * 16
    magicPacket = bytes.fromhex(msg)

    # Setup UDP Broadcast socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    # Send magic packet
    sock.sendto(magicPacket,(braodcastIP,wolPort))

    # Close socket
    sock.close()

# Makes sure the proper number of arguments were given
if(len(sys.argv)<2 or len(sys.argv)>5):
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
    elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
        listConnections()
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
            os.system("ssh "+connections[sys.argv[1]][0]+" "+connections[sys.argv[1]][1])
        except:
            print("Unable to connect to: \""+sys.argv[1]+"\"\nMake sure it is in"+
                  " the list of connections and try again")
        print("closing connection...")
        exit()
    
    elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        print("Error: No name given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        print("Error: No name or user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        print("Error: No name or user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
        print("Error: No name or user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-scp"):
        print("Error: No arguments given. Your command should look like \"[optionalFlags]\" \"file/to/send/ [name]:/path/on/server\" " +
                "or \"[optionalFlags]\" \"[name]:/file/on/server location/on/local/machine\", type connect -h for help")
        exit()
    elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
        print("Error: No connection given to update a MAC Address for. Type connect -h for help")
        exit()
    elif(sys.argv[1]=="-wol"):
        print("Error: No connection given to send the Wake-on-LAN signal to. Type connect -h for help")
        exit()
    elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
        print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
        exit()
    elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
        print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
        exit()
        
if(len(sys.argv)==3):
    if(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        delete(sys.argv[2])
        saveConnections()
        exit()
    elif(sys.argv[1]=="-scp"):
        scp(sys.argv)
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        viewSingleConnection(sys.argv[2])
        exit()
    elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
        if(sys.argv[2] in connections):
            getMACAddress(sys.argv[2], True)
        else:
            print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
        exit()
    elif(sys.argv[1]=="-wol"):
        if(sys.argv[2] in connections):
            runWOL(sys.argv[2])
        else:
            print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
        exit()
    elif("-" not in sys.argv[1]):
        print("connecting...")
        
        try:
            os.system("ssh "+connections[sys.argv[1]][0]+" "+connections[sys.argv[1]][1]+" "+sys.argv[2])
        except:
            print("Unable to connect to: \""+sys.argv[1]+" "+sys.argv[2]+"\"\nMake sure it is in"+
                  " the list of connections and try again")
        print("closing connection...")
        exit()

    elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        print("Error: No user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        print("Error: No user and domain given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
        print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
        exit()
    elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
        print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
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
    elif(sys.argv[1]=="-scp"):
        scp(sys.argv)
        exit()
    elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
        if(sys.argv[2] in connections):
            addMACAddress(sys.argv[2], sys.argv[3])
        else:
            print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
        exit()
    elif(sys.argv[1]=="-uu" or sys.argv[1]=="--update-user"):
        updatePartial(sys.argv[2], "-uu", sys.argv[3])
        exit()
    elif(sys.argv[1]=="-uf" or sys.argv[1]=="--update-flags"):
        updatePartial(sys.argv[2], "-uf", sys.argv[3])
        exit()
    elif(sys.argv[1]=="-ui" or sys.argv[1]=="--update-ipdomain"):
        updatePartial(sys.argv[2], "-ui", sys.argv[3])
        exit()
    
    elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-wol"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()

if(len(sys.argv)==5):
    if(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
        update(sys.argv[2],sys.argv[3],sys.argv[4])
        saveConnections()
        exit()
    elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
        update(sys.argv[2],sys.argv[3],sys.argv[4])
        saveConnections()
        exit()
    
    elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--version"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
        print("Error: Too many arguments given. Type connect -h for help")
        exit()
    elif(sys.argv[1]=="-wol"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="-scp"):
        print("Error: Too many arguments given. Your command should look like \"[optionalFlags]\" \"file/to/send/ [name]:/path/on/server\" " +
                "or \"[optionalFlags]\" \"[name]:/file/on/server location/on/local/machine\", type connect -h for help")
        exit()
    elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
    elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
        print("Error: Too many arguments given, type connect -h for help")
        exit()
else:
    print("Error: unrecognized command, type connect -h for help")
