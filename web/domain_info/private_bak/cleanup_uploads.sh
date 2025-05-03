#!/usr/bin/env bash
# delete any file in uploads older than 2 minutes
find /var/www/html/uploads -type f -mmin +2 -print -delete
