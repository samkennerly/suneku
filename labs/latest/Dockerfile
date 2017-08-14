FROM continuumio/anaconda3:4.4.0

MAINTAINER Sam Kennerly <samkennerly@gmail.com>

# Use apt-get to install general-purpose stuff
RUN apt-get update && apt-get install -y \
    vim gcc zip unzip

# Use pip to install extra Python stuff
RUN /opt/conda/bin/pip install --upgrade pip && /opt/conda/bin/pip install --quiet \
    awscli==1.11.133 \
    fuzzywuzzy==0.15.1 \
    jellyfish==0.5.6 \
    pyarrow==0.5.0.post2 \
    python-Levenshtein==0.12.0 \
    tweepy==3.5.0

# Tell Python where to look for custom imports
ENV PYTHONPATH=/suneku/

CMD ["/bin/bash"]