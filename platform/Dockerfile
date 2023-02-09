FROM ubuntu:22.04

# Attach to the repository
LABEL org.opencontainers.image.source https://github.com/Panduza/panduza-py

# Argument
ARG PZA_PY_PLATFORM_MODE

# Install Packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Paris \
    apt-get -y install \
        python3 python3-pip \
        git

# Append udev for device autodetection
RUN apt-get -y install udev

# Pip installations
RUN pip3 install pyudev
RUN pip3 install loguru
RUN pip3 install pyserial
RUN pip3 install paho-mqtt
RUN pip3 install python-magic
RUN pip3 install pymodbus==3.1.2
RUN pip install coloredlogs

# Repos clone
RUN echo $PZA_PY_PLATFORM_MODE

# Create the mirror directory
RUN mkdir /etc/panduza

#
WORKDIR /setup
COPY . /setup/
RUN pip install .
RUN cp -v ./deploy/pza-py-platform-run.py /usr/local/bin/pza-py-platform-run.py

# Allow plugin insertion here
ENV PYTHONPATH="/etc/panduza/plugins/py"

#
WORKDIR /work

# Create the directory for platform plugins
# Then run the platform
CMD mkdir -p /etc/panduza/plugins/py; \
    python3 /usr/local/bin/pza-py-platform-run.py
        
