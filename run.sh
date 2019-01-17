#!/usr/bin/env bash
ps aux | grep python | grep SimulaQron | awk {'print $2'} | xargs kill -9

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" 10 &
python "eve.py" 10 &
python "bob.py" 10 &
