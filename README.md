NAME: Data Transfer Regression API
AUTHOR: Alan Dinneen
PUBLISH DATE: 11/20/2015

#######################   REQUIREMENTS   ######################
1) Nginx or some other webserver
2) uWSGI 
3) Python 2.7
4) RabbitMQ
5) MongoDB


########################   DEPLOYMENT   ############################

1) Create a virtual environment in the root of the project, source it and install the requirments.txt.
2) Launch uWISGI via step 1's virtual environment uWSGI install using uwsgi.ini file included in the project.
3) Ensure RabbitMQ and MongoDB are up and running. 
4) Replace RabbitMQ and MongoDB settings in settings.py if they are different than the default install.
5) Create one or more Celery worker(s) to listen for tasks (at time or writting, emails only). 
6) Consider daemonizing all the above proccess. Daemons for uWSGI emporer mode and the Celery worker are included in the project.