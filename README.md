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



<VirtualHost *:80><br/>
ServerAdmin webmaster@example.com<br/>
DocumentRoot /home/ubuntu/chassis<br/>
ErrorLog ${APACHE_LOG_DIR}/error.log<br/>
CustomLog ${APACHE_LOG_DIR}/access.log combined<br/>

Alias /static /home/ubuntu/chassis/staticfiles<br/>
<Directory /home/ubuntu/chassis/staticfiles><br/>
Require all granted<br/>
</Directory><br/>

<Directory /home/ubuntu/chassis/project><br/>
<Files wsgi.py><br/>
Require all granted<br/>
</Files><br/>
</Directory><br/>
WSGIDaemonProcess chassis python-path=/home/ubuntu/chassis python-home=/home/ubuntu/chassis/my_project_venv<br/>
WSGIProcessGroup chassis<br/>
WSGIScriptAlias / /home/ubuntu/chassis/project/wsgi.py<br/>
</VirtualHost><br/>
