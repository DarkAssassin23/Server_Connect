# Server Connect
**Version:** 1.0<br />
**Published Date:** 11/22/2019

GENERAL USAGE NOTES
----------------------
- This software is equipped with a CLI to manage all your ssh connections
and access them anywhere on your system without having to use ssh-keygen
- Requires python version 3

---------

Setup
----------

In order to take full advantage of this software, you must first create an
alias. If you have other aliases set up add this one to them. Otherwise
in your home directory edit your .bashrc file. If you don't have one, make
one.

To add the alias type the following:

    alias connect="python3 /path/to/file/connect.py"

And add your path to the file.

------------------------

Utilizing Server Connect
----------------------

Once your alias is set up, to get help on all of the commands and what they 
do type 

	connect -h

or

	connect --help

This will display the follwing man page style menu
```bash
Server Connect interface, allows you to easily connect to and manage all your 
ssh connecitons

	[name] 		name of one of your connections your trying to
			connect to

	-h,--help	Brings up list of commands
			Ex. connect -h

	-v,--view	View the list of all your connections
			Ex. connect -v

	-a,--add 	Adds a new connection to your list of current 
			connections
			Ex. connect -a [name] [user]@[domain]

	-d,--delete 	Deletes a current connection based on the name 
			of that connection
			Ex. connect -d [name]

	-u,--update 	updates a current connection based on the name 
			and new user and domain/ip
			Ex. connect -u [name] [user]@[domain]
```
This is a list of all the current supported comands and their functionality
