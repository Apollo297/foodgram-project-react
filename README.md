# praktikum_new_diplom

Описание проекта

Foodrgam - сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов, скачивать список ингредиентов, необходимых для приготовления блюда.

Проект доступен по аресу: https://foodgrambrandnew.hopto.org/
Данные админа:
логин: admin
почта: admin@yandex.ru
пароль: admin2530

### Инструкция по запуску проекта:

**1. Клонируйте репозиторий и перейдите в него в командной строке:**
```
git clone git@github.com:Apollo297/foodgram-project-react.git
```

**2. Создайте файл .env и заполните его своими данными:**
```
POSTGRES_USER=[имя_пользователя_базы]
POSTGRES_PASSWORD=[пароль_к_базе]
POSTGRES_DB= [имя_базы_данных]
DB_PORT=[порт_соединения_к_базе]
DB_HOST=[db]
SECRET_KEY=[ключ]
DEBUG=[значение]
```

**3. Создайте Docker-образы:**

- замените username на ваш логин на DockerHub:
```
cd frontend
docker build -t username/foodgram_frontend .
cd ../backend
docker build -t username/foodgram_backend .
cd ../nginx
docker build -t username/foodgram_nginx .
```
**4. Загрузите образы на DockerHub:**
```
docker push username/foodgram_frontend
docker push username/foodgram_backend
docker push username/foodgram_nginx
```
### Деплой на удалённом сервере

**1. Подключитесь к удаленному серверу**
```
ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
```

**2. Создайте на сервере директорию kittygram через терминал**
```
mkdir foodgram-project-react
```

**3. Установите docker-compose на сервер:**
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

**4. Скопируйте в директорию kittygram/ файлы docker-compose.production.yml и .env:**
```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram-project-react/docker-compose.production.yml
```

**5. Запустите docker-compose в режиме демона:**
```
sudo docker compose -f docker-compose.production.yml up -d
```

**6. Соберите статику бэкенда и скопируйте их в /backend_static/static/:**
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

**7. Выполните миграции:**
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

**8. На сервере откройте конфиг Nginx:**
```
sudo nano /etc/nginx/sites-enabled/default
```

**9. Измените настройки location в блоке server:**
```
location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:3000;
}
```

**10. Проверьте конфиг на корректность введённых данных, а затем перезапустите Nginx:**
```
sudo nginx -t 
sudo service nginx reload
```

### Настройка CI/CD

- Инструкция workflow составлена и находится в директории:
```
foodgram-project-react/.github/workflows/main.yml
```
Ниже приведён список секретов, на которые ссылается инструкция workflow.
Добавьте их в GitHub Actions:

```
DOCKER_USERNAME                # имя пользователя в DockerHub
DOCKER_PASSWORD                # пароль пользователя в DockerHub
HOST                           # ip_address сервера
USER                           # имя пользователя
SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
SSH_PASSPHRASE                 # пароль для ssh-ключа
TELEGRAM_TO                    # id телеграм-аккаунта (предоставляет @userinfobot, команда /start)
TELEGRAM_TOKEN                 # token выдаёт бот (@BotFather, /token, имя бота)
```
### Примеры запросов API:

Регистрация пользователя:
- api/users/
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
Получение рецепта
- api/recipes/{id}/
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```


### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/DockerHub-1488C6?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/Gunicorn-00A98F?style=for-the-badge&logo=gunicorn&logoColor=white)

##### Автор: Нечепуренко Алексей



