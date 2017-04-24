#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv

    if which pyenv > /dev/null; then
	eval "$(pyenv init -)"
    fi

    pyenv install 2.7.13
    pyenv virtualenv 2.7.13 conan
    pyenv rehash
    pyenv activate conan
fi

sudo apt-get update -qq
sudo apt-get install -qq libtool
pip install conan_package_tools ConfigParser
conan user