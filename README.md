# UNDER CONSTRUCTION #
this repo is not ready for public use yet!

# suneku data science toolkit

Suneku is a complete environment for inspecting, visualizing, and analyzing data.  
It is similar to the [data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/) used by [Kaggle](https://www.kaggle.com/), but smaller and simpler.  
I use a modified version of suneku for small- and medium-sized data projects at [Conductor](https://www.conductor.com/).

## ingredients

Each suneku lab is a [Docker container](https://www.docker.com/what-docker) which starts a [Jupyter](http://jupyter.org/) server.  
Jupyter notebooks can be used to run [Python 3](https://www.python.org/) interactively and produce human-readable reports.  
Click on the [practice notebook](https://github.com/samkennerly/suneku/blob/master/practice/practice.ipynb) for an example.

Each lab comes pre-installed with Python packages for data science, including
* [pandas](http://pandas.pydata.org/) for manipulating tables and doing math
* [seaborn](http://seaborn.pydata.org/) for quickly generating plots and figures
* [scikit-learn](http://scikit-learn.org/stable/) machine-learning packages
* the complete [Anaconda 3](https://docs.continuum.io/anaconda/pkg-docs) package list
* a custom [sunekutools](https://github.com/samkennerly/suneku/tree/master/sunekutools) package

It's easy to add packages by modifying the suneku [Dockerfile](https://github.com/samkennerly/suneku/blob/master/labs/latest/Dockerfile) and rebuilding your lab. (See below for details.)


## build your own suneku lab

### Mac or Linux
1. Install [Docker for Mac](https://docs.docker.com/docker-for-mac/) or [Docker for Linux](https://docs.docker.com/engine/installation/linux/).
2. Use [git clone](https://help.github.com/articles/cloning-a-repository/) to clone this repository into your home folder.  This will create a `~/suneku/` folder.
3. Use the script [~/suneku/labs/run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab) to build a lab and start a Jupyter server.
4. Open your favorite web browser and enter `0.0.0.0:8888`. You should see a Jupyter notebook.
5. Click on `/practice/` and open the `practice.ipynb` notebook to start doing data science.

## Windows
You can use `suneku` on a Windows machine, but you'll need to know enough about Docker to write your own setup script. Look at [run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab) to see what I did.


* notebooks for exploring data interactively


*  for 
* [Anaconda](https://www.continuum.io/downloads) for installing and managing packages

## using Jupyter notebooks

## save data in /suneku/data

## import `sunekutools`

## customize your suneku lab
