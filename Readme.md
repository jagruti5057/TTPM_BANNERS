
1.create virtual environment for projects -->>> python3 -m venv venv
2.activate environment                    -->>>(for ubntu)-> source source venv/bin/activate, (for windows)-->venv\Scripts\activate
3.install all requirements from requirements.txt file ---->> pip install -r requirements.txt
4.create database in your php-myadmin for project set varible in .env file 
5.setup email configuration 
6.after setuing it create migrations --->>>  python3 manage.py makemigrations and  python3 manage.py migrate
7.To run project use --->>>  python manage.py runserver or python3 manage.py runserver yourip:port,   example-->>python manage.py runserver 192.168.0.138:8081
