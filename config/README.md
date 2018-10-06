# config

This folder is excluded by the
[.dockerignore](../.dockerignore) and
[.gitignore](../.gitignore) files.  
This README is the only exception. All other files are:
 
- **not** baked into Docker images
- **not** uploaded to GitHub
- available inside a container **only if** they are
[mounted](https://docs.docker.com/storage/bind-mounts/)

### `.ipython` and `.jupyter` folders

*Suneku* stores IPython and Jupyter configuration files in this folder.  
To use your existing configuration files,
[symlink](https://en.wikipedia.org/wiki/Symbolic_link)
to them from here:

```bash
ln -s config/.ipython /path/to/your/.ipython
ln -s config/.jupyter /path/to/your/.jupyter
```



