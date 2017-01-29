FROM continuumio/anaconda3:4.2.0

MAINTAINER Sam Kennerly <samkennerly@gmail.com>

# Install general things with apt-get
RUN apt-get update && apt-get install -y \
    vim \
    gcc

# Install core Python stuff with conda
RUN /opt/conda/bin/conda install --yes \
    pyqt=4.11 \
    jupyter=1.0.0 \
    pymysql=0.7.9 \
    seaborn=0.7.1

# Install more Python stuff with pip
RUN /opt/conda/bin/pip install --upgrade pip && /opt/conda/bin/pip install --quiet \
    awscli==1.11.11 \
    openpyxl==2.4.1 \
    python-Levenshtein==0.12.0 \
    fuzzywuzzy==0.14.0 \
    jellyfish==0.5.6 \
    unidecode==0.4.19

# Tell Python where to find the sunekutools package
ENV PYTHONPATH=/suneku/

# Start Jupyter unless another command is specified
CMD ["jupyter","notebook","--ip=0.0.0.0","--no-browser"]

