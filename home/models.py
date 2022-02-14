from django.db import models
from home.management.commands.functions.functions import LOGGER
from home.tiktok import tiktok
from conf import AVD_PACKAGES, AVD_DEVICES
from django.db.models.signals import post_save, pre_delete
from django.conf import settings
import os,random,subprocess
# Create your models here.

class Tittok_user(models.Model):
    bdate = models.CharField(max_length=255)
    number = models.IntegerField(null=False)
    def __str__(self) -> str:
        return self.number

class avds(models.Model):
    name = models.CharField(max_length=255)
    port = models.IntegerField()
    def __str__(self) -> str:
        return self.name



def create_avd(sender, instance, **kwargs):
    created = kwargs.get('created')

    if created:
        LOGGER.info('Start to create AVD')
        try:
            # Initialize bot
            disbot = tiktok(instance.name, start_appium=False, start_adb=False)

            # Create avd
            disbot.create_avd(avd_name=instance.name)
            updated_config = os.path.join(settings.BASE_DIR, 'discordbot/avd_config/config.ini')
            new_config_file = f"{settings.AVD_DIR_PATH}/{instance.name}.avd/config.ini"
            LOGGER.debug(f'updated_config: {updated_config}')
            LOGGER.debug(f'new_config_file: {new_config_file}')
            if os.path.isdir(settings.AVD_DIR_PATH) and \
                    os.path.isfile(new_config_file):
                # os.replace(updated_config, new_config_file)
                from shutil import copyfile
                copyfile(updated_config, new_config_file)

            print(f"**** AVD created with name: {instance.name} and port: {instance.port} ****")

        except Exception as e:
            # commands = [f'lsof -t -i tcp:{instance.port} | xargs kill -9',
            #                 f'lsof -t -i tcp:4724 | xargs kill -9']
            # for cmd in commands:
            #     p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
            instance.delete()
            print(f"Couldn't create avd due to the following error \n")
            print(e)


def create_better_avd(sender, instance, **kwargs):
    created = kwargs.get('created')

    if created:
        LOGGER.info('Start to create AVD')
        try:
            # Initialize bot
            disbot = tiktok(instance.name, start_appium=False, start_adb=False)

            device = random.choice(AVD_DEVICES)  # get a random device
            package = random.choice(AVD_PACKAGES)  # get a random package
            disbot.create_avd(avd_name=instance.name, package=package,
                             device=device)

            LOGGER.info(f"**** AVD created with name: {instance.name} and port: {instance.port} ****")

        except Exception as e:
            # commands = [f'lsof -t -i tcp:{instance.port} | xargs kill -9',
            #                 f'lsof -t -i tcp:4724 | xargs kill -9']
            # for cmd in commands:
            #     p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
            instance.delete()
            LOGGER.error(f"Couldn't create avd due to the following error \n")
            LOGGER.error(e)


def delete_avd(sender, instance, **kwargs):
    try:
        cmd = f'avdmanager delete avd --name {instance.name}'
        p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        pass


#  post_save.connect(create_avd, sender=UserAvd)
post_save.connect(create_better_avd, sender=avds)
pre_delete.connect(delete_avd, sender=avds)