# Use official PHP image with Apache
FROM php:8.2-apache

RUN apt-get update && apt-get install -y whois

RUN cp /usr/bin/whois /usr/local/bin/safewhois

RUN echo "disable_functions = shell_exec, passthru, popen, proc_open, pcntl_exec, assert, eval" > /usr/local/etc/php/conf.d/disable-functions.ini

WORKDIR /var/www/html

COPY . /var/www/html/

RUN mkdir -p /var/www/html/uploads

RUN chown -R root:root /var/www/html && \
    chown www-data:www-data /var/www/html/uploads && \
    chmod -R 755 /var/www/html && \
    chmod 755 /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads

RUN mv flag.txt /flag.txt

EXPOSE 81

CMD ["apache2-foreground"]
