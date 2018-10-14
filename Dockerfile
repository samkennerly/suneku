FROM python:3.6.5
LABEL maintainer="samkennerly@gmail.com"

# Install Python packages.
COPY requirements.txt /tmp
RUN pip install --upgrade pip && \
    pip install --requirement /tmp/requirements.txt

# Run as user, not as root.
RUN useradd -u 1000 -m 1000
USER 1000
WORKDIR /home/1000

# Copy repository files into image.
COPY --chown=1000 . suneku

# Install the suneku package.
RUN pip install --user --editable suneku

CMD ["/bin/bash"]
