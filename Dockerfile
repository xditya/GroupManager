# We're using Alpine stable
FROM alpine:3.9

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python
RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base

# Set Python version
ARG PYTHON_VERSION='3.7.2'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv
# Note installing THROUGH THIS METHOD WILL DELAY DEPLOYING
# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash

# Cleaning pip cache
RUN rm -rf ~/.cache/pip
#
# Install all the required packages
#
RUN apk add --no-cache \
    py-pillow py-requests py-sqlalchemy py-psycopg2 git py-lxml \
    libxslt-dev py-pip libxml2 libxml2-dev libpq postgresql-dev \
    postgresql build-base linux-headers jpeg-dev \
    curl neofetch git sudo
RUN apk add --no-cache sqlite
RUN apk add figlet
# Copy Python Requirements to /app

RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser haruka --disabled-password --home /home/haruka
RUN adduser haruka wheel
USER haruka
WORKDIR /home/haruka/haruka
COPY ./requirements.txt /home/haruka/haruka
#
# Install requirements
#
RUN sudo pip3 install -U pip
RUN sudo pip3 install -r requirements.txt
#
# Copy bot files to /app
#
COPY . /home/haruka/haruka
RUN sudo chown -R haruka /home/haruka/haruka
RUN sudo chmod -R 777 /home/haruka/haruka
cmd ["python3","-m","tg_bot"]
