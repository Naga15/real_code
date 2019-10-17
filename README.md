# Python Django-Web-Application

Steps to run locally

1. git clone https://github.com/mkdesai/Chassis-History-Web-Application.git

2. Install virtualenv package

> sudo pip install virtualenv

3. Now lets create a custom Virtual Environment and install all the requirements inside it.

> virtualenv my_project_venv

Note: If you are having problems because of python version conflict (which you will if you are using python 3 like me) then use:-

> virtualenv -p python3 my_project_venv

Activate Virtual Environment

> source my_project_venv/bin/activate

Install all the requirements inside my_project_venv

> pip install -r my_project/requirements.txt

4. Make sure your desired port is enabled on your instance and you don’t have any firewall enabled on that port. Now lets run our project by :-

> python my_project/manage.py runserver 0.0.0.0:8000

5. Visit your localhost and verify your running project

> http://127.0.0.1:8000/


```
<VirtualHost *:80>
ServerAdmin webmaster@example.com
DocumentRoot /home/ubuntu/chassis
ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

Alias /static /home/ubuntu/chassis/staticfiles
<Directory /home/ubuntu/chassis/staticfiles>
Require all granted
</Directory>

<Directory /home/ubuntu/chassis/project>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
WSGIDaemonProcess chassis python-path=/home/ubuntu/chassis python-home=/home/ubuntu/chassis/my_project_venv
WSGIProcessGroup chassis
WSGIScriptAlias / /home/ubuntu/chassis/project/wsgi.py
</VirtualHost>
```


commands for running on server

```
   git clone https://github.com/mkdesai/Chassis-History-Web-Application.git
   mv Chassis-History-Web-Application/ chassis
   cd chassis/
   virtualenv -p python3 my_project_venv
   source my_project_venv/bin/activate
   pip3 install -r requirements.txt
   pip3 install pdfkit
   sudo chown www-data:www-data db.sqlite3
   python manage.py runserver 172.31.87.159:8000
   sudo chown www-data:www-data db.sqlite3
   python3 manage.py  makemigrations
   sudo systemctl restart apache2
   
   
   Here is the feedback summary for the Chassis History Web App:
1.	Change Paccar Solutions logo by just Paccar or PTC
2.	Next to the logo, put the title for the project “Chassis History”
3.	Remove the three lines icon next to the logo
4.	Put the vehicle information on the Dashboard panel. Allow the panel to expand or collapse.
5.	Make the filter section smaller and give more space to the graphic. Avoid scrolling the page.
6.	Remove title for the filer or change the title (For Filter with chassis ID / ESN, changed by Search. For Filter Axis, changed by Chart axis configuration).
7.	Move the Y Axis, next to the X axis to have more space. Put some line separator between x Axis and y Axis.
8.	Replace PACCAR Solution by Paccar Technical Center at the bottom of the page. The copyright should be the footer bar that extend all the page and it should have a slightly different color with a line at the top.
9.	Add the user name next to the user icon at the top bar. When the icon is clicked, remove the setting option.

```
