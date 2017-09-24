from vk_history_saver import VKHistorySaver

# https://oauth.vk.com/authorize?client_id=6145982&display=page&redirect_uri=https://oauth.vk.com/blank.html &scope=messages&response_type=token&v=5.67&state=123456
ACCESS_TOKEN = 'my_access_token'
FRIEND_ID = '12345678'
OUTPUT_FILE = 'C:\\messages.txt'
OUTPUT_DIR = 'C:\\messages.txt\\photos'

vkhs = VKHistorySaver(ACCESS_TOKEN)
vkhs.saveHistory(FRIEND_ID, OUTPUT_FILE)
vkhs.saveHistoryPhotos(FRIEND_ID, OUTPUT_DIR)