This is an item catalog project for udacity's full stack nanodegree. It's a simple webserver that stores some vegan products.

To run this project you need to install vagrant, virtual box, and place the project inside vagrant directory.
navigate to vagrant directory and run 
vagrant up
vagrant ssh
cd /vagrant 
python database_setup.py     // this is to set up the database structure
python veganmarket.py 	     //populat database with data
python veganmarketserver.py   //server

from your browser open: 

http://localhost:5000/

You can easily navigate the webserver, it has got a nice easy-to-find-your-way-around interface>
There is a dedicated page for using API endpoints which are :

JSON for all the departments : '/departments/JSON'
JSON for a specific item, replace departmetent_id and item_id with valid ids: '/departments/ department_id/items/ item_id/JSON'
JSON for a specific department, replace department_id with a valid id: '/departments/department_id/items/JSON'
