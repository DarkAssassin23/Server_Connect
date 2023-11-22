#!/usr/bin/env python3
from subprocess import Popen, PIPE
import socket, platform, re, os
import fileHandling as fh


# Ping the remote host, based on the given IP, to 
# ensure the host is in the ARP table, if it is 
# on the same LAN, and or, responding to pings
def pingHost(ip, numPings = 0):
    try:
        if(numPings==0):
            cmd = ['ping', '-c', '1', '-t', '1', ip]
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            return process.returncode == 0 # code=0 means available
        elif(numPings>0):
            numPingsFlag = '-c'
            if(platform.system()=="Windows"):
                numPingsFlag = '-n'
            os.system('ping '+numPingsFlag+' '+str(numPings)+' '+ip)
        else:
            if(platform.system()=="Windows"):
                os.system("ping -t "+ip)
            else:
                os.system("ping "+ip)
    except KeyboardInterrupt:
        print("\nStopping ping...")

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
            try:
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
            except:
                pass
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
def addMACAddress(connections, name, macaddr=""):
    if(validMACAddress(macaddr)):
        while(len(connections[name])<3):
            connections[name].append("")
        connections[name][2] = macaddr
        fh.saveConnections(connections)
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
            fh.saveConnections(connections)
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
def getMACAddress(connections, name, prompt=False, quiet=False):
    gotmac = False
    while(len(connections[name])<3):
        connections[name].append("")
    ip = connections[name][0].split("@")[1]
    mac = getMAC(ip)
    if(mac == "N/A"):
        if(not pingHost(ip)):
            if(prompt):
                print("Unable to dynamically pull MAC Address.")
                addMACAddress(connections, name)
        else:
            mac = getMAC(ip)
            if(mac == "N/A"):
                if(prompt):
                    print("Unable to dynamically pull MAC Address. The given IP is not on the LAN.")
                    addMACAddress(connections, name)
            else:
                connections[name][2] = mac
                gotmac = True 
    else:
        connections[name][2] = mac
        gotmac = True
    
    if(gotmac):
        fh.saveConnections(connections)
        if(not quiet):
            print("MAC Address successfully added to the connection")

def runWOL(connections, name):
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

    try:
        # Send magic packet
        sock.sendto(magicPacket,(braodcastIP,wolPort))

        # Close socket
        sock.close()
    except:
        print("An error occured sending WOL packet. This can happen if you\n"
            "are trying to send a WOL packet on a device connected via VPN")
        exit()

