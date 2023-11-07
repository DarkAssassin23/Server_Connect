#!/usr/bin/env python3
import os
def connectToServer(argv, connections):
    print("connecting...")
    # Return code
    rc = -1
    extraFlags = ""
    if(len(argv) > 2):
        extraFlags = argv[2]

    if(argv[1] in connections):
        cmd = f"ssh {connections[argv[1]][0]} {connections[argv[1]][1]} {extraFlags}"
        rc = os.system(cmd)

    else:
        if(len(argv[1].split('@')) == 2):
            cmd = f"ssh {argv[1]} {extraFlags}"
            rc = os.system(cmd)
    
    # If the return code is -1 the connection wasn't a valid connection.
    if(rc == -1):
        print(f"Unable to connect to: \"{argv[1]}\"\nMake sure it is in"+
                    " the list of connections and try again")
        print("Alternatively you can try [username]@[ip/domain]")