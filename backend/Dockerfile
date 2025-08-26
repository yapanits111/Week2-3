FROM php:8.2-apache

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Configure Apache to listen on port 8000
RUN echo "Listen 8000" > /etc/apache2/ports.conf
RUN sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8000>/' /etc/apache2/sites-available/000-default.conf

# Set working directory
WORKDIR /var/www/html

# Copy application code
COPY public/ ./

# Set permissions
RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html

# Configure Apache DocumentRoot and Directory
RUN sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html|' /etc/apache2/sites-available/000-default.conf

# Configure Apache Directory permissions
RUN echo "<Directory /var/www/html>\n\
    Options Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n\
<Directory /var/www/html/api>\n\
    Options Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>" >> /etc/apache2/apache2.conf

# Expose port
EXPOSE 8000

# Start Apache
CMD ["apache2-foreground"]
