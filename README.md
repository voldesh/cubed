# Overview
This is an example using CubesViewer application.

# Prerequisites

Clone CubesViewer Server from https://github.com/jjmontesl/cubesviewer-server and install all the modules in its requirements file.

Install the modules in requirements.txt (Run 'pip install -r requirements.txt' to download all) in this repo.

# Usage

Go to cubesviewer-server/cvapp/ to find manage.py file.

Change settings of the Django server in cubesviewer-server/cvapp/cvapp/settings.py

Migrate data for the Django server to run
python manage.py migrate

Create a superuser for Django server
python manage.py createsuperuser

Finally, run cubesviewer-server in background at user-defined address and port (optional argument) by issuing command
python manage.py runserver [address]:[port] &

Modify the slicer config in slicer.ini to run at your desired address and port
Run server in background by issuing command
slicer server slicer.ini &

Finally, run create data.py file (modify address and port in it to fetch json array) as a daemon to create data in csv which will then prepare data in SQLite format.

Now, go to the browser and open cubesviewer url to view the data.
