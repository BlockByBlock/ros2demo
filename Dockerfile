FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    sudo git mercurial lsb-release wget cmake build-essential -y
