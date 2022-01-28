from django.core.management.base import BaseCommand
from commands.models import user_details
from .functions_file.function_msg import *

class Command(BaseCommand):
    help = 'run in order to join'

    def add_arguments(self, parser):
        parser.add_argument('view_group',type=str,help = 'view Group name')
        parser.add_argument('group',type=str,help = 'Group name')
        parser.add_argument('msg',type=str,help = 'Message')
    def handle(self,*args, **kwargs):
        msg = kwargs['msg']
        group = kwargs['group']
        view_group = kwargs['view_group']
        while True:
            for i in user_details.objects.all():
                print(i)
                number = i.number
                api_id = i.api_id
                api_hash = i.api_hash
                client = TelegramClient(f'./sessions/{number}',api_id,api_hash)
                banned = user_banned(client,number,api_id,api_hash) 
                if banned:
                    continue
                else :
                    send_messages(view_group,group,msg,client,number)
                time.sleep(random.randint(30,60))
            time.sleep(random.randint(600,1200))