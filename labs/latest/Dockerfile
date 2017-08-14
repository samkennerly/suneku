FROM continuumio/anaconda3:4.4.0

MAINTAINER Sam Kennerly <samkennerly@gmail.com>

# Install general things with apt-get
RUN apt-get update && apt-get install -y \
    vim gcc zip unzip

# Install more Python stuff with pip
RUN /opt/conda/bin/pip install --upgrade pip && /opt/conda/bin/pip install --quiet \
    awscli==1.11.133 \
    fuzzywuzzy==0.15.1 \
    jellyfish==0.5.6 \
    python-Levenshtein==0.12.0 \
    tweepy==3.5.0

# Tell Python where to look for custom imports
ENV PYTHONPATH=/suneku/

ENTRYPOINT ["/bin/bash"]