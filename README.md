# vk-history-saver
Сохраняет историю переписки с конкретным человеком в файл

## Необходимые компненты

* python 3
* библиотека vk

Для выкачивания истории сообщений и/или фотографий из истории сообщений, нужно передать в метод ACCESS TOKEN, FRIEND ID и OUTPUT
По каждому из этих пунктов поговорим подробнее:

### ACCESS TOKEN
Это внтренний ключ доступа к ВК. Согласно [документации вк](https://vk.com/dev/access_token), для его получения необходимо создать standalone-приложение и настроить ему права, чтобы оно имело доступ до личных сообщений пользователей. Мной уже было создано такое приложение и для получения access token'а вам достаточно пройти по [ссылке](https://oauth.vk.com/authorize?client_id=6145982&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=messages&response_type=token&v=5.67&state=123456). Если вы не авторизованы, то потребуется авторизоваться в вк. Данная технология придумана поддержкой ВК и не компроментирует ваш пароль (но получает доступ к личным сообщениям). Теперь в строке браузера отобразится примерно следующее:  `https://oauth.vk.com/blank.html#access_token=MY_ACCESS_TOKEN&expires_in=86400&user_id=MY_USER_ID&state=123456`
Таким образом мы получаем access token, который предоставляет доступ к вашими личными сообщениями.

### FRIEND ID
Это id вашего друга, преписку с которым вы хотите сохранить. Узнать его можно просто перейдя к нему на страницу и в строке браузера отобразится примерно следующее `https://vk.com/id12345678`, иначе можно кликнуть по времени из любой записи на стене и в строке браузера отобразится его id: `https://vk.com/smth?w=wallFRIEND_ID_2004359`.

### OUTPUT
Это либо директория, либо файл, в который нужно записать результат.

Интерфейс
---

В классе `VKHistorySaver` в конструктор передается access token. Для пользования в нем имеются два метода: `saveHistory` и `saveHistoryPhotos`, сохранящие историю сообщений в файл , и фотографии из истории в директорию соответственно. Оба метода принимают первым аргументом friend id и вторым - output.


Пример использования:
---
```
from vk_history_saver import VKHistorySaver

ACCESS_TOKEN = 'my_access_token'
FRIEND_ID = '12345678'
OUTPUT_FILE = 'C:\\messages.txt'
OUTPUT_DIR = 'C:\\photos'

vkhs = VKHistorySaver(ACCESS_TOKEN)
vkhs.saveHistory(FRIEND_ID, OUTPUT_FILE)
vkhs.saveHistoryPhotos(FRIEND_ID, OUTPUT_DIR)
```
