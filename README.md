Telegram bot "Tamogochi" EN
=======================


Telegram bot "Tamogochi" is an interactive bot that helps users take care of a virtual pet,
providing a gaming experience and entertainment.

## Installation
### 1. **Cloning the repository**

First, clone the repository to your computer:

```
git clone git@github.com:Chukseev/tamogochi.git
```

### 2. **Setting up the environments**

Copy the file .env_test to the .env file

```
cp .env_test .env
```
Next, you need to specify the configuration. It is recommended to install DB_USER by any user except root, DB_HOST install mysql, so that there would be no conflicts with your mysql on the host system and also with the port.
```
DB_USER=youruser
DB_PASSWORD=yourpassword
DB_HOST=mysql
DB_PORT=3307
DB_NAME=tamogochi

MINIO_ENDPOINT=localhost:9001
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=mybucket

TELEGRAM_TOKEN=token
```
### 3. **Docker Compose**
 Collecting all the images

```
docker compose up --build -d 
```
 

### 4. **Setting min.io**
1. Download images for the bot - [images](https://disk.yandex.ru/d/E2GtgX7sRrSAiw)

2. Log in to the mini.io web app, MINIO_ACCESS_KEY - login,
MINIO_SECRET_KEY - password.
![img](https://i.imgur.com/5a8SK4q.png)

3. Create the bucket.
![img](https://imgur.com/ZBaaD9D.png)

4. Select public acces policy.
![img](https://imgur.com/wlyAwPo.png)
5.Unzip the downloaded archive and upload the files to bucket.
![img](https://imgur.com/awCNFj9.png)
## Usage

1. **Commands**
- /start - user authorization
- /create_pet - pet creation
- /view - pet display
- /inventory - inventory view
- /balance - view the balance
- /feed - feed your pet

Телеграм бот "Тамогочи" RU
=======================

Тееграм бот Тамогочи – 
это интерактивный бот, который помогает пользователям заботиться о виртуальном питомце,
обеспечивая игровой опыт и развлечения.

## Установка
### 1. **Клонирование репозитория**

   Сначала склонируйте репозиторий на ваш компьютер: 

   ```
   git clone git@github.com:Chukseev/tamogochi.git
   ```
   
### 2. **Установка зависимостей**

   Cкопируйте файл .env_test в файл .env

   ```
   cp .env_test .env
   ```
   Далее нужно указать конфигурацию. Рекомендуется установить DB_USER любым пользователем кроме root,  DB_HOST установить mysql,что бы не было конфликтов с вашим mysql на хост системе и также с портом.
    
   ```
   DB_USER=youruser
   DB_PASSWORD=yourpassword
   DB_HOST=mysql
   DB_PORT=3307
   DB_NAME=tamogochi

   MINIO_ENDPOINT=localhost:9001
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   MINIO_BUCKET_NAME=mybucket

   TELEGRAM_TOKEN=token
   ```
    
### 3. **Docker Compose**
   Собираем все образы

```
docker compose up --build -d 
```


### 4. **Настройка min.io**
1. Загрузите изображения для бота - [images](https://disk.yandex.ru/d/E2GtgX7sRrSAiw)

2. Авторизируйтесь в mini.io веб приложении , MINIO_ACCESS_KEY - логин,
MINIO_SECRET_KEY - пароль.
![img](https://i.imgur.com/5a8SK4q.png)

3. Создайте bucket.
![img](https://imgur.com/ZBaaD9D.png)

4. Выберите публичный доступ.
![img](https://imgur.com/wlyAwPo.png)
5.Разархивируйте ранее скачанный архив и загрузите его в bucket.
![img](https://imgur.com/awCNFj9.png)

## Использование 

1. **Команды**
   - /start - авторизация пользователя
   - /create_pet - создание питомца
   - /view - показ питомца
   - /inventory - просмотр инвентаря
   - /balance - просмотр баланса
   - /feed - покормить питомцв

   
   