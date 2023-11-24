import traceback
import requests
import vk_api
import json
import os

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from dotenv import load_dotenv

from logger import logger
from messages import *


load_dotenv(dotenv_path=".env")
token_vk = os.getenv("TOKEN")

vk = vk_api.VkApi(token=token_vk)
session_api = vk.get_api()
longPool = VkBotLongPoll(vk, 223586243)


user_data = {}


running = True
while running:
    try:
        for event in longPool.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                chat_id = event.object.peer_id
                from_id = event.object.from_id
                text_m = event.object.text.lower()
                id_mes = event.object.conversation_message_id
                er_text = event.object.text
                if text_m == 'зарегистрироваться':
                    logger.debug(f'Пользователь {from_id} зарегистрировался')
                    if chat_id not in user_data:
                        user_data[chat_id] = [{
                            'fio': '',
                            'old': '',
                            'exp': '',
                            'int': '',
                            'nav': '',
                            'wht': '',
                            'con': ''
                        }, 'fio']
                    else:
                        # TODO
                        pass
                    vk.method('messages.send', {'peer_id': chat_id,
                                                'message': 'Введите ваше ФИО',
                                                'random_id': 0})
                elif chat_id in user_data:
                    if user_data[chat_id][1] == 'fio':
                        logger.debug(f'Пользователь {from_id} ввел ФИО')
                        user_data[chat_id][0]['fio'] = text_m
                        user_data[chat_id][1] = 'old'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Введите ваш возраст',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'old':
                        logger.debug(f'Пользователь {from_id} ввел опыт работы')
                        user_data[chat_id][0]['old'] = text_m
                        user_data[chat_id][1] = 'exp'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Введите ваш опыт работы',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'exp':
                        logger.debug(f'Пользователь {from_id} ввел свои интересы')
                        user_data[chat_id][0]['exp'] = text_m
                        user_data[chat_id][1] = 'int'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Введите ваши интересы',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'int':
                        logger.debug(f'Пользователь {from_id} ввел свои навыки')
                        user_data[chat_id][0]['int'] = text_m
                        user_data[chat_id][1] = 'nav'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Введите ваши основные навыки',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'nav':
                        logger.debug(f'Пользователь {from_id} ввел интересы на митапе')
                        user_data[chat_id][0]['nav'] = text_m
                        user_data[chat_id][1] = 'wht'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Напиши, что хотите узнать на митапе',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'wht':
                        logger.debug(f'Пользователь {from_id} ввел свои контакты')
                        user_data[chat_id][0]['wht'] = text_m
                        user_data[chat_id][1] = 'con'
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Введите ваши контакты',
                                                    'random_id': 0})
                    elif user_data[chat_id][1] == 'con':
                        user_data[chat_id][0]['con'] = text_m
                        user_data[chat_id][1] = ''
                        logger.info(f'Пользователь {from_id} успешно зарегестрировался')
                        logger.info(f'Данные пользователя{from_id}: {user_data[chat_id][0]}')
                        vk.method('messages.send', {'peer_id': chat_id,
                                                    'message': 'Вы успешно зарегистрированы!',
                                                    'random_id': 0})
                    else:
                        #TODO
                        pass
                else:
                    met = vk.method('photos.getMessagesUploadServer')
                    b = requests.post(met['upload_url'],
                                      files={'photo': open('1.jpeg', 'rb')}).json()
                    c = vk.method('photos.saveMessagesPhoto',
                                  {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                    d = 'photo{}_{}'.format(c['owner_id'], c['id'])

                    keyboard_deck = {'inline': True, 'buttons': [[
                        {"action": {
                            "type": "text",
                            "label": "Зарегистрироваться",
                            "payload": '{"button": "12"}',
                        },
                            "color": "secondary"}
                    ]]}
                    keyboard_deck = json.dumps(keyboard_deck, ensure_ascii=False).encode('utf-8')
                    keyboard_deck = str(keyboard_deck.decode('utf-8'))

                    vk.method('messages.send', {'peer_id': chat_id,
                                                'attachment': d,
                                                'message': start,
                                                'keyboard': keyboard_deck,
                                                'random_id': 0})
    except Exception as e:
        logger.error(traceback.format_exc())
