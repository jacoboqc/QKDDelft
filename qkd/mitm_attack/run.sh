#!/usr/bin/env bash

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" 10 &
python "bob.py" 10 &
python "eve.py" 10 &
