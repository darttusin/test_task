import os


# получение переменных окружения для бд
DBUSER = os.environ.get('DBUSER')
DBPASSWORD = os.environ.get('DBPASSWORD')
DBHOST = os.environ.get('DBHOST')
DBNAME = os.environ.get('DBNAME')
DBPORT = os.environ.get('DBPORT')