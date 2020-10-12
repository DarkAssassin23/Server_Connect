# Server Connect
**Version:** 1.1<br />
**Published Date:** 10/12/2020

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections
and access them anywhere on your system without having to use ssh-keygen
- Requires python version 3

---------

Installation
----------

To install Server Connect run the install script
```bash
sudo ./install
```
Make sure you run install script as root otherwise it won't work

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
