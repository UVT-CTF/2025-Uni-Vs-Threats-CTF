FROM php:8.0-apache

# Install MySQL client (alternative package)
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install required PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Set the working directory
WORKDIR /var/www/html

# Copy application files into the container
COPY ./private/src /var/www/html/
COPY ./private/db /var/www/html/private/db/

# Expose port 80
EXPOSE 80
