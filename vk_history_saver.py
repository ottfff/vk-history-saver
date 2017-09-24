import time
import vk
import codecs
import os

class VKHistorySaver:
    def __init__(self, accessToken):
        session = vk.Session(access_token=accessToken)
        self.api = vk.API(session)

    def saveHistory(self, friend_id: str, dest):
        print('Начинаем сохранять историю сообщений c ' + str(friend_id) + ' в файл: ' + dest + '.')
        hist_part = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=0)
        msgs_cnt = hist_part['count']
        print('Всего сообщений: ' + str(msgs_cnt))
        parent_dir = os.path.abspath(os.path.join(dest, os.pardir))
        os.makedirs(parent_dir)
        file = codecs.open(dest, 'a+','utf-8')
        messages = []
        offset_i = 0
        while offset_i < msgs_cnt:
            msg_hist = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=200, offset=offset_i)
            offset_i += 200
            msgs = msg_hist['items']
            messages.extend(msgs)
            time.sleep(0.3)
            print('Обработано сообщений: ' + str(len(messages)))
            for msg in msgs:
                file.write(str(msg) + '\n')
        file.close()