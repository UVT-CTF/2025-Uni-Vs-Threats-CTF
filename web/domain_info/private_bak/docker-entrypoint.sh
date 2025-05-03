#!/usr/bin/env bash
# start cron in the background
service cron start

# then hand off to the normal Apache entrypoint
exec docker-php-entrypoint apache2-foreground
