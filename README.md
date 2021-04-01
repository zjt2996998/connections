# connections demo

A demo app showing a simple service using flask and some supporting packages

### Requirements

 * Docker CE >= 17.04

### Stack Information

* python flask
* pipenv (for package management rather than virtualenv capabilities)
* mysql
* nginx + gunicorn

**All API calls will go through nginx at http://localhost:5000. All the other services are handled within Docker's internal network and no other ports are exposed to the host machine.**

### Instructions

- Build and kick off all the services with tilt.

```
tilt up
```

You can use ```docker ps``` command to see the running containers. You should see 2 running containers. ** Don't forget to run the migrations provided in the next section.**

MySQL database creates its own volume claim that provides persistence in the case of rebuilding/restarting/stopping the containers. Those volumes are managed by Docker and not directly exposed to the developer.

