FROM python:3.6.5
LABEL maintainer="samkennerly@gmail.com"

# Install Python packages.
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && \
    pip3 install --requirement /tmp/requirements.txt

# Run as user, not as root.
RUN useradd -m dev
USER dev
WORKDIR /home/dev

# Install the suneku package.
COPY --chown=dev . suneku
RUN pip3 install --user --editable suneku

CMD ["/bin/bash"]
