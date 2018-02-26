#!/bin/sh


# Restarts the script if it crashes
while true; do
	nohup python breaker.py >> nohup.out
done &
