#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
	eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    export CC="$C_COMPILER"
else
    export CC="clang"
fi

cd build
conan install . --build missing
conan upload apache-apr/1.6.0@pbtrung/stable --all -r=conan.io