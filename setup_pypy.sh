#!/bin/bash
DIR="./pypyenv"
if [ ! -d "$DIR" ]; then
 #pypy
 rm -rf pypyenv pypy3.6-v7.2.0-linux64 pypy3.6-v7.2.0-linux64.tar.bz2
 sudo apt-get install python3-pip;sudo pip3 install virtualenv;wget https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.2.0-linux64.tar.bz2
 tar xf pypy3.6-v7.2.0-linux64.tar.bz2; rm pypy3.6-v7.2.0-linux64.tar.bz2; virtualenv -p ./pypy3.6-v7.2.0-linux64/bin/pypy3 pypyenv;
 source ./pypyenv/bin/activate; sudo apt-get build-dep python3-pygame; sudo apt-get install python-dev;sudo apt install libsdl1.2-dev ;
 sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev;
 source ./pypyenv/bin/activate;

 #pygame
 sudo apt-get install git python3-dev python3-setuptools python3-numpy python3-opengl \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
    libtiff5-dev libx11-6 libx11-dev fluid-soundfont-gm timgm6mb-soundfont \
    xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf libfreetype6-dev

  sudo apt-get update;
  sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-setuptools python3-dev python3 libportmidi-dev;
  sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 python3 libportmidi0;
  git clone https://github.com/pygame/pygame.git;

    # Grab source
  git clone git@github.com:pygame/pygame.git

  # Finally build and install
  cd pygame
  python3 setup.py build
  sudo python3 setup.py install
  #.bashrc config PYTHONPATH="${PYTHONPATH}:pypypath/site-packages/"
  #python3 setup.py install --prefix="pypypath"

export PYTHONPATH
fi

source ./pypyenv/bin/activate
