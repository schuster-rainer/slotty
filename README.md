# Bootstrap

In order to start developement it is a good idea to first create a virtual environment.

1. Your *nix like system normally comes pre installed with easy_install. You may also have pip
installed. If not do so: 

Ubuntu:
sudo apt-get install python-pip

or an equivalant way of installing it on your machine.

2. Run bootstrap.sh it will create a virtual environment,
install the dependencies and sets up your local workspace
as package resource, so that changes in your source are instantly
reflected in the package you are using


after the bootstrapper created your virtual environment and installed 
all dependencies you are ready to run/develop the app.

# Running

Activate the virtual environment and run the webserver. You can pass in
every option gunicorn can handle (
> source .venv/bin/activate
> ./start-server.sh

or alternativelt run the command on your own
gunicorn -k flask_sockets.worker webrms.gui.app:app --debug

The Webpage says "Hello Slotty!"

Wait some seconds and it will start to generate some fictional random
race data.

#Goals

 some fictional random
race data.

#Goals

1.Have Fun!
2. Use AngularJS (Bootstrap UI) or some other sophisticated technologi
3. Use socketIO to be backwards compatible to this old browser stuff
4. Use some decent Document Store. Maybe couchdb or redis or mongodb or something completely differnt. 
   For now json files or a one file key-value store is sufficient
5. Create a modular and easily extendible Soltcar Racing Web Management System and create some Community to write plugins
6. Listen to collaborators!
7. Manage the collaboration!
8. Did I mention fun?
