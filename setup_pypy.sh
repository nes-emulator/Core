#!/bin/bash
DIR="./pypyenv"
if [ ! -d "$DIR" ]; then
 rm -rf pypyenv pypy3.5-v7.0.0-linux64 pypy3.5-v7.0.0-linux64.tar.bz2
 sudo apt-get install python3-pip;sudo pip3 install virtualenv;wget https://bitbucket.org/pypy/pypy/downloads/pypy3.5-v7.0.0-linux64.tar.bz2
 tar xf pypy3.5-v7.0.0-linux64.tar.bz2; rm pypy3.5-v7.0.0-linux64.tar.bz2; virtualenv -p ./pypy3.5-v7.0.0-linux64/bin/pypy3 pypyenv;
 source ./pypyenv/bin/activate; sudo apt-get build-dep python3-pygame; sudo apt-get install python-dev;sudo apt install libsdl1.2-dev ;
 sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev;
 pypyenv/bin/pypy3 -m pip install pygame;
 source ./pypyenv/bin/activate;
 sudo apt-get install python3-setuptools;
fi

source ./pypyenv/bin/activate
