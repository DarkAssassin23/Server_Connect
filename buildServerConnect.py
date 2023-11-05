#!/usr/bin/env python3
from zipfile import ZipFile
import os, sys, shutil

target = "connect.py"
rootDir = os.path.dirname(os.path.realpath(__file__))
srcDir = "src"

def build():
    os.chdir(srcDir)
    files = os.listdir()
    with ZipFile(target,'w') as zip:
        for file in files:
            zip.write(file)
    shutil.move(target, f"{rootDir}/{target}")

def clean():
    os.remove(target)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        build()
        exit()

    if(len(sys.argv) == 2):
        if(sys.argv[1].lower() == "build"):
            build()
            exit()
        elif(sys.argv[1].lower() == "clean"):
            clean()
            exit()
  
    print(f"Unrecognized rule \'{sys.argv[1]}\'")
        
