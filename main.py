from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import re
import requests
import main_logic


token_app = ''
token = ''

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
vk_ap = vk.get_api()
db = main_logic.DB()


def write_msg(user_id, message='', images=[]):
    session = requests.Session()
    attachments = []
    upload = vk_api.VkUpload(vk)
    for i in images:
        image = session.get(i, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append(
            'photo{}_{}'.format(photo['owner_id'], photo['id'])
        )
    vk_ap.messages.send(
        user_id=user_id,
        attachment=','.join(attachments),
        message=f'{message}',
        random_id=randrange(10 ** 7)
    )
list_id_photo = []
lack_data = {}
count = 0
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request.isdigit():
                try:
                    list_id_photo = main_logic.get_user_info(request, access_token=token_app)
                    if type(list_id_photo) is dict:
                        lack_data = list_id_photo
                        list_id_photo = []
                        print(lack_data)
                        write_msg(event.user_id, 'Укажите дату рождения в формате дд.мм.гггг и город через запятую')
                    else:
                        list_id_photo = [t for t in list_id_photo if t[0] not in db.return_ids()]
                        write_msg(event.user_id, f'https://vk.com/id{list_id_photo[count][0]}', list_id_photo[count][1])
                        count +=1
                        db.insert_data(list_id_photo[0][0])
                except:
                    write_msg(event.user_id, "Возникла проблемма, попробуйте другой ID")

            elif bool(re.search(r'\d{1,2}\.\d{1,2}\.\d{4}\,\s?[а-яА-Я]+\s?[а-яА-Я]*\s?[а-яА-Я]*', request)):

                info = request.split(',')
                lack_data['city'] = main_logic.city_search(info[1], token_app)
                lack_data['bdate'] = info[0]
                list_id_photo = main_logic.match_search(lack_data, token_app)
                list_id_photo = [t for t in list_id_photo if t[0] not in db.return_ids()]
                write_msg(event.user_id, f'https://vk.com/id{list_id_photo[count][0]}', list_id_photo[count][1])
                count += 1
                db.insert_data(list_id_photo[0][0])

            elif request == 'далее':
                if list_id_photo != []:
                    write_msg(event.user_id, f'напишите далее, чтобы увидеть следующего кандидата или новый ID\n'
                                             f'https://vk.com/id{list_id_photo[count][0]}', list_id_photo[count][1])
                    db.insert_data(list_id_photo[count][0])
                    count+=1
                else:
                    write_msg(event.user_id, "Напишите корректный id пользователя для которого ищем пару")

            else:
                write_msg(event.user_id, "Напишите корректный id пользователя для которого ищем пару")
