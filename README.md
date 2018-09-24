# suneku

[data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/)

farewell to [dependency hell](https://en.wikipedia.org/wiki/Dependency_hell)


## more science, less installing stuff


1. Install
[Docker for Mac](https://docs.docker.com/docker-for-mac/install/) or
[Windows](https://docs.docker.com/docker-for-windows/install/) or
[Linux](https://docs.docker.com/install/#supported-platforms).
2. [Clone this repository](https://help.github.com/articles/cloning-a-repository/) to any folder on your machine.
3. Open a terminal and `cd` to this repository.

Installing and running *suneku* **does not alter any other Python installations.**  
It does not touch
[pip](https://pypi.org/project/pip/),
[homebrew](https://brew.sh/),
[virtualenv](https://virtualenv.pypa.io/en/stable/),
nor your system Python.  
Docker prefers not to know what you've done with those other programs.

## data science containers

Everything in
[requirements.txt](requirements.txt) is pre-installed in every *suneku* container.

### run python

1. `docker-compose run python` opens a Python interpreter.
2. `import suneku` imports the *suneku* package.
3. `exit()` exits Python and stops the container.

### start jupyter

1. `docker-compose up jupyter` starts a Jupyter server.
2. Open a browser. Jupyter is at `127.0.0.1:8888`.
3. `CTRL-C` in the terminal exits Jupyter and stops the container.

### nuke the entire site for orbit

1. `docker-compose down` gently stops containers and cleans up after itself.
1. `docker/clean` rudely deletes all containers and any Docker leftovers.
2. `docker/delete` deletes the `suneku:latest` Docker image.

## jupyter setup

## docker basics

## table of contents

### suneku repository

| folder | contents |
| ------ | -------- |
| [bin](bin) | executable Python scripts |
| [config](config) | credentials, configuration, etc |
| [docker](docker) | scripts which run Docker commands |
| [examples](examples) | *suneku* examples in Jupyter notebooks  |
| [suneku](suneku) | Python package |
| [tests](tests) | automated tests |

### suneku package

| module | description |
| ------ | ----------- |
| [classifier](suneku/classifier.py) | |
| [plot](suneku/plot.py) | |
| [zero](suneku/zero.py) | |

## FAQ

### What is a dev environment?

### Is this like [virtualenv](https://virtualenv.pypa.io/en/stable/)?

### What does `pip install --user --editable` do?

### Can Docker run containers inside containers?

![*squints*](examples/data/squint.png)




