API сервис на основе django и drf для рассылки сообщений клиентам при помощи внешнего API.

Для запуска проекта при помощи docker-compose необходимо:
1. Перейти в директорию проекта
2. Изменить при необходимости переменные окружения в файле docker-compose.yml (FETCH_URL - URL внешнего API для рассылки, JWT - JW token для доступа к внешнему API, RECEIVER_EMAIL - email для ежедневного отчета по направленным сообщениям)
3. Запустить контейнеры командой docker-compose up

Для просмотра страницы документации по API endpoints необходимо перейти по адресу /docs/ после запуска приложения. Также schema доступна по адресу /openapi/

В рамках тестового задания реализованы следующие дополнительные задачи:

1. организовать тестирование написанного кода - написаны тесты для всех API endpoints
3. подготовить docker-compose для запуска всех сервисов проекта одной командой (указано выше)
5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io
8. реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email (реализовано при помощи celery-beat)
9. удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок. (задачи celery откладываются при невозможности исполнения)



