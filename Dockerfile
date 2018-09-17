FROM python:3.6.5
LABEL maintainer="samkennerly@gmail.com"

# Install Python packages.
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && \
    pip3 install --requirement /tmp/requirements.txt

# Run as user, not as root.
RUN useradd -m kingofsnake
USER kingofsnake
WORKDIR /home/kingofsnake

# Copy local files into container.
COPY --chown=kingofsnake . suneku

# Install local code as an editable package.
RUN pip3 install --user --editable suneku

CMD ["/bin/bash"]
