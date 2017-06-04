# suneku labs

Each **suneku lab** is a [Docker container](https://docs.docker.com/engine/understanding-docker/) built from this [Dockerfile](https://github.com/samkennerly/suneku/blob/master/labs/latest/Dockerfile). It is a self-contained data science environment based on the [Anaconda](https://www.continuum.io/blog/developer-blog/anaconda-and-docker-better-together-reproducible-data-science) open-source platform.

## build a lab

On a Linux or Mac machine with Docker installed, the [run_suneku_lab](https://github.com/samkennerly/suneku/blob/master/labs/run_suneku_lab) script will automatically build a Docker image and run a Docker container. By default, the container will be named `suneku_lab`. To use another name, specify it when running `run_suneku_lab` like this:
```
~/suneku/labs/run_suneku_lab another_suneku_lab
```
The first time you run a lab, it will need time to download and build an image. (This takes roughly ~2GB of disk space.) Subsequent builds on the same machine will be much faster because Docker can re-use the existing image.


## stop and restart your suneku lab

When a lab misbehaves, try turning it off and on again. Enter these commands in a terminal:

- `docker start suneku_lab` starts a stopped lab.
- `docker stop suneku_lab` requests the lab to stop running.
- `docker kill suneku_lab` forces the lab to stop. (Try this if `docker stop` doesn't work.)
- `docker restart suneku_lab` stops and starts a lab which is already running.


## delete a suneku lab

To delete a lab, enter these commands in a terminal:
```
docker stop suneku_lab
docker rm suneku_lab
```

## avoid Docker inception limbo

Some rules of Docker data persistence:

- Stopping and restarting a container does not delete any files.
- Deleting a container deletes all the files in that container. (It does not affect your `~/suneku/` folder.)
- Deleting an image deletes all the containers which depend on that image.

It is possible to run a Docker container from inside a Docker container, but I dare not go there.


## Docker commands

Here are some useful commands for keeping track of your lab(s):

- `docker images` shows all images on your machine
- `docker ps` shows containers which are running on your machine
- `docker ps -a` shows all containers, including stopped ones
- `docker exec -it suneku_lab /bin/bash` opens an interactive terminal in a running lab
- `docker kill $(docker ps -q)` forces all running containers to stop
- `docker rm suneku_lab` deletes `my_suneku_lab`
- `docker rmi suneku_lab` deletes the image used to run suneku labs
- `docker rmi $(docker images -qf dangling=true)` deletes [dangling images which are wasting disk space](http://stackoverflow.com/questions/32723111/how-to-remove-old-and-unused-docker-images)

For more information, see the [official Docker tutorial](https://docs.docker.com/engine/getstarted/).
