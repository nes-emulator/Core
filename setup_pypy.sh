#!/bin/bash
DIR="./pypyenv"
if [ ! -d "$DIR" ]; then
  rm -rf pypyenv pypy3.5-v7.0.0-linux64 pypy3.5-v7.0.0-linux64.tar.bz2
  sudo apt-get install python3-pip;sudo pip3 install virtualenv;wget https://bitbucket.org/pypy/pypy/downloads/pypy3.5-v7.0.0-linux64.tar.bz2
 tar xf pypy3.5-v7.0.0-linux64.tar.bz2; rm pypy3.5-v7.0.0-linux64.tar.bz2; virtualenv -p ./pypy3.5-v7.0.0-linux64/bin/pypy3 pypyenv
fi

source ./pypyenv/bin/activate
