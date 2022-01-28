import time
import random
from telethon import TelegramClient
import telethon
from telethon.sync import TelegramClient
from commands.models import *
import os
def send_messages(view_group,groupname,Message,client,number):
    try:
        client.start()
        if client.is_user_authorized():
            me = client.get_me()
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                print(f"{me.first_name} has Marked as seen in {view_group}'s chat")
            else : 
                print(f'{number}No new messages in this {view_group} ')
            entity1 = client.get_entity(groupname)
            if client.send_read_acknowledge(entity1):
                print(f"{me.first_name} has Marked as seen in {groupname}'s chat")
            else : 
                print('Marked as seen is not completed !')
            client.send_message(groupname,Message)
            print(f'{me.first_name} has been sent Message')
            time.sleep(random.randint(5,10))
        else:
            print(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except Exception as e :
        client.disconnect()
        print(e)

def view_chat(groupname,client,number):
    try:
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            entity = client.get_entity(groupname)
            if client.send_read_acknowledge(entity):
                print(f"{me.first_name} has Marked as seen in {groupname}'s chat")
            else : 
                print(f'{number}No new messages in this {groupname} ')
        time.sleep(random.randint(3,5))
        client.disconnect()
    except Exception as e:
        client.disconnect()
        print(e)


def user_banned(client,number,apiid,apihash):
    try:
        banned = False
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone=number)
                client.sign_in(code=(input(f'Eneter code of {number}')))
                client.disc
                client.disconnect()

                return banned
            except telethon.errors.rpcerrorlist.PhoneNumberBannedError:
                print(f'Phone number {number} is banned !')
                if os.path.exists(f'./sessions/{number}'):
                    os.remove(f'./sessions/{number}')
                    banned = True
                    client.disconnect()
                client.disconnect()
                return banned
        else: 
            client.disconnect()
            return banned
    except Exception as e:
        client.disconnect()
        print(e)