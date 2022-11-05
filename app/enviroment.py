import os


# получение переменных окружения для бд
# DBUSER = os.environ.get('DBUSER')
# DBPASSWORD = os.environ.get('DBPASSWORD')
# DBHOST = os.environ.get('DBHOST')
# DBNAME = os.environ.get('DBNAME')
# DBPORT = os.environ.get('DBPORT')


DBUSER = 'admin'
DBPASSWORD = 'admin'
DBHOST = 'localhost'
DBNAME = 'postgres'
DBPORT = '5432'
# раскоментить для тестов 
# также изменить в мейн файле путь до posts.csv на ./files/posts.csv