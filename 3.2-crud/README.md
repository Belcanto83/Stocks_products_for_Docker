## Инструкция по запуску Django-приложения через Docker Compose

1. Перейдите в директорию вашего проекта: \<repository-root>/3.2-crud/
2. Запустите сразу все необходимые для работы приложения контейнеры (postgres, nginx, stocks_products) следующей командой:
    ```shell
    docker-compose up -d --build
    ```
3. Примените все необходимые миграции в базу данных::
    ```shell
    docker-compose exec stocks_products python manage.py migrate --noinput
    ```
4. Соберите все необходимые статические файлы:
   ```shell
   docker-compose exec stocks_products python manage.py collectstatic --no-input --clear
   ```
   "Обмен" статическими файлами между запущенными контейнерами осуществляется с помощью общего volume "static_vol", примонтированного к обоим контейнерам "stocks_products" и "nginx"
5. Работающее Django-приложение доступно по адресу: http://localhost:8080/
6. Для остановки приложения используйте команду:
   ```shell
    docker-compose down -v
   ```
