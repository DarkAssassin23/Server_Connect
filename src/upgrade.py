#!/usr/bin/env python3
from requests import get
import os, zipfile, shutil, platform, json
import fileHandling as fh
from fileHandling import path

apiURL = "https://api.github.com/repos/DarkAssassin23/Server_Connect/releases"
baseDownloadURL = "https://github.com/DarkAssassin23/Server_Connect/releases/download/"
baseFilename = "Server_Connect-"

# Get the current latest release for Server Connect from the
# GitHub API
def getLatestRelease():
    try:
        info = json.loads(get(apiURL + "/latest").text)
    except:
        print("Error: Unable to check for updates at this time...")
        exit()
    latest = info["tag_name"].replace("v", "").strip()
    return latest

# Download the selected version, extract it, and install it
def updateServerConnect(version, isWindows, upgrading = True):
    global baseFilename
    if(isWindows):
        baseFilename += "Windows"
    else:
        baseFilename += "macOS_Linux"
    zipName = baseFilename + ".zip"

    try:
        zip = get(f"{baseDownloadURL}v{version}/{zipName}")
    except:
        print("Error: Failed to download the update")
        exit()

    try:
        with open(zipName, 'wb') as f:
            f.write(zip.content)
    except:
        print("Error: Download succeeded, but failed to write the file to disk")
        exit()

    try:
        with zipfile.ZipFile(zipName, 'r') as zip_ref:
            zip_ref.extractall(baseFilename)
    except:
        print("Error: Failed to extract the update")
        os.remove(zipName)
        exit()

    if(upgrading):
        print("Installing new version")
    else:
        print(f"Reinstalling v{version}")

    try:
        os.chdir(baseFilename)
        if(isWindows):
            if(os.path.isfile(f"{path}/connect.py")):
                os.remove(f"{path}/connect.py")
            if(os.path.isfile(f"{path}/connect.bat")):
                os.remove(f"{path}/connect.bat")
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
    except:
        print("Error: Failed to install the update")
        exit()

    if(upgrading):
        print(f"Update to ", end="")
    else:
        print("Reinstall of ", end="")
    print(f"version {version} was successful")

## Prompt the user if they want to view the release notes, if so display them
# @param url The API URL of the release to get the release notes of
# @param prompt Should the user be prompted if they want to view the release 
# notes
def getReleaseNotes(url, prompt = True):
    if(prompt):
        choice = input("Would you like to view the release notes? (y/n) ")
        if(not choice.lower() == "y"):
            print("Release notes can be viewed anytime by running: "
                  "connect -rn")
            return
    try:
        info = json.loads(get(url).text)
    except:
        print("Error: Unable to download release notes")
        exit()

    print(info["body"])

## Get the release notes for the version you have installed
# @param version Current version of Server Connect
# @param prompt Should the user be prompted if they want to view the release 
# notes
def getCurrentReleaseNotes(version, prompt = False):
    try:
        info = json.loads(get(apiURL).text)
    except:
        print("Error: Unable to query GitHub API at this time...")
        exit()
    for r in info:
        ver = r["tag_name"].replace("v", "").strip()
        if(ver == version):
            getReleaseNotes(r["url"], prompt)
            return
    print(f"Error: The version \'{version}\' does not contain release notes. " 
        "Does it exist?")

## Reinstall the current version of Server Connect
# @param version The current version of Server Connect installed
# @note If a new version is available the user will be prompted if they want
# to upgrade
def reinstall(version):
    latestVersion = getLatestRelease()
    if(version < latestVersion):
        print(f"Current Version: {version}")
        print(f"Latest Version:  {latestVersion}")
        print("A new version is available")

        choice = input("Would you like to update instead? (y/n) ")
        if(choice.lower() == "y"):
            isWindows = platform.system() == "Windows"
            updateServerConnect(latestVersion, isWindows)
            getReleaseNotes(apiURL + "/latest")
            return

    if(version > latestVersion):
        print(f"Latest Version:  {latestVersion}")
        print(f"Your Version:    {version}")
        print("Error: It appears you are trying to reinstall an unreleased "
              "version")
        return

    choice = input("Are you sure you would like to reinstall Server Connect "
                   f"v{version}? (y/n) ")
    if(choice.lower() == "y"):
        isWindows = platform.system() == "Windows"
        updateServerConnect(version, isWindows, False)
        getCurrentReleaseNotes(version, True)
        return
    else:
        print("Reinstall skipped")

# Reaches out to check and see if there are any
# new versions of Server Connect. If so, it will
# prompt the user if they would like to update.
# If they do, the new version will be downloaded and
# installed
def upgrade(version):
    latestVersion = getLatestRelease()
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
        getReleaseNotes(apiURL + "/latest")
    else:
        print("Update skipped")