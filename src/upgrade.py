#!/usr/bin/env python3
from requests import get
import os
import fileHandling as fh
from fileHandling import path

# Sets the directory of connect.py
#path = fh.path# os.path.expanduser("~")+"/.ssh"

# Reaches out to check and see if there are any
# new versions of Server Connect. If so, it will
# prompt the user if they would like to update.
# If they do, the new version will be downloaded and
# installed
def upgrade(version):
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