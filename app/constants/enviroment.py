from os import environ as env


# получение переменных окружения для бд
DBUSER: str | None = env.get('DBUSER')
DBPASSWORD: str | None = env.get('DBPASSWORD')
DBHOST: str | None = env.get('DBHOST')
DBNAME: str | None = env.get('DBNAME')
DBPORT: str | None = env.get('DBPORT')


# DBUSER = 'admin'
# DBPASSWORD = 'admin'
# DBHOST = 'localhost'
# DBNAME = 'postgres'
# DBPORT = '5432'
# раскоментить для тестов 
# также изменить в мейн файле путь до posts.csv на ./files/posts.csv
