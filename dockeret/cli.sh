#!/bin/sh

export PYTHONPATH=/root/.config/mailsort/filters/
/usr/bin/timeout -t 300 -s KILL mailsort
