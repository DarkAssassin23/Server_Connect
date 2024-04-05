#!/usr/bin/env python3
import fileHandling as fh
from help import printHelp
from scp import scp
from connectToServer import connectToServer
from upgrade import upgrade
from upgrade import getCurrentReleaseNotes
from upgrade import reinstall
import updateConnections as update
import connectionInfo as coninfo
import wol, platform, sys

if(platform.system() == "Windows"):
    from pyreadline import Readline
else:
    import readline

version = "4.0.1"
copyrightYear = "2023"
connections = {}

def tooManyArgs():
    print("Error: Too many arguments given, type connect -h for help")
    exit()

def printInfo(full = False):
    print("Server Connect version "+version)
    if(full):
        print(f"Copyright (C) {copyrightYear} Dark Assassins Inc.")

if __name__ == "__main__":
    # Makes sure the proper number of arguments were given
    if(len(sys.argv)<2 or len(sys.argv)>5):
        print("Invalid number of arguments, type connect -h for help")
        exit()
        
    fh.loadConnections(connections)

    if(len(sys.argv)==2):
        if(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
            printHelp()
            exit()
        elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
            coninfo.viewConnections(connections)
            exit()
        elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
            update.deleteAll(connections)
            exit()
        elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
            coninfo.listConnections(connections)
            exit()
        elif(sys.argv[1]=="--version"):
            printInfo()
            exit()
        elif(sys.argv[1]=="-i" or sys.argv[1]=="--info"):
            printInfo(True)
            exit()
        elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
            upgrade(version)
            exit()
        elif(sys.argv[1]=="-R" or sys.argv[1]=="--reinstall"):
            reinstall(version)
            exit()
        elif(sys.argv[1]=="-rn" or sys.argv[1]=="--release-notes"):
            getCurrentReleaseNotes(version)
            exit()
        elif("-" not in sys.argv[1]):
            connectToServer(sys.argv, connections)
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
        elif(sys.argv[1]=="-ping"):
            print("Error: No connection given to send a ping to. Type connect -h for help")
            exit()
        elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
            print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
            exit()
        elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
            print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
            exit()
            
    if(len(sys.argv)==3):
        if(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
            update.delete(connections,sys.argv[2])
            fh.saveConnections(connections)
            exit()
        elif(sys.argv[1]=="-scp"):
            scp(connections,sys.argv)
            exit()
        elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
            coninfo.viewSingleConnection(connections,sys.argv[2])
            exit()
        elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
            if(sys.argv[2] in connections):
                wol.getMACAddress(connections,sys.argv[2], True)
            else:
                print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
            exit()
        elif(sys.argv[1]=="-wol"):
            if(sys.argv[2] in connections):
                wol.runWOL(connections,sys.argv[2])
            else:
                print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
            exit()
        elif(sys.argv[1]=="-ping"):
            if(sys.argv[2] in connections):
                wol.pingHost(connections[sys.argv[2]][0].split("@")[1], -1)
            else:
                print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
            exit()
        elif("-" not in sys.argv[1]):
            connectToServer(sys.argv, connections)
            exit()

        elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
            tooManyArgs()
        elif(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
            print("Error: No user and domain given, type connect -h for help")
            exit()
        elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
            print("Error: No user and domain given, type connect -h for help")
            exit()
        elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
            tooManyArgs()
        elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
            tooManyArgs()
        elif(sys.argv[1]=="--version"):
            tooManyArgs()
        elif(sys.argv[1]=="-i" or sys.argv[1]=="--info"):
            tooManyArgs()
        elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
            tooManyArgs()
        elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
            tooManyArgs()
        elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
            print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
            exit()
        elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
            print("Error: No name or user, domain, or flags were provided. Type connect -h for help")
            exit()
        elif(sys.argv[1]=="-rn" or sys.argv[1]=="--release-notes"):
            tooManyArgs()
        elif(sys.argv[1]=="-R" or sys.argv[1]=="--Reinstall"):
            tooManyArgs()

    if(len(sys.argv)==4):
        if(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
            update.update(connections, sys.argv[2],sys.argv[3])
            fh.saveConnections(connections)
            exit()
        elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
            update.update(connections, sys.argv[2],sys.argv[3])
            fh.saveConnections(connections)
            exit()
        elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
            update.rename(connections, sys.argv[2],sys.argv[3])
            fh.saveConnections(connections)
            exit()
        elif(sys.argv[1]=="-scp"):
            scp(connections, sys.argv)
            exit()
        elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
            if(sys.argv[2] in connections):
                wol.addMACAddress(connections, sys.argv[2], sys.argv[3])
            else:
                print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
            exit()
        elif(sys.argv[1]=="-uu" or sys.argv[1]=="--update-user"):
            update.updatePartial(connections, sys.argv[2], "-uu", sys.argv[3])
            exit()
        elif(sys.argv[1]=="-uf" or sys.argv[1]=="--update-flags"):
            update.updatePartial(connections, sys.argv[2], "-uf", sys.argv[3])
            exit()
        elif(sys.argv[1]=="-ui" or sys.argv[1]=="--update-ipdomain"):
            update.updatePartial(connections, sys.argv[2], "-ui", sys.argv[3])
            exit()
        elif(sys.argv[1]=="-ping"):
            if(sys.argv[2] in connections):
                if(sys.argv[3].isdigit()):
                    wol.pingHost(connections[sys.argv[2]][0].split("@")[1], int(sys.argv[3]))
                else:
                    print(f"Error: '{sys.argv[3]}' is not an integer")
            else:
                print(f"Error: '{sys.argv[2]}' does not exist in your connections.txt file")
            exit()
        
        elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
            tooManyArgs()
        elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
            tooManyArgs()
        elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
            tooManyArgs()
        elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
            tooManyArgs()
        elif(sys.argv[1]=="--version"):
            tooManyArgs()
        elif(sys.argv[1]=="-i" or sys.argv[1]=="--info"):
            tooManyArgs()
        elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
            tooManyArgs()
        elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
            tooManyArgs()
        elif(sys.argv[1]=="-wol"):
            tooManyArgs()
        elif(sys.argv[1]=="-rn" or sys.argv[1]=="--release-notes"):
            tooManyArgs()
        elif(sys.argv[1]=="-R" or sys.argv[1]=="--Reinstall"):
            tooManyArgs()

    if(len(sys.argv)==5):
        if(sys.argv[1]=="-u" or sys.argv[1]=="--update"):
            update.update(connections, sys.argv[2],sys.argv[3],sys.argv[4])
            fh.saveConnections(connections)
            exit()
        elif(sys.argv[1]=="-a" or sys.argv[1]=="--add"):
            update.update(connections, sys.argv[2],sys.argv[3],sys.argv[4])
            fh.saveConnections(connections)
            exit()
        
        elif(sys.argv[1]=="-r" or sys.argv[1]=="--rename"):
            tooManyArgs()
        elif(sys.argv[1]=="-h" or sys.argv[1]=="--help"):
            tooManyArgs()
        elif(sys.argv[1]=="-v" or sys.argv[1]=="--view"):
            tooManyArgs()
        elif(sys.argv[1]=="-d" or sys.argv[1]=="--delete"):
            tooManyArgs()
        elif(sys.argv[1]=="-D" or sys.argv[1]=="--delete-all"):
            tooManyArgs()
        elif(sys.argv[1]=="--version"):
            tooManyArgs()
        elif(sys.argv[1]=="-i" or sys.argv[1]=="--info"):
            tooManyArgs()
        elif(sys.argv[1]=="-l" or sys.argv[1]=="--list"):
            tooManyArgs()
        elif(sys.argv[1]=="-U" or sys.argv[1]=="--upgrade"):
            tooManyArgs()
        elif(sys.argv[1]=="-um" or sys.argv[1]=="--update-mac"):
            tooManyArgs()
        elif(sys.argv[1]=="-wol"):
            tooManyArgs()
        elif(sys.argv[1]=="-ping"):
            tooManyArgs()
        elif(sys.argv[1]=="-scp"):
            print("Error: Too many arguments given. Your command should look like \"[optionalFlags]\" \"file/to/send/ [name]:/path/on/server\" " +
                    "or \"[optionalFlags]\" \"[name]:/file/on/server location/on/local/machine\", type connect -h for help")
            exit()
        elif(sys.argv[1]=="-uu" or sys.argv[1]=="-uf" or sys.argv[1]=="-ui"):
            tooManyArgs()
        elif(sys.argv[1]=="--update-user" or sys.argv[1]=="--update-flags" or sys.argv[1]=="--update-ipdomain"):
            tooManyArgs()
        elif(sys.argv[1]=="-rn" or sys.argv[1]=="--release-notes"):
            tooManyArgs()
        elif(sys.argv[1]=="-R" or sys.argv[1]=="--Reinstall"):
            tooManyArgs()
    else:
        # A catch incase the connection has a '-' in it
        if(sys.argv[1] in connections):
            connectToServer(sys.argv, connections)
        else:
            print("Error: unrecognized command, type connect -h for help")
