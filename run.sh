#!/usr/bin/env bash
<<<<<<< HEAD
# sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "alice.py" 10 &
# python "eve.py" 5 &
=======
ps aux | grep python | grep SimulaQron | awk {'print $2'} | xargs kill -9

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "alice.py" 10 &
python "eve.py" 10 &
>>>>>>> 4047e1ac3af054deddb819cbf88769ae1d6967a9
python "bob.py" 10 &
