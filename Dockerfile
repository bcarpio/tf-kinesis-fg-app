############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Brian Carpio

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

ADD /app/ /app

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Expose ports
EXPOSE 8080

# Set the default directory where CMD will execute
WORKDIR /app

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python server.py
