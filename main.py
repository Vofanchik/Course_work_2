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
count = 0
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if re.match(r'\d{1,9}', request):
                try:
                    list_id_photo = main_logic.get_user_info(request, access_token=token_app)
                    print(list_id_photo)
                    if type(list_id_photo) == dict and not 'bday' in list_id_photo:
                        write_msg(event.user_id, 'Укажите дату рождения в формате дд.мм.гггг')
                    else:
                        list_id_photo = [t for t in list_id_photo if t[0] not in db.return_ids()]
                        write_msg(event.user_id, f'https://vk.com/id{list_id_photo[count][0]}', list_id_photo[count][1])
                        count +=1
                        db.insert_data(list_id_photo[0][0])
                except:
                    write_msg(event.user_id, "Возникла проблемма, попробуйте другой ID")

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
