#!/usr/bin/env bash

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" 40 &
python "bob.py" 40 &
python "eve.py" 40 &
