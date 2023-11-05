#!/usr/bin/env python3
from zipfile import ZipFile
import os, sys, shutil, platform

target = "connect.py"
rootDir = os.path.dirname(os.path.realpath(__file__)) + "/"
srcDir = "src"

winPackage = "Server_Connect-Windows"
winPackageZip = winPackage + ".zip"

unixPackage = "Server_Connect-macOS_Linux"
unixPackageZip = unixPackage + ".zip"


def build():
    os.chdir(srcDir)
    files = os.listdir()
    with ZipFile(target,'w') as zip:
        for file in files:
            zip.write(file)
    shutil.move(target, f"{rootDir}{target}")
    os.chdir(rootDir)

def package(isWindows):
    folderName = ""
    installUninstallPath = "Install_Uninstall_Scripts/"
    runScript = "run_scripts/connect"
    installScript = "install"
    uninstallScript = "uninstall"

    if(isWindows):
        folderName = winPackage
        runScript += ".bat"
        prefix = installUninstallPath + "Windows" + "/"
        installScript = prefix + installScript + ".bat"
        uninstallScript = prefix + uninstallScript + ".bat"

    else:
        folderName = unixPackage
        runScript += ".sh"
        prefix = installUninstallPath + "macOS_Linux" + "/"
        installScript = prefix + installScript
        uninstallScript = prefix + uninstallScript

    filesList = [
        target,
        "README.md",
        "LICENSE",
        runScript,
        installScript,
        uninstallScript
    ]

    if(os.path.isdir(folderName)):
        shutil.rmtree(folderName)

    os.mkdir(folderName)

    for f in filesList:
        shutil.copy2(f, folderName)

def packageAll():
    package(True)
    package(False)

def zipPackage(isWindows):
    packageDir = unixPackage
    zipPack = unixPackageZip
    if(isWindows):
        packageDir = winPackage
        zipPack = winPackageZip

    os.chdir(packageDir)
    files = os.listdir()
    with ZipFile(rootDir+zipPack,'w') as zip:
        for file in files:
            zip.write(file)

    os.chdir(rootDir)


def zipAll():
    zipPackage(True)
    zipPackage(False)


def clean():
    objsToRemove = [
        target,
        winPackage,
        winPackageZip,
        unixPackage,
        unixPackageZip
    ]

    for o in objsToRemove:
        try:
            if(os.path.isdir(o)):
                shutil.rmtree(o)
            else:
                os.remove(o)
        except:
            pass

def printHelp():
    print(f"Usage: {sys.argv[0]} [option]\n\n")
    print('''Options:
    build           Create the connect.py file (default)
                    Note: if no option is passed this will be run

    package         Create a package bundle of all the files needed for
                    your given operating system

    package-all     Create packages for both Windows and Unix

    zip             Create a zip containing all the files needed for
                    your given operating system

    zip-all         Create zips for both Windows and Unix

    clean           Remove the package bundles, zip's, and connect.py
    ''')

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        build()
        exit()

    if(len(sys.argv) == 2):
        arg = sys.argv[1].lower()
        if(arg == "-h" or arg == "--help" or arg == "help"):
            printHelp()
            exit()
        elif(arg == "build"):
            build()
            exit()
        elif(arg == "clean"):
            clean()
            exit()
        elif(arg == "package"):
            build()
            package(platform.system() == "Windows")
            exit()
        elif(arg == "package-all"):
            build()
            packageAll()
            exit()
        elif(arg == "zip"):
            build()
            package(platform.system() == "Windows")
            zipPackage(platform.system() == "Windows")
            exit()
        elif(arg == "zip-all"):
            build()
            packageAll()
            zipAll()
            exit()

    print(f"Unrecognized rule \'{sys.argv[1]}\'")
    printHelp()
        
