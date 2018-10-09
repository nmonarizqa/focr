FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN useradd -ms /bin/bash focruser

RUN apt-get -y update && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
      git \
      curl \
      python3 \
      python3-dev \
      python3-pip \
      python3-setuptools \
      python3-pyproj \
      python3-psutil \
      python3-tk \
      software-properties-common && \
    add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    apt-get -y update && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
      libgdal20 \
      python3-gdal && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    git clone https://github.com/Mohitsharma44/focr /home/focruser/focr && \
    cd /home/focruser/focr && git checkout uo-web && \
    pip install --no-cache-dir -r requirements.txt && chown -R focruser:focruser . && \
    apt-get remove --purge -y  python3-pip python3-dev && \
    apt-get clean -y  && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
    
#RUN git	clone https://github.com/Mohitsharma44/focr && \
#    cd focr && git checkout uo-web && \
#    pip install --no-cache-dir -r requirements.txt && chown -R focruser:focruser . && \
#    apt-get remove --purge -y  python3-pip python3-dev && \
#    apt-get clean -y  && \
#    apt-get autoremove -y && \
#    rm -rf /var/lib/apt/lists/*

USER focruser

WORKDIR /home/focruser/focr

HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

CMD [ "python", "app.py" ]