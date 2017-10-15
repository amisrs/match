#!/bin/sh

while true; do
	nohup python breaker.py >> nohup.out
done &
