# suneku

[Docker](https://www.docker.com/)
example: a Python
[package](https://docs.python.org/3/tutorial/modules.html#packages)
which builds its own
[Python](https://docs.docker.com/get-started/part2/#your-new-development-environment).

## bring your favorite Python everywhere

I want my code to have the Python it needs, even when it's deployed remotely.

![Everybody strap in.](snake.jpg)

*Suneku* uses
[Docker Compose](https://docs.docker.com/compose/)
to:

- build an
[image](https://docs.docker.com/get-started/#images-and-containers)
from instructions in its [Dockerfile](Dockerfile)
- download packages listed in
[requirements.txt](requirements.txt)
- run custom
[services](https://docs.docker.com/get-started/part3/)
defined in
[docker-compose.yaml](docker-compose.yaml)
- run its own
[Jupyter notebook server](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html)

*Suneku* installs software to a Docker image, not to the host machine.  
It never modifies
[anaconda](https://www.anaconda.com/what-is-anaconda/),
[pip](https://pypi.org/project/pip/),
[brew](https://brew.sh/),
[virtualenv](https://virtualenv.pypa.io/en/stable/),
nor your system Python(s).  

## quickstart

1. Install
[Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
or
[Windows](https://docs.docker.com/docker-for-windows/install/)
or
[Linux](https://docs.docker.com/install/#supported-platforms).
2. [Clone this repository](https://help.github.com/articles/cloning-a-repository/) to any folder on your machine.
3. Open a terminal and `cd` to that folder.
4. Enter `docker-compose run clock` to run an example service.

Docker will download everything it needs to build a `suneku:latest` image.  
Subsequent runs re-use this image and are much faster.

See the
[dockerbash](https://github.com/samkennerly/dockerbash)
repository for a short list of common Docker commands.

### run temporary services
* `docker-compose run python` starts an interactive Python session.
* `docker-compose run tests` runs all automated tests.

### start persistent services
* `docker-compose up clock` prints a timestamp every 1 second.
* `docker-compose up jupyter` starts a Jupyter server.

### terminate all services
1. Open a terminal and `cd` to wherever you cloned this repository.
2. `docker-compose down` stops and deletes all `suneku` containers.

### uninstall suneku
1. Delete the folder where you cloned the `suneku` repository.
2. Run `docker rmi suneku:latest` to delete the image.
3. Run `docker system prune` to delete any Docker leftovers.

## suneku package

The
[suneku](suneku)
folder is a Python package.  
To comply with
[PEP 423](https://www.python.org/dev/peps/pep-0423/#use-a-single-name),
it has the same name as this repository.  
The `suneku:latest` image includes it as an
[editable pip install](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).

See the
[examples](examples)
folder for notebooks demonstrating the package.  
Notebooks can be
[viewed in GitHub](https://help.github.com/articles/working-with-jupyter-notebook-files-on-github/)
without running Jupyter.

## jupyter server

1. Enter `docker-compose up jupyter` to ensure the server is running.  
2. Open a browser and enter `127.0.0.1:8888` in the address bar.  
3. If Jupyter demands a token, then copypaste it from the terminal.

The Jupyter server ignores requests from all other addresses.  
The address can be modified in
[docker-compose.yaml](docker-compose.yaml).

*Suneku* stores its IPython and Jupyter settings in the
[config](config) folder.  
To use your own settings,
[symlink](https://en.wikipedia.org/wiki/Symbolic_link)
to your `.ipython` and/or `.jupyter` folders:

```bash
ln -s config/.ipython /path/to/your/.ipython
ln -s config/.jupyter /path/to/your/.jupyter
```

## private folders

The [config](config) folder is for configuration files.  
The [data](data) folder is for datasets. 

Files here are not
[copied into images](.dockerignore)
nor
[uploaded to GitHub](.gitignore).  
Containers can access these folders only by
[mounting](https://docs.docker.com/storage/bind-mounts/)
them or their parents.  
The only exceptions are
[config/README.md](config/README.md)
and these example datasets:

- [data/NewYorkEnergy.csv](data/NewYorkEnergy.csv)
from
[data.ny.gov](https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu)  
GWh of electricity generated in New York since 1980.
- [ZonalTempAnomaly.csv](data/ZonalTempAnomaly.csv)
from [data.giss.nasa.gov](https://data.giss.nasa.gov/gistemp/)  
Global surface temperature anomalies since 1880.
