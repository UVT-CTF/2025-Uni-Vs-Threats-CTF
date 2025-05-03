# 1. Base image
FROM php:8.2-apache

# 2. Install cron (and whois if you still need it)
RUN apt-get update \
 && apt-get install -y cron whois \
 && cp /usr/bin/whois /usr/local/bin/safewhois

# 3. Disable dangerous PHP functions
RUN echo "disable_functions = shell_exec, passthru, popen, proc_open, pcntl_exec, assert, eval" \
     > /usr/local/etc/php/conf.d/disable-functions.ini

# 4. Copy your web app into place
WORKDIR /var/www/html
COPY . /var/www/html/

# create uploads (if not already there) and hand it to www‑data
RUN mkdir -p /var/www/html/uploads \
 && chown -R www-data:www-data /var/www/html/uploads \
 && chmod 755 /var/www/html/uploads

# 6. Copy the cleanup script and make it executable
COPY cleanup_uploads.sh /usr/local/bin/cleanup_uploads.sh
RUN chmod +x /usr/local/bin/cleanup_uploads.sh

# 7. Copy the cron definition and install it
COPY cleanup.cron /etc/cron.d/cleanup
RUN chmod 0644 /etc/cron.d/cleanup \
 && crontab /etc/cron.d/cleanup

# 8. Copy a tiny entrypoint that starts cron + Apache
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 9. Expose HTTP and set entrypoint
EXPOSE 80
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
