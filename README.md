# Server Connect
**Version:** 1.1<br />
**Published Date:** 10/12/2020

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections
and access them anywhere on your system without having to use ssh-keygen

---------

System Requirenments 
----------
- Python 3
- **Additional Requirements (Windows Users Only)**
  - Windows 10 version 1803 or later
________

Windows Installation
----------

Make sure you have python set up as an environment variable. Also make sure that the
pyreadline package is installed. That can be done via the command line with the following command
```bash
pip install --user pyreadline
```

If you already have those installed, double click on the install.bat file to install.
You will then be prompted with the following diologue
```bash
Value Path exists, overwrite(Yes/No)?
```
Enter 'yes'. This will update your environment path registry which will allow you to execute Server
Connect from anywhere on the command line.

The last step is to reboot your computer and you're good to go.
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
```bash
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

	-d,--delete 		Deletes a current connection based on the name 
				of that connection
				Ex. connect -d [name]
	
	-D,--delete-all		Deletes all connections
				Ex. connect -D

	-u,--update 		Updates a current connection based on the name 
				and new user and domain/ip
				Ex. connect -u [name] [user]@[domain]
```
This is a list of all the current supported comands and their functionality
