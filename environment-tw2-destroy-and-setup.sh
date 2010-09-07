#!/bin/bash

venv=virtualenv-tw2.jit
$venv/bin/deactivate
rm -rf $venv

virtualenv $venv --no-site-packages

source $venv/bin/activate

hg clone http://bitbucket.org/paj/tw2core
hg clone http://bitbucket.org/paj/tw2devtools

pip install genshi

cd tw2core
python setup.py develop
cd -

cd tw2devtools
python setup.py develop
cd -
