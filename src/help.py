#!/usr/bin/env python3

# Prints the help menu with all the commands
# as well as what they do
def printHelp():
    print('''Server Connect allows you to easily connect to and manage all your 
ssh connections. Below is a list of the supported commands and functionality

    [name]                   Name of one of your connections you're trying to
                             connect to. Additionaly, you can append regular ssh
                             flags in quotes. You can also just enter a
                             normal ssh command with the flags in quotes.
                             Ex. connect vpn_server
                             Ex. connect vpn_server "-i ~/.ssh/id_rsa -p 2653"
                             Ex. connect vpn@192.168.54.78 "-p 2653"

    -h,--help                Brings up the list of commands
                             Ex. connect -h

    -v,--view                View the list of all your connections or a
                             single connection by typing its name
                             Ex. connect -v
                             Ex. connect -v web_server

    -l,--list                Lists the names of all your connections
                             Ex. connect -l

    -a,--add                 Adds a new connection to your list of current
                             connections with any additional ssh flags
                             Ex. connect -a [name] [user]@[domain]
                             Ex. connect -a [name] [user]@[domain] "[sshFlags]"

    -r,--rename              Renames a connection in your list
                             Ex. connect -r [currentName] [newName]

    -d,--delete              Deletes a current connection based on the name
                             of that connection
                             Ex. connect -d [name]

    -D,--delete-all          Deletes all connections
                             Ex. connect -D

    -u,--update              Updates a current connection based on the name,
                             new user, domain/ip, and ssh flags
                             Ex. connect -u [name] [user]@[domain]
                             Ex. connect -u [name] [user]@[domain] "[sshFlags]"

    -um,--update-mac         Updates/adds the MAC Address for the specified
                             connection, for use with Wake-on-LAN
                             Ex. connect -um [name]
                             Ex. connect -um [name] [MAC Address]

    -uu,--update-user        Updates a current connection's user based
                             on the name
                             Ex. connect -uu [name] [user]
                             Ex. connect -uu webserver webadmin

    -uf,--update-flags       Updates a current connection's ssh flags based
                             on the name
                             Ex. connect -uf [name] "[ssh flags]"
                             Ex. connect -uf nas "-p 34521 -i ~/.ssh/id_rsa"

    -ui,--update-ipdomain    Updates a current connection's domain/ip based
                             on the name
                             Ex. connect -ui [name] [ip/domain]
                             Ex. connect -ui vpn 192.164.1.146

    -U,--upgrade             Checks to see if there is a newer version and
                             and will automatically update for you
                             Ex. connect -U

    -i,--info                Prints out information about Server Connect
                             such as version number and copyright information
                             Ex. connect -i

    -R,--release-notes       Shows the release notes for the current version
                             of Server Connect you are running
                             Ex. connect -R

    --version                Shows what version of Server Connect you're
                             running
                             Ex. connect --version

    -scp                     Allows you to enter optional scp flags, in addition
                             to your normal scp command utilzing the name of one
                             of your connections
                             Ex. connect -scp "Documents/data.txt nas:~/Data"
                             Ex. connect -scp "-r" "Documents/Data/ nas:~/Data"

    -ping                    Pings the domain/ip of the given connection.
                             Optionally, you can pass a number for the number
                             of ICMP packets to send.
                             Ex. connect -ping nas
                             Ex. connect -ping nas 7

    -wol                     Sends a Wake-on-LAN signal to the given connection
                             Ex. connect -wol [name]
                             Ex. connect -wol plex_server
    ''')