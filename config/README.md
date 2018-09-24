# config

Secrets and host-specific configuration files go here. Files in this folder are:

- **not** baked into Docker images.
- **not** uploaded to GitHub.
- available inside a container **only if** they are
[mounted](https://docs.docker.com/storage/bind-mounts/).
  
Everything but this README file is excluded by
[.dockerignore](../.dockerignore) and
[.gitignore](../.gitignore) files.




