# Lab Inventory
Picture this, you're an engineer that needs to replicate a networking issue in a shared lab environment. You and a group of other engineers can access
the lab devices remotely. However,
as an engineer:
- you need a way to see what devices are available to work with.
- you need a way to tell the other engineers that you are currently working with a device, so that no one hijacks it while you're logged in.

as a lab administrator:
- you need an audit trail of which engineers had worked with which devices, and their respective timestamps.

Before I created this app, all the things I previously discussed were done via email. Engineers had to send out emails to verify which devices were available
to work with, and everything was tracked by reading the group email history. It was a tedious mess.


## Introduction
The Pod request web application is built with the Django web framework using the Model-View-Template (MVT) paradigm. The project is made of two Django apps,
“auth_app” for registration and authentication, and “podrequest” for requesting and returning devices. It was built with Python 3.6 using Django 2.1.2,
and PostgreSQL.

## Models
- Engineer (one-to-one relationship with Django built-in User): keeps track of the information of
each Engineer.
- Device: the properties of a device.
- RequestHistory: keeps track of who requested what device and when (date and time) it was
requested.

## Views and URLs
Podrequest uses a mixture of Django’s Function Based Views (FBV) and Class Based Views (CBV). FBVs were used for the flexibility while CBVs were used
because they require less code.
This section discusses the views as related to the apps.

*auth_app*
- user_login: to authenticate to the web application
- register: to register new users
- user_logout: to logout a logged in user. A user must be logged in for this View to be
accessible/executed

*podrequest*
- index
- DeviceListView
- DeviceDetailView
- Requestdevice: update method was used instead of .save() because .save() requires the dataset
to be pulled first before manipulating the data and saving it back to the database. The problem with this is 
that the data might have already been changed by a different user before the
manipulated data is sent back to the database. For instance, if Alice requests a device and has a
slower connection than Bob who is requesting the same device, the device would no longer be
available by the time Alice’s request is complete. The update method solves this problem
because it simply makes the change to the database.

## Templates
Bootstrap, CSS, HTML pages.

## Database
Inventorydb.


## Deploying the Docker app
You need to [install Docker engine](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) and
docker-compose to deploy the application.
1. Navigate to the project directory, in this case *Lab Inventory*.
2. Run `docker-compose` build to build the docker containers for the project. It
would rebuild them if necessary.
3. If you’re running the containers for the first time, run `docker-compose up –d`.
You might have to run this command twice, the web application might not run, because
it can’t connect to the database. It would run the second time, because the database
container is already running.
4. You should be able to access the application in a browser using `<IP address>:<port>`.
5. If there are issues with serving static files, that is css, bootstrap and javascript files, run:
`docker exec django_web /bin/sh -c "python manage.py collectstatic --noinput"`.
The staticfiles would be put in `/static` directory so that whenever you hit the URL,
the webpages would be properly styled and behave as they should. `/static` will serve
static files from that folder.

To stop the docker containers, run `docker-compose stop`. To re-run the docker
containers, use `docker-compose start`

*For shell access to the docker containers:*

- Nginx
`docker exec -ti nginx bash`

- Web
`docker exec -ti web bash`

- Database
`docker exec -ti db bash`

*For logs:*

- Nginx
`docker-compose logs nginx`

- Web
`docker-compose logs web`

- DB
`docker-compose logs db`

## References
[1] [*Deploy Django, Gunicorn, NGINX, Postgresql using Docker*](https://ruddra.com/docker-django-nginx-postgres/).

[2] [*Serve Static Files by Nginx from Django using Docker*](https://ruddra.com/serve-static-files-by-nginx-from-django-using-docker/).
