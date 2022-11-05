# Web-search
Для того, чтобы поднять сервис вам нужно установить elasticsearch

После вы запускаете его командами

```
sudo systemctl start elasticsearch
```

```
sudo systemctl enable elasticsearch
```

Проверяете работу 

```
curl -XGET http://localhost:9200/
```

Результат должен быть ответом в json

После переходим в папку с проектом и пишем команду

```
docker-compose up -d
```

После нужно перейти по 

```
localhost:8000/initialize
```

Чтобы инициализировать сервис

После по роутеру получим словарь с результатами по запросу

```
localhost:8000/find=(ваш текст запроса)
```

Для удаления текста роутер

```
localhost:8000/delete=(айди текста)
```
