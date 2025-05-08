# Use official PHP image with Apache
FROM php:8.2-apache

# Install whois
RUN apt-get update && apt-get install -y whois

# Copy binaries and setup
RUN cp /usr/bin/whois /usr/local/bin/safewhois

# Disable dangerous PHP functions
RUN echo "disable_functions = shell_exec, passthru, popen, proc_open, pcntl_exec, assert, eval" > /usr/local/etc/php/conf.d/disable-functions.ini

# Set working directory
WORKDIR /var/www/html

# Copy all challenge files
COPY . /var/www/html/

# Create uploads folder
RUN mkdir -p /var/www/html/uploads

# Secure permissions
RUN chown -R root:root /var/www/html && \
    chown www-data:www-data /var/www/html/uploads && \
    chmod -R 755 /var/www/html && \
    chmod 755 /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads

# Copy flag outside webroot (optional, for extra protection)
RUN mv flag.txt /flag.txt

# Expose HTTP
EXPOSE 81

# Start Apache
CMD ["apache2-foreground"]
