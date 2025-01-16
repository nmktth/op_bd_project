Система парсинга товаров с маркетплейса Озон
Данное веб-приложение предназначено для автоматического извлечения и отображения информации о товарах с маркетплейса Озон. Оно позволяет пользователям эффективно собирать данные о ценах и описаниях товаров, а также управлять этими данными через удобный интерфейс.
## Основные функции:
-   Парсинг товаров: Программа извлекает название, цену, описание и ссылки на товары с маркетплейса Озон, используя библиотеки Requests и Selenium.
-   Хранение данных: Сохранение полученной информации в локальной базе данных SQLite для последующего доступа и анализа.
-   Веб-интерфейс: Все данные отображаются на веб-странице в виде карточек товаров, что обеспечивает пользователям удобный доступ к информации о каждом товаре.
-   Изменение цен: Пользователи могут отслеживать процентное изменение цен товаров по сравнению с первоначальными значениями.
-   Управление товарами: Реализованы функции добавления и удаления карточек товаров через веб-интерфейс.
## Технические характеристики:
-   Программное обеспечение разработано на основе фреймворка Django и использует SQLite в качестве базы данных.
-   Кроссбраузерная совместимость с современными версиями браузеров (Chrome, Firefox).
-   Устойчивое функционирование при парсинге большого числа ссылок с обработкой возможных ошибок.
## Этапы разработки:
1. Создание структуры базы данных и интеграция с Django.
2. Разработка парсера для сбора данных с маркетплейса Озон.
3. Проектирование и внедрение веб-интерфейса для управления товарами.
4. Тестирование всех компонентов приложения и исправление возможных ошибок.
5. Развертывание и запуск системы на сервере.
## Установка и запуск:
Для корректной работы проекта выполните следующие шаги:

1. Установите Python и необходимые библиотеки
Убедитесь, что на вашем устройстве установлен Python версии 3.9 или выше. Затем выполните установку необходимых библиотек. Для этого откройте терминал (или командную строку) и выполните команды:

pip install django requests selenium webdriver_manager

2. Установите Google Chrome
Проект использует Selenium для работы с браузером. Скачайте и установите последнюю версию Google Chrome с официального сайта.
WebDriver для Chrome будет автоматически загружен с помощью webdriver_manager.

3. Запустите сервер
В папке проекта находится исполняемый файл run_server.exe, который автоматизирует запуск сайта. Просто запустите этот файл двойным щелчком мыши или через терминал.

После этого сервер будет автоматически запущен. Перейдите в браузер и откройте сайт по адресу:

http://127.0.0.1:8000/

## Экономический эффект:
Представленная система упрощает процесс мониторинга цен и автоматизирует сбор информации, что значительно экономит время пользователей и повышает эффективность их работы с данными о товарах.
# op_bd_project