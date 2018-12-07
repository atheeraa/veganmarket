this is an item catalog project for udacity's full stack nanodegree.

to run this project you need to install vagrant, virtual box, and place the project inside vagrant directory.
navigate to vagrant directory and run 
vagrant up
vagrant ssh
cd /vagrant 
python database_setup.py     // this is to set up the database structure
python veganmarket.py 	     //populat database with data
python veganmarketserver.py   //server

from your browser open: 

http://localhost:5000/

