## Инструкция по запуску Django-приложения через Docker Compose

### Сборка всех нужных образов проекта из Докер-файлов

1. Скачайте к себе все необходимые папки и файлы проекта
2. Перейдите в директорию проекта: \<repository-root>/3.2-crud/
3. Запустите сразу все необходимые для работы приложения контейнеры (postgres, nginx, stocks_products) следующей командой:
    ```shell
    docker-compose up -d --build
    ```
4. Примените все необходимые миграции в базу данных::
    ```shell
    docker-compose exec stocks_products python manage.py migrate --noinput
    ```
5. Соберите все необходимые статические файлы:
   ```shell
   docker-compose exec stocks_products python manage.py collectstatic --no-input --clear
   ```
   "Обмен" статическими файлами между запущенными контейнерами осуществляется с помощью общего volume "static_vol", примонтированного к обоим контейнерам "stocks_products" и "nginx"
6. Работающее Django-приложение доступно по адресу: http://localhost:8080/
7. Для остановки приложения используйте команду:
   ```shell
    docker-compose down -v
   ```
### Загрузка всех нужных образов из Докер-хаба (разворачивание приложения на "production" сервере)

1. Скопируйте на рабочий сервер папку "for_production"
2. Запустите приложение:
    ```shell
    docker-compose up -d
    ```
3. Примените все необходимые миграции в базу данных:
    ```shell
    docker-compose exec stocks_products python manage.py migrate --noinput
    ```
4. Соберите все необходимые статические файлы:
   ```shell
   docker-compose exec stocks_products python manage.py collectstatic --no-input --clear
   ```
5. Работающее Django-приложение доступно извне по адресу: http://\<ip-адрес-вашего-сервера>:8080/. При наличии фаервола убедитесь, что порт 8080 открыт.
6. Для остановки приложения используйте команду:
   ```shell
    docker-compose down -v
   ```
