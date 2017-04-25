#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
	eval "$(pyenv init -)"
    fi
    pyenv activate conan
    python build.py
else
    export CC="$C_COMPILER"
    conan user pbtrung -p $CONAN_PASSWORD
    cd build
    conan install . --build missing
    conan upload apache-apr/1.6.0@pbtrung/stable --all -r=conan.io
    cd ..
    conan test_package
fi