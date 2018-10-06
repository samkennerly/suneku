# suneku

*Suneku* builds and runs examples of Python
[data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/).  

## more science, less installing stuff

The
[SciPy ecosystem](https://www.scipy.org/about.html)
and a huge variety of
[topical software](https://www.scipy.org/topical-software.html)
have made Python into a powerful scientific computing toolbox,
but it can easily become a highway to [dependency hell](https://en.wikipedia.org/wiki/Dependency_hell).

*Suneku* uses
[Docker Compose](https://docs.docker.com/compose/)
to run containers with pre-installed software. *Docker* and this repository are the only dependencies. *Suneku* downloads everything else it needs:

- the specific Python version used to develop *suneku*
- all Python packages in [requirements.txt](requirements.txt)
- any required system packages unrelated to Python
- [Jupyter](http://jupyter.org/) and its requirements

Installed software is saved to a
[Docker image](https://docs.docker.com/get-started/#images-and-containers)
and re-used on subsequent builds. When a container malfunctions, it can be destroyed and rebuilt quickly without affecting other software on your machine. This makes containers especially useful as 
[sandboxes](https://en.wikipedia.org/wiki/Sandbox_(software_development)). 

Dependencies are specified in a few human-readable files:  

* [Dockerfile](Dockerfile)
tells Docker how to build a `suneku` image.
* [requirements.txt](requirements.txt)
tells
[pip](https://pypi.org/project/pip/)
what Python packages to install inside the image.
* [docker-compose.yaml](docker-compose.yaml)
tells Docker Compose how to run pre-defined
[services](https://docs.docker.com/compose/gettingstarted/#step-3-define-services-in-a-compose-file).

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
* `docker-compose up clock` starts an example service.
* `docker-compose run tests` tests code in the [suneku](suneku) package.

### run python
1. `docker-compose run python` opens a Python interpreter.
2. `import suneku` imports the [suneku](suneku) package.
3. `exit()` exits Python and stops the container.

### start jupyter
1. `docker-compose up jupyter` starts a Jupyter server.
2. Open a browser and enter `127.0.0.1:8888` in the address bar.
3. `CTRL-C` in the terminal exits Jupyter and stops the container.

See
[config/README.md](config/README.md)
for Jupyter configuration details.

### burn it all down and start over
1. `docker-compose down` gently stops and deletes *suneku* containers.
1. `docker/clean` deletes all containers and any Docker leftovers.
2. `docker/delete` deletes the `suneku:latest` Docker image.

## config folder

Secrets and configuration files go here. See
[config/README.md](config/README.md)
for details.

## docker scripts

The
[docker](docker)
folder contains bash scripts which run Docker commands.   

## example notebooks

The
[examples](examples)
folder contains
[Jupyter notebooks](http://jupyter.org/)
demonstrating the
[suneku](suneku) package.

### data sources

* [NewYorkEnergy.csv](examples/data/NewYorkEnergy.csv)
from
[data.ny.gov](https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu)  
GWh of electricity generated in New York since 1980.
* [ZonalTempAnomaly.csv](examples/data/ZonalTempAnomaly.csv)
from [data.giss.nasa.gov](https://data.giss.nasa.gov/gistemp/)  
Global surface temperature anomalies since 1880.

## suneku package

The
[suneku](suneku)
folder is an example Python package.  
To comply with
[PEP 423](https://www.python.org/dev/peps/pep-0423/#use-a-single-name),
it is also named *suneku*.

### modules
* [suneku.classifier](suneku/classifier.py):
[Probabilistic classification](https://en.wikipedia.org/wiki/Probabilistic_classification)
using
[scikit-learn](http://scikit-learn.org/)
and
[pandas](https://pandas.pydata.org/).
* [suneku.plot](suneku/plot.py):
Data visualization using
[matplotlib](https://matplotlib.org/) and
[pandas](https://pandas.pydata.org/).
* [suneku.zero](suneku/zero.py):
Constants and functions shared by other modules.




## FAQ

### Is this like [virtualenv](https://virtualenv.pypa.io/en/stable/)?

Suneku and virtualenv both keep their Python packages isolated from other Pythons on the same machine. Suneku also has its own isolated OS, system installs, users, and directories.

### Is this like [anaconda](https://www.anaconda.com/what-is-anaconda/)?

Anaconda is separate from the system Python(s), but it shares the same OS, system installs, users, and filesystem. Docker containers are more isolated from the host machine. For those who want both, the Anaconda team releases
[Docker images with Anaconda pre-installed]
(https://hub.docker.com/r/continuumio/anaconda3/).

### What does `pip install --user --editable` do?

Code in the
[suneku](suneku)
folder is installed as an
[editable Python package](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
to ensure the Python interpreter can import it without relying on
[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)
or modifying
[sys.path](https://docs.python.org/3/library/sys.html#sys.path).

### Can Docker run containers inside containers?

![*squints*](examples/data/squint.png)




