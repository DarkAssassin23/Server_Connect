# Server Connect
**Version:** 4.1<br />
**Published Date:** 4/5/2024

## Table of Contents
* [General Usage](#general-usage-notes)
* [System Requirements](#system-requirements)
* ['Building' from source](#building-from-source)
* Installing Server Connect
    * [Windows](#windows-installation)
    * [macOS/Linux](#macoslinux-installation)
* [Using Server Connect](#utilizing-server-connect)
    * [Using Server Connect with SSH Flags](#utilizing-ssh-flags-with-server-connect)
    * [Using SCP with Server Connect](#utilizing-scp-with-server-connect)
    * [Using Wake-on-Lan with Server Connect](#utilizing-wake-on-lan-with-server-connect)
* Uninstalling Server Connect
    * [Windows](#windows-uninstall)
    * [macOS/Linux](#macoslinux-uninstall)

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections
  for you and access them anywhere on your system without needing to
  constantly maintain a config file for it
- As of version 2.0, this software also has support for utilizing scp via
  your existing connections.
- As of version 2.0, any new software updates can be downloaded and
  installed through the CLI itself without having to download and install 
  a new version yourself
- As of version 3.0, this software also has support to send Wake-on-LAN
  signals to connections
- As of version 3.2, this software also has support for direct ssh commands
  in addtion to names of connections
  - This allows you to now do the following:
```bash
connect user@server.local
# or with ssh flags
connect admin@10.34.79.123 "-v -p 43731"
```
- As of version 3.2, this software also has support for connection names to
  include hyphens
  - Ex. `vpn-server`
- As of version 4.0, this software now pulls updates directly from the 
  GitHub releases page. All users on version 3.2.1 or earlier will either: 
  need to run the `upgrade` command to update to 3.2.2 before running 
  another `upgrade` to upgrade to latest version, or install latest version 
  via the install script.

---------

System Requirements
----------
- Python3
- Pip3
- **Additional Requirements (Windows 10 Users Only)**
  - Windows 10 version 1803 or newer
  - Any version of Windows older than Windows 10, or any Windows 10 version
    older than version 1803, is not supported, due to Windows lack of SSH
    support on the command line.
________

'Building' From Source
----------
This is Python after all, so there is no building and compiling. However, 
with Server Connect 4.0, it is no longer a single script. It has been 
broken up into modules. For minimal changes to be needed to install and
uninstall scripts, as well as the upgrade process, rather than having 
the user run the `__main__.py` file, all of the source files will now 
be joined together to form the `connect.py` that is now in the releases. 
This file can be created by running the `buildServerConnect.py` script.

To do this, simply clone this repo, cd into it, and run the build script.
```bash
./buildServerConnect.py
# Or
python3 buildServerConnect.py
```

The easiest way to install Server Connect from source is running the 
`buildServerConnect.py` script with the `install` option.
```bash
python3 buildServerConnect.py install
```

This will build the `connect.py` file then install Server Connect 
automatically for you.

________

Windows Installation
----------
As of version 2.0 the Windows installation has been
streamlined. Simply download the Windows release from the releases tab and
run the `install.bat` file and you will be good to go.

One thing to note, though, you can install the program perfectly fine
without admin privileges, however, it is not recommended since if you do
not run the installer with admin privileges you will then have to do one
of the following:

1. Log out and log back in
2. Open `Advanced System Settings` -> `Environment Variables`, then select
  `OK` and `OK` again
3. Restart your device

Since you did run the installer as administrator, the registry environment
variables were not able to automatically propogate throughout the OS, which
is why you need to do one of the three options listed above in order to
trigger it.

If you ran the `install.bat` file as an administrator, however,
you are good to go. Just close out of any open command prompt windows
(if applicable) for their environment variables to reset.

______

macOS/Linux Installation
------------------------

To install Server Connect on macOS/Linux, download the macOS/Linux version
from the releases tab and run the install script
```bash
./install
```

------------------------

Utilizing Server Connect
----------------------

Once the installation is complete, to get help on all of the commands and
what they do type
```bash
connect -h
```
or
```bash
connect --help
```
This will display the follwing man page style menu
```
Server Connect allows you to easily connect to and manage all your
ssh connecitons. Below is a list of the supported commands and functionality

[name]                  Name of one of your connections you're trying to
                        connect to. Additionaly, you can append regular ssh
                        flags in quotes. You can also just enter a
                        normal ssh command with the flags in quotes.
                        Ex. connect vpn_server
                        Ex. connect vpn_server "-i ~/.ssh/id_rsa -p 2653"
                        Ex. connect vpn@192.168.54.78 "-p 2653"

-h,--help               Brings up the list of commands
                        Ex. connect -h

-v,--view               View the list of all your connections or a
                        single connection by typing its name
                        Ex. connect -v
                        Ex. connect -v web_server

-l,--list               Lists the names of all your connections
                        Ex. connect -l

-a,--add                Adds a new connection to your list of current
                        connections with any additional ssh flags
                        Ex. connect -a [name] [user]@[domain]
                        Ex. connect -a [name] [user]@[domain] "[sshFlags]"

-r,--rename             Renames a connection in your list
                        Ex. connect -r [currentName] [newName]

-d,--delete             Deletes a current connection based on the name
                        of that connection
                        Ex. connect -d [name]

-D,--delete-all         Deletes all connections
                        Ex. connect -D

-u,--update             Updates a current connection based on the name,
                        new user, domain/ip, and ssh flags
                        Ex. connect -u [name] [user]@[domain]
                        Ex. connect -u [name] [user]@[domain] "[sshFlags]"

-um,--update-mac        Updates/adds the MAC Address for the specified
                        connection, for use with Wake-on-LAN
                        Ex. connect -um [name]
                        Ex. connect -um [name] [MAC Address]

-uu,--update-user       Updates a current connection's user based
                        on the name
                        Ex. connect -uu [name] [user]
                        Ex. connect -uu webserver webadmin

-uf,--update-flags      Updates a current connection's ssh flags based
                        on the name
                        Ex. connect -uf [name] "[ssh flags]"
                        Ex. connect -uf nas "-p 34521 -i ~/.ssh/id_rsa"

-ui,--update-ipdomain   Updates a current connection's domain/ip based
                        on the name
                        Ex. connect -ui [name] [ip/domain]
                        Ex. connect -ui vpn 192.164.1.146

-U,--upgrade            Checks to see if there is a newer version and
                        and will automatically update for you
                        Ex. connect -U

-R,--reinstall          Reinstall the current version of Server Connect.
                        If a new version is available, you will be asked
                        if you would rather upgrade instead
                        ex. connect -R

-i,--info               Prints out information about Server Connect
                        such as version number and copyright information
                        Ex. connect -i

-rn,--release-notes     Shows the release notes for the current version
                        of Server Connect you are running
                        Ex. connect -rn

--version               Shows what version of Server Connect you're
                        running
                        Ex. connect --version

-scp                    Allows you to enter optional scp flags, in addition
                        to your normal scp command utilzing the name of one
                        of your connections
                        Ex. connect -scp "Documents/data.txt nas:~/Data"
                        Ex. connect -scp "-r" "Documents/Data/ nas:~/Data"

-ping                   Pings the domain/ip of the given connection.
                        Optionally, you can pass a number for the number
                        of ICMP packets to send.
                        Ex. connect -ping nas
                        Ex. connect -ping nas 7

-wol                    Sends a Wake-on-LAN signal to the given connection
                        Ex. connect -wol [name]
                        Ex. connect -wol plex_server
```
This is a list of all the current supported commands and their functionality
________

Utilizing SSH flags with Server Connect
----------------------

As of Server Connect version 2.0, Server Connect now has support for
utilizing SSH flags for your connections. You have two choices on how you
want to use SSH flags. You can either tack them on when connecting as a
separate one time argument in quotes, as shown here:
```
connect mediaServer "-i ~./ssh/id_rsa"
```
Or you could add a new connection, or update an existing one, and tack them
on so anytime you call connect on that connection, those flags will be
applied automatically as seen here:
```
connect -a plexServer plex@192.168.1.150 "-i ~./ssh/id_rsa"
```
```
connect -u webServer web@10.1.1.200 "-p 4523 -v"
```
Regardless of how you use them, make sure any flags you tack on come last
and are in either single or double quotes. Otherwise, it will not work
__________

Utilizing SCP with Server Connect
----------------------

As of Server Connect version 2.0, Server Connect now has support for
utilizing your existing connections for ssh to be used for scp. Any flags,
such as port number, identity files etc. will automaticly be used when
using scp with Server Connect. You still have the option to pass in your own
flags such as `-r` to copy a folder. Below are some additional example use
cases.

In this first example, say you just opened up your terminal and want to copy
a file from your Documents folder to your Documents folder on the server
```
connect -scp "Documents/file.txt fileServer:~/Documents"
```

The key here is to make sure you put either single or double quotes around
your normal scp command. Otherwise it will not work.

In this second example, say you want to copy a folder from a server, and
you want to copy it into your Downloads folder, but you are current
working directory is the Desktop
```
connect -scp "-r" "fileServer:~/Documents/DataFolder ~/Downloads"
```

The key think to note here is, any flags you want to pass must be in
either single or double quotes, and must go before, and be seprate from,
the quotes surrounding the file you want to copy and the destination you
want to copy to. Otherwise, it will not work.

__________

Utilizing Wake-on-LAN with Server Connect
------
As of Server Connect version 3.0, Server Connect now has support for
sending Wake-on-LAN magic packets to your connections.
## Prerequisites
In order to be able to utilize this feature, you first need to ensure
that your connection you wish to use this functionality with has a
MAC address associated with it. As seen in the
[Utilizing Server Connect](#utilizing-server-connect)
section, this can be done with the following command:
```bash
connect -um [nameOfConnection]
```
By running this command. Server Connect will automatically pull the
MAC address, **IF** it meets the following criteria:
1. The connection is on your LAN
2. The connection is powered on and reachable through the network

Otherwise, Server Connect will prompt you asking if you would like to
manually add the MAC address.

If you do not wish for Server Connect to automatically pull the MAC
address, you can manually set it with the following command:
```bash
connect -um [nameOfConnection] 00:11:22:33:44:55
```

Where <code>00:11:22:33:44:55</code> would be substituted with the
actual MAC address of the system.

## Using Wake-on-LAN
Once you have a MAC address associated with your connection, as seen
in the [Utilizing Server Connect](#utilizing-server-connect)
section, you can send a Wake-on-LAN signal to your connection with
the following command:
```bash
connect -wol [nameOfConnection]
```
Assuming your connection meets the following criteria, it should
begin booting

1. Wake-on-LAN is supported by the physical device and is turned on
2. The physical device is on your LAN
_________

Windows Uninstall
----------
To uninstall Server Connect on Windows run the `uninstall.bat` file as
Administrator.

______

macOS/Linux Uninstall
------------------------

To uninstall Server Connect on macOS/Linux run the uninstall script
```bash
./uninstall
```
