from datetime import datetime
import random
from django.core.management.base import BaseCommand
from home.management.commands.functions.functions import port_device
from models import avds
from home.tiktok import tiktok
class Command(BaseCommand):
    help = 'Create random users'


    def handle(self, *args, **kwargs):
        port,devices = port_device()
        port = random.choice(port)
        devices = random.choice(devices)
        print(port,'------------',devices)
        useravd = avds.objects.create(name = devices,port=port)
        tiktok(useravd.name)

        pass
