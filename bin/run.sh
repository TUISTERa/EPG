#!/bin/bash

echo "Checking for dependancies"
python3 -c "import git" > /dev/null 2>&1

if [[ $? -gt 0 ]]
then
  echo "Some python dependancies were not found. Installing ..."
  pip3 install gitpython
else
  echo "Dependancies already installed!"
fi

python3 main.py
