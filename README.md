# Server Connect
**Version:** 3.0<br />
**Published Date:** 11/6/2022

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections for you
and access them anywhere on your system without needing to constantly maintain a config
file for it
- As of version 2.0, this software also has support for utilizing scp via your existing
connections.
- As of version 2.0, any new software updates can be downloaded and installed through the
CLI itself without having to download and install a new version yourself
- As of version 3.0, this software also has support to send Wake-on-LAN signals to connections

---------

System Requirenments 
----------
- Python3
- Pip3
- **Additional Requirements (Windows 10 Users Only)**
  - Windows 10 version 1803 or newer
  - Any version of Windows older than Windows 10, or any Windows 10 version older than version 1803, is not supported, due to Windows lack of SSH support on the command line.
________

Windows Installation
----------
Compared to previous versions, As of version 2.0 the Windows installation has been 
streamlined. Simply run the `install.bat` file. and you will be good to go.

One thing to note, can install the program perfectly fine without admin privileges, 
however, it is not recommended since if you do not run the installer with admin 
privileges you will then have to do one of the follwoing:

1. Log out and log back in
2. Open 'Advanced System Settings' -> Environment Variables, then select 'OK' and 'OK' again
3. Restart your device

Since you did run the installer as administrator, the registry environment variables were 
not able to automatically propogate throughout the OS, which is why you need to do one of 
the three options listed above in order to trigger it.

If you ran the `install.bat` file as an administrator, however, you are good to go.
Just close out of any open command prompt windows (if applicable) for their environment 
variables to reset.

______

macOS/Linux Installation
------------------------

To install Server Connect on macOS/Linux run the install script
```bash
./install
```

------------------------

Utilizing Server Connect
----------------------

Once the installation is complete, to get help on all of the commands and what they 
do type 

	connect -h

or

	connect --help

This will display the follwing man page style menu
```
Server Connect interface, allows you to easily connect to and manage all your 
ssh connecitons

	[name] 			Name of one of your connections your trying to
				connect to. Additionaly, you can append regular ssh
                		flags in quotes
				Ex. connect vpn_server
				Ex. connect vpn_server "-i ~/.ssh/id_rsa -p 2653"

	-h,--help		Brings up list of commands
				Ex. connect -h

	-v,--view		View the list of all your connections
				single connection by typing its name
				Ex. connect -v
				Ex. connect -v web_server

	-a,--add 		Adds a new connection to your list of current 
				connections with any additional ssh flags
				Ex. connect -a [name] [user]@[domain]
				Ex. connect -a [name] [user]@[domain] "[sshFlags]"

	-r,--rename		Renames a connection in your list
				Ex. connect -r [currentName] [newName]

	-d,--delete 		Deletes a current connection based on the name 
				of that connection
				Ex. connect -d [name]
	
	-D,--delete-all		Deletes all connections
				Ex. connect -D

	-u,--update 		Updates a current connection based on the name,
                		new user and domain/ip, and ssh flags
				Ex. connect -u [name] [user]@[domain]
				Ex. connect -u [name] [user]@[domain] "[sshFlags]"
	
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
	
	-U,--upgrade        	Checks to see if there is a newer version and
                		and will automatically update for you
                		Ex. connect -U
				
	--version		Shows what version of Server Connect you're
				running
				Ex. connect --version	

    	-scp            	Allows you to enter optional scp flags, in addition
                		to your normal scp command utilzing the name of one
                		of your connections
                		Ex. connect -scp "Documents/data.txt nas:~/Data"
                		Ex. connect -scp "-r" "Documents/Data/ nas:~/Data"	
```
This is a list of all the current supported comands and their functionality
________

Utilizing SSH flags with Server Connect
----------------------

As of Server Connect version 2.0, Server Connect now has support for utilizing SSH flags 
for your connections. You have two choices on how you want to use SSH flags. You can 
either tack them on when connecting as a separate one time argument in quotes, 
as shown here:
```
connect mediaServer "-i ~./ssh/id_rsa"
```
Or you could add a new connection, or update an existing one, and tack them on so anytime
you call connect on that connection, those flags will be applied automatically as seen 
here:
```
connect -a plexServer plex@192.168.1.150 "-i ~./ssh/id_rsa"
```
```
connect -u webServer web@10.1.1.200 "-p 4523 -v"
```
Regardless of how you use them, make sure any flags you tack on come last and are in 
either single or double quotes. Otherwise, it will not work
__________

Utilizing SCP with Server Connect
----------------------

As of Server Connect version 2.0, Server Connect now has support for utilizing your 
existing connections for ssh to be used for scp. Any flags, such as port number, identity 
files etc. will automaticly be used when using scp with Server Connect. You still have 
the option to pass in your own flags such as `-r` to copy a folder. Below are some 
additional example use cases.

In this first example, say you just opened up your terminal and want to copy a file from 
your Documents folder to your Documents folder on the server
```
connect -scp "Documents/file.txt fileServer:~/Documents"
```

The key here is to make sure you put either single or double quotes around your normal 
scp command. Otherwise it will not work. 

In this second example, say you want to copy a folder from a server, and you want to copy 
it into your Downloads folder, but you are current working directory is the Desktop
```
connect -scp "-r" "fileServer:~/Documents/DataFolder ~/Downloads"
```

The key think to note here is, any flags you want to pass must be in either single or 
double quotes, and must go before, and be seprate from, the quotes surrounding the file 
you want to copy and the destination you want to copy to. Otherwise, it will not work. 

__________

Utilizing Wake-on-LAN with Server Connect

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
