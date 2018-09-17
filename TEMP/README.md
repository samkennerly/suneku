# start doing data science with suneku

Suneku is a complete environment for analyzing data using [Python 3](https://www.python.org/).  
Suneku "labs" are similar to the [data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/) used by [Kaggle](https://www.kaggle.com/).  
These labs are designed to be easily built, customized, rebuilt, and shared.

Suneku works best for data which fits comfortably in your computer's RAM.  
For larger datasets, I use [Databricks](https://databricks.com/) to run a [Spark cluster](http://spark.apache.org/).

Here are some things you can do with a suneku lab:
* [load, inspect, and clean a table](https://github.com/samkennerly/suneku/blob/master/practice/practice.ipynb)
* [make complicated plots quickly](https://github.com/samkennerly/suneku/blob/master/sunekutools/viz/viz.ipynb)
* [train a machine to classify flowers](https://github.com/samkennerly/suneku/blob/master/sunekutools/ml/logistic_classifier.ipynb)



## ingredients

A suneku lab is a [Docker container](https://www.docker.com/what-docker) which starts a [Jupyter](http://jupyter.org/) server. (If you've never used Jupyter, see below for a quick introduction.) Each lab comes pre-installed with many Python packages including:
* [pandas](http://pandas.pydata.org/) for loading, cleaning, and transforming tables
* [seaborn](http://seaborn.pydata.org/) for generating plots and figures
* [scikit-learn](http://scikit-learn.org/stable/) for training and testing machine-learning algorithms
* the complete [Anaconda 3](https://docs.continuum.io/anaconda/pkg-docs) package list
* the custom [sunekutools](https://github.com/samkennerly/suneku/tree/master/sunekutools) package


## build your own suneku lab

### Mac or Linux
1. Install [Docker for Mac](https://docs.docker.com/docker-for-mac/) or [Docker for Linux](https://docs.docker.com/engine/installation/linux/).
2. Use [git clone](https://help.github.com/articles/cloning-a-repository/) to clone this repository into your home folder.  This will create a `~/suneku/` folder.
3. Create a blank text file called `.env` in your `~/suneku/` folder.
4. Run the script [~/suneku/labs/run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab). This will build a lab and start a Jupyter server.
5. Open your favorite web browser and go to `0.0.0.0:8888`. You should see a Jupyter notebook.
6. Click on `/practice/` and open the `practice.ipynb` notebook to start doing data science.


### Windows

[Docker for Windows](https://docs.docker.com/docker-for-windows/) can build and run labs which can be shared with any Mac or Linux user. The only catch is: you may need to write your own setup script if [run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab) does not work.


## Jupyter notebooks

Jupyter notebooks are useful for "exploratory data analysis," which is a polite name for projects in which you don't know precisely what you're doing yet. I use them to inspect data for quality and formatting issues, quickly test hypotheses, and export human-readable reports. My typical workflow looks like this:

* Open a notebook.
* Import packages with Python `import` statements.
* Type some Python code in a cell.
* Hit Shift-Enter to run that cell and inspect the output.
* Oops, that's not actually what I meant to do. Edit my code and try again.
* Whenever I do something useful, I save the notebook and go to the next cell.

For more details, see this [Jupyter tutorial](http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb).

When I create a new notebook (let's call it `my_project.ipynb`), I often create a `my_project.py` file in the same folder. I view the notebook in a web browser and open `my_project.py` in a text editor side-by-side on one big screen. I keep most of my code in `my_project.py` and run `from my_project import *` in the first cell of my notebook. This reduces clutter in my notebooks so there's more space for text, plots, and results.

GitHub can automatically render Jupyter notebooks! If you upload a notebook to GitHub, anyone can view it in a web browser without installing software or running scripts.


## about your ~/suneku/ folder

For the most part, suneku labs avoid interacting with other files and programs on their host computer. Two big exceptions are: they connect to `0.0.0.0:8888` so the web browser can find the Jupyter server, and they link their own `/suneku/` folder to the host machine's `~/suneku/` folder.

**If you modify the `/suneku/` folder inside a suneku lab, your `~/suneku/` folder will be modified.** The `/suneku/` folder is not really "inside" a container; it is the host machine's `~/suneku/` folder [mounted as a data volume](https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-host-directory-as-a-data-volume).


### store environment variables in ~/suneku/.env

Any [environment variables](https://en.wikipedia.org/wiki/Environment_variable) declared in this file will be automatically loaded when you execute [run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab). It's OK to leave your `.env` file blank, but the file must exist.

I use my `.env` file to store login credentials. Suneku's [gitignore](https://git-scm.com/docs/gitignore) includes `.env`, so GitHub will not see, track, or upload the contents of your `.env` file.


### store data in ~/suneku/data

From inside a lab, this folder will appear as `/suneku/data/` without the `~`. The suneku `.gitignore` file tells Git not to track files in `/suneku/data/`. Keeping data here helps avoid clogging GitHub with large files.

Remember: GitHub will not track files in this folder, so you need another way to backup data. I use an [S3 bucket](https://aws.amazon.com/s3/) for backup and sharing, and all suneku labs come with [`awscli`](https://aws.amazon.com/cli/) pre-installed.


### store prototypes and untested code in ~/suneku/studies/

When I write code which is well-tested and intended to be re-used often, I usually save it to a subfolder of `~/suneku/sunekutools/`. To avoid clutter, other code usually goes in a subfolder of `~/suneku/studies/`. (Remember, you don't need the `~` from inside a lab.)

I also like to keep a nearly empty [scratch notebook](https://github.com/samkennerly/suneku/blob/master/studies/scratch.ipynb) in my `~/suneku/studies/` folder for easy access when I need to try something quickly.


## import sunekutools

This custom Python package comes pre-installed with every suneku lab. See the [sunekutools](https://github.com/samkennerly/suneku/tree/master/sunekutools) folder for details.


## maintaining and customizing your lab(s)

To add or remove packages, modify the [Dockerfile](https://github.com/samkennerly/suneku/blob/master/labs/latest/Dockerfile) and build a new lab. The [labs](https://github.com/samkennerly/suneku/tree/master/labs) folder contains a very brief intro to Docker and some common commands.
