# Kaifeck Website
The website of the band Kaifeck. View at https://www.kaifeck.de

## Framework
This website was built with the [django framework](https://www.djangoproject.com/). 
The frontend is mainly based on the [Bootstrap Grayscale Template](https://github.com/BlackrockDigital/startbootstrap-grayscale).

## License
All source code is licensed under the MIT license (view [LICENSE](../master/LICENSE) file for details) and is free to use. 
This does **not** include images and vector graphics.

## Quick setup
```
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py runserver
```
You should now be able to view the website locally at [127.0.0.1:8000](http://127.0.0.1:8000).
To add videos and posts, log in with your superuser at [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin). \
To work with emails and YouTube API see corresponding bullet points in [Adjust Settings](#adjust-settings).

# Deployment
There's several things to do when deploying this project.

## Adjust Settings
In [settings.py](../master/kaifeck/settings.py):
  * Disable debug mode
    ```
    DEBUG = False
    ```
  * Create a new secret key
    ```
    $ python3
    >>> from django.core.management.utils import get_random_secret_key
    >>> get_random_secret_key()
    '<secret_key>'
    >>> exit()
    ```
    ```
    SECRET_KEY = '<secret_key>'
    ```
  * Set allowed hosts
    ```
    ALLOWED_HOSTS = ['www.example.com']
    ```
  * Change to another database format (e.g. mysql). Make sure the user has all privileges on the database.
    You will need to install the mysqlclient python package.
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': '<db_user>',
            'NAME': '<db_name>',
            'PASSWORD': '<db_user_password>',
        }
    }
    ```
  * Configure email backend
    ```
    EMAIL_HOST = 'smtp.example.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'user@example.com'
    EMAIL_HOST_PASSWORD = 'P4ssw0rd'
    EMAIL_SENDER = 'noreply@example.com'
    ```
  * Enter YouTube API key (to get one, watch this [video](https://www.youtube.com/watch?v=-QMg39gK624))
    ```
    YOUTUBE_API_KEY = '<api_key>'
    ```
    To get other uploads than those by [Kaifeck](https://www.youtube.com/channel/UCU5yJUgbF9E2LxDLS-voY4g) change the 
    channel_id in [website.admin.YouTubeAdmin.get_uploads](../master/website/admin.py#L40)
  * When using https (which is highly recommended), also add:
    ```
    SECURE_HSTS_SECONDS = 1
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'same-origin'
    ```
  * *(optional)* Change timezone
    ```
    TIME_ZONE = '<time_zone>'
    ```
  
### Check configuration
```
$ python3 manage.py check --deploy
```
If everything was done correctly, this should yield no issues.

## Configure HTTP Server
Example configuration for Apache:
```
WSGIPythonHome /var/www/www.example.com/.venv
WSGIPythonPath /var/www/www.example.com/

<Directory /var/www/www.example.com/kaifeck/>
        <Files wsgi.py>
                Require all granted
        </Files>
</Directory>

<Directory /var/www/www.example.com/assets/>
        Require all granted
</Directory>

<VirtualHost *:80>
        ServerAdmin admin@example.com
        DocumentRoot /var/www/www.example.com/
        ServerName www.example.com
        ErrorLog logs/www.example.com-error_log
        CustomLog logs/www.example.com-access_log common

        Alias "/static/" "/var/www/www.example.com/assets/"

        WSGIScriptAlias / /var/www/www.example.com/kaifeck/wsgi.py

        RewriteEngine on
        RewriteCond %{SERVER_NAME} =www.example.com
        RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
        ServerAdmin admin@example.com
        DocumentRoot /var/www/www.example.com/
        ServerName www.example.com
        ErrorLog logs/www.example.com-error_log
        CustomLog logs/www.example.com-access_log common

        Alias "/static/" "/var/www/www.example.com/assets/"

        WSGIScriptAlias / /var/www/www.example.com/kaifeck/wsgi.py

        Include /etc/letsencrypt/options-ssl-apache.conf
        SSLCertificateFile /etc/letsencrypt/live/www.example.com/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/www.example.com/privkey.pem
</VirtualHost>
</IfModule>
```

## Django management
```
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py collectstatic
```
