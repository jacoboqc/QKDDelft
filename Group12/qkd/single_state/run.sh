#!/usr/bin/env bash

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" &
python "bob.py" &
python "eve.py" &
