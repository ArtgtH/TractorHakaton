# SlovarikDB*
- Богодист Всеволод
- Сахабутдинов Рустам
- Вичук Артём

# Проект с хакатона EstechChallenge от Петербургского Тракторного Завода #


1. Запуск проекта в bash:

    ```
    docker-compose up --build
    ```
Данный репозиторий содержит изначальную структуру проекта за исключением папок с большими датасетами, которые GitHub не пропускал. 

- Папка `data` содержит данные для первого (поиск аномалий) и второго (построение прогнозной модели) заданий соответственно (ПАПКА УДАЛЕНА);
- В папку `EDA` просим участников положить код по анализу данных и любому другому преобразованию датасета. Рекомендуется формат `.ipynb` (ПАПКА УДАЛЕНА)
- В папке `anomaly_detection` выполняется первое задание соревнования. Здесь необходимо приложить код преобразования данных (если требуется после предыдущего шага), обучения модели для поиска аномалий, выгрузки данных для проверяющей системы.
- В папке `forecasting` ведется работа над вторым заданием, соответственно. Обратите внимание, что данная папка в обязательном порядке должна содержать:  
    - Код обучения модели прогнозирования;  
    - Сохраненный файл с весами обученной модели прогнозирования (можно сохранять через pickle или torch);
    - `.md`-файл с кратким описанием проделанной работы, обоснованием выбора модели, логикой ее работы и другими комментариями от разработчиков;
    - `.ipynb`-ноутбук, демонстрирующий запуск вашей модели на тестовых данных и выгрузку датасета для проверяющей системы. Если вы изменяли данные перед тем, как обучать модель, приложите файл преобразованных данных или приведите обработку в коде ноутбука. У жюри должна быть возможность склонировать ваш репозиторий и без дополнительных усилий запустить предсказания, получив в результате работы ноутбука файл с ответами для проверки в проверяющей системе.
- В `interface` загрузите код пользовательского интерфейса, имитирующего течение времени в соответствии с поданным на вход интерфейсу файлом с данными о тракторе и выводящего элементы UI согласно ТЗ.
- В `video` должна быть доступна демонстрация работающего интерфейса и всей его функциональности (ПАПКА УДАЛЕНА).

__Желаем удачи в решении задач!__
