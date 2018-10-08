FROM ubuntu:18.04

RUN useradd -ms /bin/bash focruser

WORKDIR /home/focruser/focr

COPY requirements.txt ./

RUN apt-get -y update && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
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
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove --purge -y  python3-pip python3-dev && \
    apt-get clean -y  && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

USER focruser

COPY --chown=focruser:focruser . .

CMD [ "python", "app.py" ]