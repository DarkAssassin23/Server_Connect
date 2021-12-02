# Server Connect
**Version:** 2.0<br />
**Published Date:** 12/2/2021

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections for you
and access them anywhere on your system without having to use ssh-keygen and needing to
maintain a config file for it

---------

System Requirenments 
----------
- Python3
- Pip3
- **Additional Requirements (Windows Users Only)**
  - Windows 10 version 1803 or newer
________

Windows Installation
----------
Compared to previous versions, the Windows installation has been streamlined.
Simply run the ```install.bat``` file. and you will be good to go.

One thing to note, while you can install the program without admin privileges, you will
then have to either

1. Log out and log back in
2. Open 'Advanced System Settings' -> Environment Variables, then select 'OK' and 'OK' again
3. Restart your device

In order for the registry environment variable to propogate through the OS.

If you ran the ```install.bat``` file as an administrator, however, you are good to go.
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

Windows Uninstall
----------
To uninstall Server Connect on Windows run the ```uninstall.bat``` file as 
Administrator. Otherwise, it will not work 

______

macOS/Linux Uninstall
------------------------

To uninstall Server Connect on macOS/Linux run the uninstall script
```bash
./uninstall
```

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
				connect to

	-h,--help		Brings up list of commands
				Ex. connect -h

	-v,--view		View the list of all your connections
				Ex. connect -v

	-a,--add 		Adds a new connection to your list of current 
				connections
				Ex. connect -a [name] [user]@[domain]

	-r,--rename		Renames a connection in your list
				Ex. connect -r [currentName] [newName]

	-d,--delete 		Deletes a current connection based on the name 
				of that connection
				Ex. connect -d [name]
	
	-D,--delete-all		Deletes all connections
				Ex. connect -D

	-u,--update 		Updates a current connection based on the name 
				and new user and domain/ip
				Ex. connect -u [name] [user]@[domain]
				
	--version		Shows what version of Server Connect you're
				running
				Ex. connect --version	
```
This is a list of all the current supported comands and their functionality
________
