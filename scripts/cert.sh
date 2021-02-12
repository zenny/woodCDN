#!/bin/bash
cd /opt/woodCDN/cron

if [[ "`pidof -x $(basename $0) -o %PPID`" ]]; then
  echo "This script is already running with PID `pidof -x $(basename $0) -o %PPID`"
else
  /usr/bin/python3 cert.py
fi
