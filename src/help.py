#!/usr/bin/env python3
whiteSpace = ' '

# Prints the help menu with all the commands
# as well as what they do
def printHelp():
    print("Server Connect allows you to easily connect to "+
        "and manage all your \nssh connections. Below is a list of the supported commands and functionality\n")

    print("%s[name]%sName of one of your connections you're trying to\n%sconnect to. Additionaly, you can append regular ssh\n%sflags in quotes. You can also just enter a\n%snormal ssh command with the flags in quotes." % 
        (whiteSpace*4, whiteSpace*19, whiteSpace*29, whiteSpace*29, whiteSpace*29))
    print("%sEx. connect vpn_server" % (whiteSpace*29))
    print("%sEx. connect vpn_server \"-i ~/.ssh/id_rsa -p 2653\"" % (whiteSpace*29))
    print("%sEx. connect vpn@192.168.54.78 \"-p 2653\"\n" % (whiteSpace*29))

    print("%s-h,--help%sBrings up the list of commands" % (whiteSpace*4, whiteSpace*16))
    print("%sEx. connect -h\n" % (whiteSpace*29))

    print("%s-v,--view%sView the list of all your connections or a\n%ssingle connection by typing its name" % (whiteSpace*4, whiteSpace*16, whiteSpace*29))
    print("%sEx. connect -v" % (whiteSpace*29))
    print("%sEx. connect -v web_server\n" % (whiteSpace*29))

    print("%s-l,--list%sLists the names of all your connections" % (whiteSpace*4, whiteSpace*16))
    print("%sEx. connect -l\n" % (whiteSpace*29))

    print("%s-a,--add%sAdds a new connection to your list of current\n%sconnections with any additional ssh flags" % 
        (whiteSpace*4, whiteSpace*17, whiteSpace*29))
    print("%sEx. connect -a [name] [user]@[domain]" % (whiteSpace*29))
    print("%sEx. connect -a [name] [user]@[domain] \"[sshFlags]\"\n" % (whiteSpace*29))

    print("%s-r,--rename%sRenames a connection in your list" % (whiteSpace*4, whiteSpace*14))
    print("%sEx. connect -r [currentName] [newName]\n" % (whiteSpace*29))

    print("%s-d,--delete%sDeletes a current connection based on the name\n%sof that connection" % 
        (whiteSpace*4, whiteSpace*14, whiteSpace*29))
    print("%sEx. connect -d [name]\n" % (whiteSpace*29))

    print("%s-D,--delete-all%sDeletes all connections" % (whiteSpace*4, whiteSpace*10))
    print("%sEx. connect -D\n" % (whiteSpace*29))

    print("%s-u,--update%sUpdates a current connection based on the name,\n%snew user, domain/ip, and ssh flags" % 
        (whiteSpace*4, whiteSpace*14, whiteSpace*29))
    print("%sEx. connect -u [name] [user]@[domain]" % (whiteSpace*29))
    print("%sEx. connect -u [name] [user]@[domain] \"[sshFlags]\"\n" % (whiteSpace*29))

    print("%s-um,--update-mac%sUpdates/adds the MAC Address for the specified\n%sconnection, for use with Wake-on-LAN" % 
        (whiteSpace*4, whiteSpace*9, whiteSpace*29))
    print("%sEx. connect -um [name]" % (whiteSpace*29))
    print("%sEx. connect -um [name] [MAC Address]\n" % (whiteSpace*29))

    print("%s-uu,--update-user%sUpdates a current connection\'s user based\n%son the name" % 
        (whiteSpace*4, whiteSpace*8, (whiteSpace*29)))
    print("%sEx. connect -uu [name] [user]" % (whiteSpace*29))
    print("%sEx. connect -uu webserver webadmin\n" % (whiteSpace*29))

    print("%s-uf,--update-flags%sUpdates a current connection\'s ssh flags based\n%son the name" % 
        (whiteSpace*4, whiteSpace*7, whiteSpace*29))
    print("%sEx. connect -uf [name] \"[ssh flags]\"" % (whiteSpace*29))
    print("%sEx. connect -uf nas \"-p 34521 -i ~/.ssh/id_rsa\"\n" % (whiteSpace*29))

    print("%s-ui,--update-ipdomain%sUpdates a current connection\'s domain/ip based\n%son the name" % 
        (whiteSpace*4, whiteSpace*4, whiteSpace*29))
    print("%sEx. connect -ui [name] [ip/domain]" % (whiteSpace*29))
    print("%sEx. connect -ui vpn 192.164.1.146\n" % (whiteSpace*29))

    print("%s-U,--upgrade%sChecks to see if there is a newer version and\n%sand will automatically update for you" % 
        (whiteSpace*4, whiteSpace*13, whiteSpace*29))
    print("%sEx. connect -U\n" % (whiteSpace*29))

    print("%s-i,--info%sPrints out information about Server Connect\n%ssuch as version number and copyright information" % 
        (whiteSpace*4, whiteSpace*16, whiteSpace*29))
    print("%sEx. connect -i\n" % (whiteSpace*29))

    print("%s--version%sShows what version of Server Connect you're\n%srunning" % 
        (whiteSpace*4, whiteSpace*16, whiteSpace*29))
    print("%sEx. connect --version\n" % (whiteSpace*29))

    print("%s-scp%sAllows you to enter optional scp flags, in addition\n%sto your normal scp command utilzing the name of one\n%sof your connections" % 
        (whiteSpace*4, whiteSpace*21, whiteSpace*29, whiteSpace*29))
    print("%sEx. connect -scp \"Documents/data.txt nas:~/Data\"" % (whiteSpace*29))
    print("%sEx. connect -scp \"-r\" \"Documents/Data/ nas:~/Data\"\n"  % (whiteSpace*29))

    print("%s-ping%sPings the domain/ip of the given connection.\n%sOptionally, you can pass a number for the number\n%sof ICMP packets to send." % 
        (whiteSpace*4, whiteSpace*20, whiteSpace*29, whiteSpace*29))
    print("%sEx. connect -ping nas" % (whiteSpace*29))
    print("%sEx. connect -ping nas 7\n" % (whiteSpace*29))

    print("%s-wol%sSends a Wake-on-LAN signal to the given connection" % 
        (whiteSpace*4, whiteSpace*21))
    print("%sEx. connect -wol [name]" % (whiteSpace*29))
    print("%sEx. connect -wol plex_server\n" % (whiteSpace*29))