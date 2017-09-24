import codecs
import os
import pathlib
import re
import time
import urllib

import vk


class VKHistorySaver:
    def __init__(self, accessToken):
        self.accessToken = accessToken
        self.session = vk.Session(access_token=accessToken)
        self.api = vk.API(self.session)
        self.frequency = 0.3

    def saveHistory(self, friend_id: str, dest):
        print('Начинаем сохранять историю сообщений c ' + str(friend_id) + ' в файл: ' + dest + '.')
        hist_part = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=0)
        msgs_cnt = hist_part['count']
        print('Всего сообщений: ' + str(msgs_cnt))
        parent_dir = os.path.abspath(os.path.join(dest, os.pardir))
        if not pathlib.Path(parent_dir).exists():
            os.makedirs(parent_dir)
        file = codecs.open(dest, 'a+', 'utf-8')
        messages = []
        offset_i = msgs_cnt - (msgs_cnt % 200)
        while offset_i >= 0:
            try:
                msg_hist = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=200, offset=offset_i)
            except:
                self.session = vk.Session(self.accessToken)
                self.api = vk.API(self.session)
                msg_hist = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=200, offset=offset_i)
            msgs = msg_hist['items']
            messages.extend(msgs)
            time.sleep(self.frequency)
            print('Обработано сообщений: ' + str(len(messages)))
            for msg in reversed(msgs):
                file.write(str(msg) + '\n')
            offset_i -= 200
        file.close()

    def saveHistoryPhotos(self, friend_id: str, dest):
        print('Начинаем сохранять фотографии из истории сообщений c ' + str(friend_id) + ' в директорию: ' + dest + '.')
        hist_part = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=0)
        msgs_cnt = hist_part['count']
        print('Всего сообщений: ' + str(msgs_cnt))
        if not pathlib.Path(dest).exists():
            os.makedirs(dest)
        messages = []
        offset_i = msgs_cnt - (msgs_cnt % 200)
        img_counter = 0
        while offset_i >= 0:
            try:
                msg_hist = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=200, offset=offset_i)
            except:
                self.session = vk.Session(self.accessToken)
                self.api = vk.API(self.session)
                msg_hist = self.api.messages.getHistory(user_id=friend_id, v='5.67', count=200, offset=offset_i)
            msgs = msg_hist['items']
            messages.extend(msgs)
            time.sleep(self.frequency)
            print('Обработано сообщений: ' + str(len(messages)))
            for msg in reversed(msgs):
                attachments = msg.get('attachments', [])
                for attachment in attachments:
                    if attachment['type'] == 'photo':
                        photo = attachment['photo']
                        keys = photo.keys()
                        max_res = 0
                        for key in keys:
                            s = re.search('photo_(\d+)', key)
                            if s is not None:
                                res = int(re.search('photo_(\d+)', key).group(1))
                                if res > max_res: max_res = res
                        href = photo['photo_' + str(max_res)]
                        self.save_img(href, str(img_counter), dest)
                        img_counter += 1
            offset_i -= 200

    def save_img(self, href, number, output_dir):
        img_name = '00000'[:-len(number)] + number + '_' + re.search('[^/]+$', href).group(0)
        output_file = str(pathlib.Path(output_dir, img_name))
        urllib.request.urlretrieve(href, output_file)
        print('Image ' + str(href) + ' saved into ' + output_file + '.')
