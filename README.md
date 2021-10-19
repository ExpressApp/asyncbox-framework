# Asyncbox Framework

## Установка 

1. Установка
   
    Склонировать репозиторий с исходниками
    ```bash
    git clone https://github.com/ExpressApp/asyncbox-framework.git
    ```
    Собрать пакет и установить его
    ```bash
    cd asyncbox-framework
    poetry build
    pip install --user dist/asyncbox-0.4.0-py3-none-any.whl
    ```

2. Создание проекта из шаблона
   
    ```bash
    asyncbox -v -t http://path/to/template -p plugin1 -p plugin2 bot_project_name
    cd bot_project_name
    ```
   
3. Установка зависимостей

    ```bash
    poetry install
    ```
    Важно: библиотека asyncbox в созданном проекте будет установлена той версии, которя
    указана в шаблоне файла pyproject.toml. При необходимости вы можете указать нужную
    версию или ветку репозитория следующим образом: 
    ```
    asyncbox = { git = "https://github.com/ExpressApp/asyncbox.git", branch = "master"}
    ```    

4. Обновление
   
    Для обновления библиотеки в проекте:
    ```bash
    poetry update
    ```
   
    Для обновления шаблона для новых проектов - повторить операции из пункта 1.


5. Настройки бота
    
    Настройки бота находятся в файле `app/settings.py` и представляют собой класс
    унаследованный от `pydantic.BaseSettings`. При необходимости можно изменить место
    расположения настроек с помощью переменной окружения `APP_SETTINGS` задав её
    значением строку вида `app.settings:AppSettings`, где до двоеточия указывается
    модуль, а после двоеточия объект внутри модуля.
   
    Функциональность бота можно расширять при помощи плагинов. Список включеных плагинов
    задаётся настройкой `PLUGINS`, которая является списком строк в описанном выше
    формате. Имя класса `Plugin` можно не указывать.
    Плагины вкючённые в библиотеку:
   
    | Путь                             | Описание
    -----------------------------------|:-----------------------------------
    | asyncbox.plugins.logger          | расширенное логирование (Loguru)
    | asyncbox.plugins.sqlalchemy      | БД (PostgreSQL)
    | asyncbox.plugins.redis           | Redis
    | asyncbox.plugins.sentry          | мониторинг ошибок (Sentry)
    | asyncbox.plugins.prometheus      | сбор метрик (Prometheus)

    Каждый из плагинов может требовать наличия определённых настроек. В этом случае
    необходимо добавить соответствующую настройку в класс AppSettings
   
    Список коллекторов хэндлеров комманд задаётся в настроке `COLLECTORS` в таком же
    формате как и список плагинов.
   