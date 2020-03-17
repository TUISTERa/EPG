#!/bin/bash

echo "Checking for dependancies"
python3 -c "import git"

if [[ $? -gt 0 ]]
then
  echo "Installing python modules"
  pip3 install --upgrade gitpython
else
  echo "Dependancies already installed!"
fi

python3 run.py
