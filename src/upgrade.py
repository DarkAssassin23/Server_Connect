#!/usr/bin/env python3
from requests import get
import os, zipfile, shutil, platform
import fileHandling as fh
from fileHandling import path

# Sets the directory of connect.py
baseDownloadURL = "https://github.com/DarkAssassin23/Server_Connect/releases/download/"
baseFilename = "Server_Connect-"

def getLatestRelease():
    latest = get("https://github.com/DarkAssassin23/Server_Connect/releases/latest").text
    latest = latest[latest.find("<title>"):latest.find("</title>")].replace("Server Connect", "")
    releaseStart = latest.find("v") + 1
    latest = latest[releaseStart:].split(" ")
    latest = latest[0].strip()
    return latest

def updateServerConnect(version, isWindows):
    global baseFilename
    if(isWindows):
        baseFilename += "Windows"
    else:
        baseFilename += "macOS_Linux"
    zipName = baseFilename + ".zip"

    zip = get(f"{baseDownloadURL}v{version}/{zipName}")
    with open(zipName, 'wb') as f:
        f.write(zip.content)

    with zipfile.ZipFile(zipName, 'r') as zip_ref:
        zip_ref.extractall()

    print("Installing new version")
    os.chdir(baseFilename)
    if(isWindows):
        shutil.move("connect.py", f"{path}/")
        shutil.move("connect.bat", f"{path}/")
    else:
        dest = "/usr/local/bin/"
        os.system(f"sudo mv connect.py {dest} && sudo mv connect.sh {dest}/connect") 
        os.system(f"sudo chown -R $(whoami) {dest}connect && chmod +x {dest}connect")
    os.chdir("..")

    os.remove(zipName) 
    shutil.rmtree(baseFilename)
    if(os.path.isdir("__MACOSX")):
        shutil.rmtree("__MACOSX")

    print(f"Update to version {version} was successful")

# Reaches out to check and see if there are any
# new versions of Server Connect. If so, it will
# prompt the user if they would like to update.
# If they do, the new version will be downloaded and
# installed
def upgrade(version):
    latestVersion = getLatestRelease()
    #Testing
    version = "2.0"
    if(version >= latestVersion):
        print("You are up to date!")
        exit(0)

    print(f"Current Version: {version}")
    print(f"Latest Version:  {latestVersion}")
    print("A new version is available")

    choice = input("Would you like to update? (y/n) ")
    if(choice.lower() == "y"):
        isWindows = platform.system() == "Windows"
        updateServerConnect(latestVersion, isWindows)
    else:
        print("Update skipped")