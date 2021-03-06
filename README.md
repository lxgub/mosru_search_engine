mosru_search_engine
=============

Установка и запуск::

    $ cd /mosru_search_engine
    $ python setup.py install
    $ cd /mosru_search_engine/searchengine
    $ python -m searchengine
    ======== Running on http://127.0.0.1:9002 ========

1. При первом запуске скрипт обращается к документу (docs.json) со списком категорий и соответствующим
каждой категории фразам.
2. Скрипт создает inverted index для каждого слова в поисковых фразах. Каждое слово очищается от цифр и небуквенных
символов и приводится к канонической форме (например, форма единственного числа, именительного падежа для
существительных).
3. Для последующего использования индекс сериализуется и сохраняется в файл inverted_index.pickle. (при следующем запуске
файл будет десириализован и использован для поиска без повторного создания индекса).

**Описание**
1. Сервис принимает GET запрос пользователя вида::

    http://{host}:{port}/?req=<ваша поисковая фраза>

2. Определяет, к какой теме или темам может принадлежать запрос (подробности см. ниже).
3. Выдает результат в формате json, в котором указан список соответствущих запросу тем.
прим. {"categories": ["News", "Citchen", "Goods", "Culture", "Events", "Sports"]}

Каждая тема определяется набором фраз, соответствующих определенной категории.  Некоторые фразы могут принадлежать нескольким категориям.
Наборы категорий и фраз располагаются в файле .\docs.json

Предполагается, что наборы фраз все умещаются в оперативной памяти, но при этом могут быть достаточно большими.

**Правило принадлежности запроса теме:**

1. Если набор слов из запроса содержит в себе все слова какой-либо из фраз, то запрос считается соответствующим теме. Иначе - не соответствующим.
2. Порядок слов в запросе и во фразах не учитывается.

**Примеры:**
1. Запрос "где купить зимние шины" соответствует теме "товары", т.к. содержит в себе все слова из фразы "зимние шины".
2. Запрос "борща любимого рецепт" соответствует теме "кухня" т.к. содержит в себе все слова из фразы "рецепт борща".
3. Запрос "тайская кухня" соответствует двум темам: "кухня" и "товары".
4. Запрос "кухня" не соответствует ни одной теме, т.к. не включает в себя целиком слова ни одной из фраз.
