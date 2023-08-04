# Продуктовый помощник
Приложение "Продуктовый помощник": сайт, на котором вы можете публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.

# Запуск проекта
## Создайте файл .env
```
SECRET_KEY=<...>
DB_ENGINE=django.db.backends.postgresql # укажите, с какой базой данных вы работаете
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к базе данных (создайте свой собственный)
DB_HOST=db # название хоста (контейнера)
DB_PORT=5432 # порт для подключения к базе данных
```
### Сборка контейенеров
Перейдите в папку infra и запустите команду в терминале

```
docker compose up -d
```
#### Создайте суперпользователя
```
docker compose exec backend python manage.py createsuperuser
```

### Заполнение базы данных
Заполните БД подготовленными данными при первом запуске

``` 
docker compose exec backend python manage.py loaddata fixtures/ingredients.json
```