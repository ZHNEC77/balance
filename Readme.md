## Установка

### 1. Клонирование репозитория

git clone https://github.com/ZHNEC77/balance.git

### 2. Создание  среды окружения

python -m venv venv

### 3. Запуск среды окружения

source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate # Windows

### 4. Установка пакетов пайтон

pip install -r requirements.txt

### 5. Запуск докер образа бд

docker-compose up -d --build

### 6. Запуск приложения

cd balance_project
python manage.py migrate
### можно создать admin
python manage.py createsuperuser
python manage.py runserver


## API Endpoints

### можно попробовать обратиться к ручкам через http://127.0.0.1:8000/swagger/
### авторизация через Autorize и в value Token ваш_токен

### 1. Регистрация
POST http://127.0.0.1:8000/api/users/register/

Body:
{
    "username": "new_user",
    "password": "securepassword123",
    "email": "user@example.com"
}

### 2. Вход
POST http://127.0.0.1:8000/api/users/login/
Body:
{
    "username": "new_user",
    "password": "securepassword123"
}

Ответ:
{
    "token": "9944b09199c62bcf...",
    "user_id": 1,
    "username": "new_user"
}


### 3. Выход
POST http://127.0.0.1:8000/api/users/new/logout/
Headers:
Authorization: Token ваш_токен

## Управление балансом

### 1. Получение баланса
GET http://127.0.0.1:8000/api/balance/
Headers:
Authorization: Token ваш_токен

### 2. Пополнение баланса
POST http://127.0.0.1:8000/api/balance/deposit/
Headers:
Authorization: Token ваш_токен
Content-Type: application/json
Body:
{
    "amount": 10000  // сумма в копейках (10000 = 100 руб)
}

### 3. Перевод средств
POST http://127.0.0.1:8000/api/balance/transfer/
Headers:
Authorization: Token ваш_токен
Content-Type: application/json
Body:
{
    "amount": 5000,  // сумма в копейках
    "user_id": 2
}

### 4. История операций
GET http://127.0.0.1:8000/api/balance/transactions/
Headers:
Authorization: Token ваш_токен

## Администрирование
Доступно по адресу http://localhost:8000/admin/