sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "alice.py" 10 &
python "bob.py" 10 &