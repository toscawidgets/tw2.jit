#!/bin/bash -e

devbase=development-deps
venv=$devbase/virtualenv-tw2.jit
$(
    rm -rf $venv
) || echo "Did not destroy $venv"

virtualenv $venv --no-site-packages

source $venv/bin/activate
pushd $devbase
hg clone http://bitbucket.org/paj/tw2core || echo "tw2core exists."
hg clone http://bitbucket.org/paj/tw2forms || echo "tw2forms exists."
hg clone http://bitbucket.org/ralphbean/tw2devtools || echo "tw2devtools exists."
hg clone http://bitbucket.org/toscawidgets/tw2jquery || echo "tw2jquery exists."
pushd tw2core;hg pull;python setup.py develop;popd
pushd tw2forms;hg pull;python setup.py develop;popd
pushd tw2devtools;hg pull;python setup.py develop;popd
pushd tw2jquery;hg pull;python setup.py develop;popd
popd

