FROM python:3.6.5
LABEL maintainer="samkennerly@gmail.com"

# Install Python packages.
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && \
    pip3 install --requirement /tmp/requirements.txt

# Run as user, not as root.
RUN useradd -m suneku
USER suneku
WORKDIR /home/suneku

# Create a folder for user data.
RUN mkdir data && chown suneku:suneku data

# Install the Python package.
COPY --chown=suneku . code
RUN pip3 install --user --editable code

CMD ["python"]
