#!/bin/bash -e

venv=virtualenv-tw2.jit
$(
    rm -rf $venv
) || echo "Did not destroy $venv"

virtualenv $venv --no-site-packages

source $venv/bin/activate

hg clone http://bitbucket.org/paj/tw2core || echo "tw2core exists."
hg clone http://bitbucket.org/paj/tw2devtools || echo "tw2devtools exists."

pip install genshi

cd tw2core
python setup.py develop
cd -

cd tw2devtools
python setup.py develop
cd -
