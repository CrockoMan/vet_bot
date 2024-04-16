# vet_bot
Бот, загружающий расписание занятий для студентов факультета ветеринарной медицины</br></br>
Стек: Pyton BeautifulSoup, aiogram, request</br></br>
Бот, показывающий текущее расписание занятий студентам факультета 
ветеринарной медицины. Производит парсинг сайта университета для получения 
расписания занятий, так же парсит сайт с картинками ветеринарной практики и 
выводит одну случайную.</br>


Порядок работы:</br>
Клонировать репозиторий</br>
```
git clone git@github.com:CrockoMan/vet_bot.git
```

Перейти в каталог проекта

```
cd vet_bot
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
source venv/scripts/activate
```

Установить зависимости:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Заполнить файл .env переменных окружения:</br>
BOT_TOKEN=Токен_бота_telegram</br>

Запуск бота:
```
python main.py
```

 Автор: [К.Гурашкин](<https://github.com/CrockoMan>)