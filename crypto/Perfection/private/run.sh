#!/bin/sh

gcc ./source.c -o ./perfection -lm
timeout --kill-after=1s 10m ./perfection