from dotenv import load_dotenv
import os
load_dotenv()



from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
webhook = os.getenv('WEBHOOK')


bit = Bitrix(webhook)


def get_all_users():
    users = bit.get_all('user.get', params={'filter':{'ACTIVE': 'Y'}})
    return users

def create_event(dictUser:dict):

    bit.call('calendar.event.add',  dictUser)
    
def get_all_contact():
    contact = bit.get_all('crm.contact.list')
    return contact

def create_event_to_brithday():
    users = get_all_users()
    users=get_all_contact()   
    
    for user in users:
        # birthday = user.get('PERSONAL_BIRTHDAY')
        
        birthday = user.get('BIRTHDATE')
        if birthday =='': continue
        #2024-07-09T03:00:00+03:00
        name=user.get('NAME')
        second_name=user.get('SECOND_NAME')
        last_name=user.get('LAST_NAME')
        birthday=birthday.split('T')[0]+'T11:00:00' 
        print(birthday)
        title=f'🎁 - {last_name} {name} {second_name}'
        print(title)

        fields={
            'name': title,
            'from':birthday,
            'to':birthday,
            'ownerId': ' ',
            'section': 1,
            'type':'company_calendar',
            # 'type':'user',
            "rrule": {
                "FREQ": "YEARLY",
                "INTERVAL": 1,
                "UNTIL": "01.01.2033",
                "~UNTIL": ""
            },
            'is_meeting': 'Y',
            'attendees':[1,f'C_{user.get("ID")}'],
            # 'UF_CRM_CAL_EVENT':[f'C_{user.get("ID")}']
            # 'UF_CRM_CAL_EVENT[]':[f'C_{user.get("ID")}']
            
            
        }
        pprint(fields)
        create_event(fields)
        1/0
        break


        pass        

def main():
    users=get_all_users()
    pprint(users)

create_event_to_brithday()
# cont=get_all_contact()
# pprint(cont)


