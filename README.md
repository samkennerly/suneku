# start doing data science with suneku

Suneku is a complete environment for inspecting, visualizing, and analyzing data using [Python 3](https://www.python.org/).  
It has much in common with the [data science containers](http://blog.kaggle.com/2016/02/05/how-to-get-started-with-data-science-in-containers/) used by [Kaggle](https://www.kaggle.com/).  
It is designed to provide a standardized, professional data science toolkit quickly and easily.

Suneku is designed for manipulating datasets which can comfortably fit in your computer's RAM.  
It is a simplified, open-source version of the setup I use for small-data projects at [Conductor](https://www.conductor.com/).  
For larger datasets, I suggest using [Databricks](https://databricks.com/) or building your own [Spark cluster](http://spark.apache.org/).


## ingredients

Each suneku lab is a [Docker container](https://www.docker.com/what-docker) which starts a [Jupyter](http://jupyter.org/) server.  
Jupyter notebooks can be used to run Python interactively and produce human-readable reports.  
See [`practice/practice.ipynb`](https://github.com/samkennerly/suneku/blob/master/practice/practice.ipynb) for an example.

Each lab comes pre-installed with popular Python packages including:
* [pandas](http://pandas.pydata.org/) for loading, cleaning, and transforming tables
* [seaborn](http://seaborn.pydata.org/) for quickly generating plots and figures
* [scikit-learn](http://scikit-learn.org/stable/) for training and testing machine-learning algorithms
* the complete [Anaconda 3](https://docs.continuum.io/anaconda/pkg-docs) package list
* the [sunekutools](https://github.com/samkennerly/suneku/tree/master/sunekutools) package of convenience functions and classes


## build your own suneku lab

### Mac or Linux
1. Install [Docker for Mac](https://docs.docker.com/docker-for-mac/) or [Docker for Linux](https://docs.docker.com/engine/installation/linux/).
2. Use [git clone](https://help.github.com/articles/cloning-a-repository/) to clone this repository into your home folder.  This will create a `~/suneku/` folder.
3. Run the script [~/suneku/labs/run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab) to build a lab and start a Jupyter server.
4. Open your favorite web browser and go to `0.0.0.0:8888`. You should see a Jupyter notebook.
5. Click on `/practice/` and open the `practice.ipynb` notebook to start doing data science.

### Windows
You can use suneku on a Windows machine with [Docker for Windows](https://docs.docker.com/docker-for-windows/), but you'll need to know enough about Docker to write your own setup script instead of using [run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab).


## Jupyter notebooks

Jupyter notebooks are useful for the early stages of a study when you don't know what you're doing yet. I use them to inspect data for quality and formatting issues, quickly try untested ideas, and export summaries of projects. My basic Jupyter workflow typcally works like this:

* Open a notebook
* Import packages (or your own custom modules) with Python `import` statements
* Type some Python code in a cell
* Hit Shift-Enter to run that cell and inspect the output
* If the result isn't what you wanted, then edit your code and try again
* When you're reasonably sure that you did something useful, save and go to the next cell

For more details, see this [Jupyter tutorial](http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb).

Whenever I create a notebook (let's call it `my_project.ipynb`), I usually create a `my_project.py` file in the same folder as my notebook. I open the notebook in Jupyter and `my_project.py` in a text editor. I keep most function definitions, global variables, custom classes, and `import` statements in `my_project.py` file. I then import all that stuff into my notebook with `from my_project import *` in the first cell.

GitHub can automatically render Jupyter notebooks! If you upload a notebook to GitHub, anyone can view it in a web browser without installing any software or running any scripts. 


## store your science in your ~/suneku/ folder

For the most part, Docker containers do not interact with the rest of your computer. Suneku labs make two exceptions: they connect to `0.0.0.0:8888` on the host machine so you can use Jupyter, and they link their own `/suneku/` folder to the host machine's `~/suneku/` folder.

**If you modify the `/suneku/` folder inside a suneku lab, your computer's `~/suneku/` folder will also be modified.** The `/suneku/` folder is not really "inside" a Docker container. It is your `~/suneku/` folder [mounted as a data volume](https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-host-directory-as-a-data-volume).

**Always store data in `~/suneku/data/`.** From inside your lab, this folder will appear as `/suneku/data/` without the `~`. The suneku repo contains a `.gitignore` file which tells Git not to track files in `/suneku/data/`. Keeping data in `~/suneku/data/` helps avoid accidentally uploading large files to GitHub.

Remember: GitHub will not upload files from your `~/suneku/data/` folder, so you'll need to find another way to backup data. I use an [S3 bucket](https://aws.amazon.com/s3/) for backup and sharing, and all suneku labs come with [`awscli`](https://aws.amazon.com/cli/) pre-installed.


## import sunekutools

See the [sunekutools](https://github.com/samkennerly/suneku/tree/master/sunekutools) folder for a description of this package.


## maintaining and customizing your lab(s)

If you've built and tested one suneku lab, building another is quick and easy. To add or remove packages, modify the [Dockerfile](https://github.com/samkennerly/suneku/blob/master/labs/latest/Dockerfile) and build a new lab. The [labs](https://github.com/samkennerly/suneku/tree/master/labs) folder contains an introduction to Docker and some common commands.
