import time
import random
from telethon import TelegramClient
from telethon.sync import TelegramClient
from commands.models import *
import telethon,os

def send_messages(view_group,groupname,Message,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                print(f"{me.first_name} {number} have Marked as seen in {view_group}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {view_group}'s chat")
            if client.send_message(groupname,Message):
                print(f'+{number} {me.first_name} has sent a message in {groupname}')
            else:
                print(f"+{number} {me.first_name} couldn't sent Message in {groupname}")
            time.sleep(random.randint(5,10))
        else:
            print(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except Exception as e :
        client.disconnect()
        print(e)

def view_chat(groupname,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            entity = client.get_entity(groupname)
            if client.send_read_acknowledge(entity):
                print(f"{me.first_name} {number} have Marked as seen in {groupname}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {groupname}'s chat")
        time.sleep(random.randint(3,5))

        client.disconnect()
    except Exception as e :
        client.disconnect()
        print(e)

def user_banned(number,apiid,apihash):
    try:
        banned = False
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone=number)
                client.sign_in(code=(input(f'Eneter code of {number}')))
                client.disconnect()
                return banned
            except telethon.errors.rpcerrorlist.PhoneNumberBannedError:
                print(f'Phone number {number} is banned !')
                if os.path.exists(f'./sessions/{number}.session'):
                    banned = True
                    os.remove(f'./sessions/{number}.session')
                    user_details.objects.filter(number=number).delete()
                print(f'{number} is deleted from DATABASE')
                banned = True
                client.disconnect()
                return banned
        else: 
            client.disconnect()
            return banned
    except Exception as e :
        client.disconnect()
        print(e)


def script_chat(i,number,id,hash,msg,group):
    try:
        # print(i,number,'----------',msg)
        client = TelegramClient(f'./sessions/{number}',id,hash)
        client.connect()
        entity = client.get_entity(group)
        client.send_message(entity,msg)
        f_name = client.get_me().first_name
        print(f"{number} : {f_name} --- sent a message {msg}")
        time.sleep(random.randint(3,5))
        client.disconnect()

    except Exception as e:
        client.disconnect()
        print(e)   



















