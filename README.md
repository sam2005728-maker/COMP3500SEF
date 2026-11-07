Download Python 3.12, then install package by

cd to Admin_Microservice run:
pip install -r requirements.txt
 
cd to Student Voting System run:
pip install -r requirements_real_useful.txt

Explain:

Since the prototype is 6 years old and it was probably using Python 3.7 back then 6 years ago, its Python version is too old and it stopped updating so its lack of protection and compatibility, so we need to first download Python 3.12 to run it well in vs code.

Therefore, its package also need update compatible with Python 3.12 such as:

Under Admin_Microservice:

requirements.txt

cffi>=1.16.0
click>=7.0
cryptography>=41.0.0
Flask==1.1.1
Flask-Login==0.4.1
Flask-SQLAlchemy==2.4.1
Flask-WTF==0.14.2
itsdangerous==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
pycparser==2.19
PyMySQL==0.9.3
six>=1.16.0
SQLAlchemy==1.3.11
Werkzeug==0.16.0
WTForms==2.2.1
matplotlib
Under Voting_System: 

Its have over 96 package need to download and its lack of performance so i used pipreqs to find clean and useful package compatible with Python 3.12 and renamed it to requirements_real_useful.txt:

Flask==1.1.1
flask_login==0.4.1
flask_mail==0.10.0
Flask_SQLAlchemy==2.4.1
Flask_WTF==0.14.2
mysql-connector-python>=8.0.29
onetimepass==1.0.1
pyqrcode==1.2.1
SQLAlchemy==1.3.11
Werkzeug==0.16.0
WTForms==2.2.1
Jinja2>=3.0.3,<3.1.0
MarkupSafe>=2.0.1,<2.1.0


Database setup:

Download MySQL Server 8.0: https://dev.mysql.com/downloads/installer/ (565.9M)

Download XAMPP for phpMyAdmin: https://www.apachefriends.org/zh_tw/download.html (8.0.30 / PHP 8.0.30) (only select Apache and phpMyAdmin)

Open XAMPP configuration at C:\xampp\phpMyAdmin\config.inc.php and update the password to root, and we can start the apache server for phpmyadmin.

Enter http://localhost/phpmyadmin/ to manage database data more easily by website interface.

Explain:

Since the prototype is using SQL language, we need to download MySQL Server 8.0 to insert, delete or update data.

Then, access phpMyAdmin to create a new database more easily, named votedb which matches the prototype database name.

Start the website: 

cd to Admin_Microservice and run: python wsgi.py
cd to Voting_System and run:
python run.py
