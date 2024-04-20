# vet_bot
Бот, загружающий расписание занятий для студентов факультета ветеринарной медицины</br></br>
Стек: Pyton aiogram, BeautifulSoup, SQLAlchemy, request</br></br>
Бот, показывающий текущее расписание занятий студентам факультета 
ветеринарной медицины. Позволяет ввести и сохранить номер группы 
пользователя для получения расписания группы обучающегося. Производит парсинг 
сайта университета для получения расписания занятий, парсинг сайта с 
картинками ветеринарной практики и вывод одной случайной.</br>


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
![image](https://github.com/CrockoMan/vet_bot/assets/125302139/88b18fb0-afb9-466d-93dc-ae57f64737c8)

 Автор: [К.Гурашкин](<https://github.com/CrockoMan>)
