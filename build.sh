#Build the project
echo "Build the project...."
python3.10.6 -m pip install -r requirements.txt

echo "Make Migrations...."
python3.10.6 manage.py makemigrations  --noinput
python3.10.6 manage.py migrate  --noinput

echo "Collect static...."
python3.10.6 manage.py collectstatic  --noinput
