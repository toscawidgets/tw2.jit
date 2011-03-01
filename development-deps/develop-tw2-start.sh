#!/bin/bash

devbase=development-deps
venv=$devbase/virtualenv-tw2.jit
source $venv/bin/activate
pip install formencode

pushd ../../tw2.devtools;hg pull;python setup.py develop;popd

python setup.py develop && paster tw2.browser



