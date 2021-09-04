# Hotel Management

_A web app using django framework to manage hotels for different cities._

### How to setup

* The file _env`_`file_ in the main directory must be updated with the following environmental variables:  
  * SECRET_KEY (django settings)  
  * MC_URL (city's url)  
  * MH_URL (hotel's url)  
  * M_USERNAME (api username)  
  * M_PASSWORD (api password)  
* [Install docker-compose](https://docs.docker.com/compose/install/)  
### Setup the github's action - workflow for testing on every push or pull request

_The file must be in the root of project (/github/workflows/django.yml)_  
The action is triggered on every push to master by checking if the code passes the tests  

### How to run

`docker-compose up`  
It starts all the services (django application, redis, celery)  

### Django container (app)

By typing `docker exec -it django_container /bin/bash`, the user can have access to the django container in order to do the following:  
  * Run tests  
`python manage.py test`
  * Create a superuser (needed in order to have access to the admin panel and for creating a manager)  
`python manage.py createsuperuser`  

### Usage

* Daily_job  
Using celery and redis as a message broker, the application has a task which fetches the csv data from the server every day at 06:00 UTC. This data is used to update the database with the cities and the hotels.  
  
* Search for a city  
The home page of the application is used to search for a city and shows all the cities and their hotels.  
  
* Admin panel (admin user needs to be created)  
The administrator page gives us access to all models (cities, hotels, users, managers) and we can make crud operations. 
  
* Manager interface (needs a staff user)  
A manager can have access to the manager interface and update only the hotels of his/her city. In order to have access we need to do the following:    

  * create a group _managers_  
  
  * create a user (staff status) and add him/her in managers group    
    
  * apply user crud permissions (add, change, delete, view)  

  * add the user to the managers table by choosing the city in which he/she belongs to  

  * the user can have access to the hotels via the _/managers/_ endpoint  
