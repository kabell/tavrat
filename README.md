TaVrat - Don't forget your owes

Requirements:

    - Python 3.x
    - Django == 1.8

Install:

    mkdir tavrat
    cd tavrat
    virtualenv -p /usr/bin/python3 tavratenv
    git clone https://github.com/kabell/tavrat.git
    source tavratenv/bin/activate
    pip3 install django==1.8
    cd tavrat
    python3 manage.py migrate

    !!! if it can't open database - set full path of database in settings.py

    apache:

Alias /tavrat/static /var/tavrat/tavrat/static
<Directory /var/tavrat/tavrat/static>
            Order allow,deny
            Require all granted
            Options +Indexes
            Allow from all
</Directory>

<Directory /var/tavrat/tavrat/tavrat>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
<Location /tavrat>
WSGIProcessGroup tavrat
</Location>

WSGIDaemonProcess tavrat user=nobody group=nobody threads=10 python-path=/var/tavrat/tavrat:/var/tavrat/tavratenv/lib/python3.3/site-packages
WSGIScriptAlias /tavrat /var/tavrat/tavrat/tavrat/wsgi.py



    Settings:

    settings.py
    views.py





