#!/usr/bin/env sh
TEST_PIDS=$(ps aux | grep python | grep -E "BB84" | awk {'print $2'})
if [ "$TEST_PIDS" != "" ]
then
        kill -9 $TEST_PIDS
fi

sh $NETSIM/run/startAll.sh -nd "Alice Bob Eve"

python "aliceBB84_mitm.py" &
python "eveBB84_mitm.py" &
python "bobBB84_mitm.py" &
