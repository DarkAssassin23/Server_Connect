#!/usr/bin/env python3
from zipfile import ZipFile
import os, sys

target = "connect.py"
srcDir = "src"

def build():
    files = os.listdir(srcDir)
    with ZipFile(target,'w') as zip:
        for file in files:
            zip.write(f"{srcDir}/{file}")

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
        
