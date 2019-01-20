#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" 20 &
python "eve.py" 20 &
python "bob.py" 20 &
