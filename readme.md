Инструкция по развертыванию



1. Установите дистрибутив Ubuntu версии 24.04+ (можно на компьютере с ОС Windows, понадобится VirtualBox и iso-образ дистрибутива)



2. Подготовьте структуру проекта, загрузив фласк-проект из гитхаб в папку по адресу Documents/



3. Откройте загруженный файл app.py в корневой папке проекта, найдите в нём нижеследующую строку:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://CHANGEMELOGIN:CHANGEMEPASSWORD@localhost/mydatabase'

Замените в ней CHANGEMELOGIN и CHANGEMEPASSWORD на данные, которые вы будете использовать в PostgreSQL для доступа к БД: имя учетной записи (все буквы нижнего регистра) вместо CHANGEMELOGIN и пароль вместо CHANGEMEPASSWORD соответственно. Примените изменения.



4. Вернитесь в Терминал и установите нижеследующие компоненты:
4.1. Nginx
4.2. Gunicorn
4.3. Python
4.4. Pip
4.5. Flask (версии 3.1.1)
4.6. SQLAlchemy
4.7. PostgreSQL



5. Убедитесь в том, что:
5.1. Вы находитесь в [venv]
5.2. Вы создали БД под названием mydatabase в PostgreSQL
5.3. Вы зарегистрировали учетную запись в PostgreSQL, ее имя и пароль соответствуют указанным вами в файле app.py, и у нее есть все права на взаимодействие с БД



6. Настройте конфиги
6.1. Откройте конфиг Nginx командой:

sudo nano /etc/nginx/sites-available/flask_project

и вставьте содержимое:

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/Documents/myproj/static/;
    }
}

6.2. Выполните в Терминале следующие команды:

sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

6.3. Создайте в корневой папке проекта файл gunicorn.conf.py и заполните его следующим содержимым:

bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5
loglevel = "info"
accesslog = "-"
errorlog = "-"
reload = False

6.4. Выполните в Терминале следующую команду:

gunicorn app:app -c gunicorn.conf.py



7. Убедитесь в том, что структура проекта выглядит так:

myproj/
├── app.py
├── gunicorn.conf.py

myproj/
├── app.py
├── gunicorn.conf.py
├── templates/
│   ├── index.html
│   └── view_data.html
├── static/
│   └── js/
│   	└── scripts.js
└── README.md

8. Запустите проект
8.1. Выполните в Терминале команду:

Flask run

8.2. Откройте браузер вашего дистрибутива
8.3. Введите в адресную строку:

http://127.0.0.1:5000

8.4. Используя кнопки и поля для ввода, внесите некоторое количество данных, после чего подтвердите их отправку.
8.5. После переадресации на страницу 127.0.0.1:5000/submit нажмите на адресную строку и замените в ней слово submit на слово view. Просмотрите таблицу с данными, полученными из вашей БД



9. Для остановки работы Flask-приложения вернитесь в Терминал и воспользуйтесь сочетанием клавиш Ctrl+C









