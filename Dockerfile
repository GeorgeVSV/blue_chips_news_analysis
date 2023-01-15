# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# make app directory in container
WORKDIR /app

# copy requirements.txt to image
COPY requirements.txt requirements.txt

# install necessary dependencies & packages
RUN pip3 install -r requirements.txt

# add source code into the image
COPY . .

# define command for docker image execute inside container
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
