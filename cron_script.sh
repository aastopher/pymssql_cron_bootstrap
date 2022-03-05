#!/bin/bash

source $pwd/env/bin/activate
sudo python3 main.py log -v
deactivate
