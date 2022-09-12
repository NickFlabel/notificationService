API сервис на основе django и drf для рассылки сообщений клиентам при помощи внешнего API.
Для запуска проекта при помощи docker-compose необходимо:

Перейти в директорию проекта
Изменить при необходимости переменные окружения в файле docker-compose.yml (FETCH_URL - URL внешнего API для рассылки, JWT - JW token для доступа к внешнему API, RECEIVER_EMAIL - email для ежедневного отчета по направленным сообщениям)
Запустить контейнеры командой docker-compose up

В рамках проекта также реализован сервис flower для отслеживания задач celery. Доступ к нему можно получить по порту :5555
Для просмотра страницы документации по API endpoints необходимо перейти по адресу /docs/ после запуска приложения. Также schema доступна по адресу /openapi/
Для запуска тестов необходимо перейти в терминал по адресу контейнера с веб-приложением django и запустить команду python manage.py test

API endpoints:
http://0.0.0.0:8000/ - api проекта
http://0.0.0.0:8000/clients/ - клиенты
http://0.0.0.0:8000/mailings/ - рассылки
http://0.0.0.0:8000/mailings/all_stats/ - общая статистика по всем рассылкам
http://0.0.0.0:8000/mailings//stats/ - детальная статистика по конкретной рассылке
http://0.0.0.0:8000/docs/ - Swagger UI документация
http://0.0.0.0:5555 - celery flower
