# suneku

*Suneku* builds and runs examples of Python
[data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/).  

## more science, less installing stuff

Python's many powerful
[scientific computing tools](https://www.scipy.org/about.html)
can easily trap scientists in
[dependency hell](https://en.wikipedia.org/wiki/Dependency_hell).
The huge number of (package,version) combinations can make sharing code difficult or impossible.

*Suneku* uses
[Docker Compose](https://docs.docker.com/compose/)
to run containers with all software pre-installed:

- the specific Python version used to develop *suneku*
- all Python packages in [requirements.txt](requirements.txt)
- any required system packages unrelated to Python
- [Jupyter](http://jupyter.org/) and its requirements

Containers are especially useful as 
[sandboxes](https://en.wikipedia.org/wiki/Sandbox_(software_development))
for experimentation. When a container malfunctions, it can be destroyed and rebuilt quickly without affecting other software on your machine.

## get suneku

1. Install
[Docker for Mac](https://docs.docker.com/docker-for-mac/install/) or
[Windows](https://docs.docker.com/docker-for-windows/install/) or
[Linux](https://docs.docker.com/install/#supported-platforms).
2. [Clone this repository](https://help.github.com/articles/cloning-a-repository/) to any folder on your machine.

*Suneku* never modifies
[anaconda](https://www.anaconda.com/what-is-anaconda/),
[pip](https://pypi.org/project/pip/),
[brew](https://brew.sh/),
[virtualenv](https://virtualenv.pypa.io/en/stable/),
nor any system Pythons.

## run containers

Open a terminal and `cd` to wherever you cloned this repository.

### test suneku
* `docker-compose up clock` starts an example
[service](https://docs.docker.com/compose/gettingstarted/#step-3-define-services-in-a-compose-file).
* `docker-compose run tests` tests code in the *suneku* package.

### run python
1. `docker-compose run python` opens a Python interpreter.
2. `import suneku` imports the *suneku* package.
3. `exit()` exits Python and stops the container.

### start jupyter
1. `docker-compose up jupyter` starts a Jupyter server.
2. Open a browser and enter `127.0.0.1:8888` in the address bar.
3. `CTRL-C` in the terminal exits Jupyter and stops the container.

See [config/README.md](config/README.md) for Jupyter configuration details.

### burn it all down and start over
1. `docker-compose down` gently stops and deletes *suneku* containers.
1. `docker/clean` deletes all containers and any Docker leftovers.
2. `docker/delete` deletes the `suneku:latest` Docker image.

## config folder

Secrets and configuration files go here. See
[config/README.md](config/README.md) for details.

## docker scripts

The [docker](docker) folder contains bash scripts which run Docker commands.   
See the comments in each script for details.

## example notebooks

The [examples](examples) folder 

## suneku package

This is an example Python package. To comply with
[PEP 423](https://www.python.org/dev/peps/pep-0423/#use-a-single-name),
it is also named *suneku*.

* The
[classifier](suneku/classifier.py) module uses
[scikit-learn](http://scikit-learn.org/) and
[pandas](https://pandas.pydata.org/) to build a
[probabilistic classifier](https://en.wikipedia.org/wiki/Probabilistic_classification).
* The
[plot](suneku/plot.py) module uses
[matplotlib](https://matplotlib.org/) and
[pandas](https://pandas.pydata.org/) to visualize data.
* The
[zero](suneku/zero.py)
module defines constants and functions for use by other modules.


## FAQ

### Is this like [virtualenv](https://virtualenv.pypa.io/en/stable/)?

*Docker Compose* and *virtualenv* are both commonly used to build isolated
[environments](https://en.wikipedia.org/wiki/Deployment_environment)
for developing and testing software. *Suneku* is intended as a bigger, blunter *virtualenv* which includes Python packages _and_ its own separate OS, system installs, users, and directories.

### Is this like [anaconda](https://www.anaconda.com/what-is-anaconda/)?

*Anaconda* normally installs itself separately from the system Python(s), but it is less isolated than a Docker container. It shares the same OS, system installs, users, and filesystem as the host machine. The Anaconda team also releases
[Docker images](https://hub.docker.com/r/continuumio/anaconda3/)
for running containers with Anaconda pre-installed.

### What does `pip install --user --editable` do?

### Can Docker run containers inside containers?

![*squints*](examples/data/squint.png)




