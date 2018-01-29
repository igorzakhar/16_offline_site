# Сайт в оффлайн

Скрипт ```get_offline_template.py``` скачивает и сохраняет html шаблон для работы offline. Так же извлекаются все внешние зависимости, такие как таблицы стилей(```.css```), скрипты (```.js```), favicon(```.ico```). Данные файлы размещаются в соответсвующих директориях (```css/```, ```js/```). Результирующий  html-документ сохраняется в файле ```index.html```.   

За основу взят шаблон Bootstrap: [http://getbootstrap.com/examples/jumbotron/](http://getbootstrap.com/examples/jumbotron/)

# Установка

Для запуска программы требуется установленный Python 3.5.  
Используйте команду pip для установки сторонних библиотек из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).


# Цели проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)
