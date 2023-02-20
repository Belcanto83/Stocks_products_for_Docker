## Инструкция по запуску Django-приложения через Docker

### Первый вариант

1. Перейдите в директорию вашего проекта: \<repository-root>/3.2-crud/stocks_products/
2. Создайте и запустите контейнер PostgreSQL на базе стандартного образа "postgres" из https://hub.docker.com/_/postgres следующей командой:
    ```shell
    docker run --name some-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
    ```
    Данная команда создает работающую базу данных и пользователя с именем "postgres". Пароль пользователя "postgres" задается переменной окружения "POSTGRES_PASSWORD=password".
3. Создайте образ вашего Django-приложения из Docker-файла с помощью команды:
    ```shell
    docker build -t myapp_image .
    ```
4. Запустите контейнер вашего Django-приложения на основе созданного вами образа следующей командой:
   ```shell
   docker run --env-file .env --link some-postgres:db --name myapp -p 8000:8000 --rm -it myapp_image
   ```
   Необходимые для работы Django-приложения переменные окружения хранятся в файле ".env". Связь с базой данных задается параметром "--link".
5. Работающее Django-приложение доступно по адресу: http://localhost:8000/

### Второй вариант

1. Перейдите в директорию вашего проекта: \<repository-root>/3.2-crud/stocks_products/
2. Создайте новую сеть командой:
    ```shell
    docker network create test-net
    ```
3. Создайте и запустите контейнер PostgreSQL на базе стандартного образа "postgres" из https://hub.docker.com/_/postgres в созданной сети "test-net" следующей командой:
    ```shell
    docker run --name some-postgres -e POSTGRES_PASSWORD=password --network test-net -p 5432:5432 -d postgres
    ```
    Данная команда создает работающую базу данных и пользователя с именем "postgres". Пароль пользователя "postgres" задается переменной окружения "POSTGRES_PASSWORD=password".
4. Создайте образ вашего Django-приложения из Docker-файла с помощью команды:
    ```shell
    docker build -t myapp_image .
    ```
5. Запустите контейнер вашего Django-приложения в этой же сети "test-net" на основе созданного вами образа следующей командой:
   ```shell
   docker run --env-file .env --name myapp --network test-net -p 127.0.0.1:8000:8000 --rm myapp_image
   ```
   Необходимые для работы Django-приложения переменные окружения хранятся в файле ".env". В файле ".env" должна быть следующая переменная окружения: DB_HOST=some-postgres, где "some-postgres" - это имя запущенного контейнера с БД.
6. Работающее Django-приложение доступно по адресу: http://localhost:8000/
