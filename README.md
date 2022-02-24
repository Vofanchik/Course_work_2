# VKinder
Приложение для поиска пары в контакте
##Подготовка к работе
Для настройки работы приложения в файле settings.py необходимо:
 1. Записать в переменную token токен вашей группы в которой
 будет работать бот. Инструкция https://github.com/netology-code/py-advanced-diplom/blob/new_diplom/group_settings.md
 2. Записать в переменную token_app токен вашего приложения. Инструкция https://dev.vk.com/api/getting-started#%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F
 3. Записать в переменную database_path название/путь базы данных для записи уже отправленных пользователей
 4. Установить зависимости командой `pip install -r requirements.txt`
 ##Поиск пары
 После подготовки необходимо написать боту группы в личном сообщении id ползователя для которого ищем пару. Если недостаточно данных
 на странице пользователя, то нужно прописать их по инстукции бота.
 ##Результат
 После выполнения данных действий, вам будут направлены 3 фотографии и ссылка на подходящего пользователя. Далее нужно действовать по инструкции бота.