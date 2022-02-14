import traceback,os
from home.models import *
from home.management.commands.functions.functions import *
from conf import WAIT_TIME
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from ppadb.client import Client as AdbClient
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tiktok.settings import *
from django.conf import settings


class tiktok:
    def __init__(self,emulator_name,start_appium = True,start_adb = True) -> None:
        self.emulator_name = emulator_name
        self.user_avd = avds.objects.get(name=emulator_name)
        self.kill_bot_process(appium=True, emulators=True)
        self.app_driver = None
        self.emulator_port = None
        self.service = self.start_appium(port=4724) if start_appium else None
        self.adb = AdbClient() if start_adb else None
        self.device = None
        
        self.logger = LOGGER
        self.get_device_retires = 0
        self.start_driver_retires = 0
        log_activity(
            self.user_avd.id,
            action_type="TiktokBotInit",
            msg=f"Initiated DiscordBot instance with {self.user_avd.name}",
            error=None,
        )

        self.wait_time = WAIT_TIME

        run_cmd('adb start-server')

    @property
    def wait_obj(self):
        """Used for waiting certain element appear"""
        return WebDriverWait(self.driver(), self.wait_time)

    def start_appium(self, port):
        # start appium server
        LOGGER.debug(f'Start appium server, port: {port}')
        server = AppiumService()
        server.start(
            args=["--address", "127.0.0.1", "-p", str(port), "--session-override"]
        )
        if server.is_running and server.is_listening:
            log_activity(
                self.user_avd.id,
                action_type="StartAppiumServer",
                msg=f"Started Appium server for {self.user_avd.name}",
                error=None,
            )
            return server
        else:
            log_activity(
                self.user_avd.id,
                action_type="StartAppiumServer",
                msg=f"Failed to start Appium server for {self.user_avd.name}",
                error=f"server status is not running and listening.",
            )
            return False

    def get_avd_options(self):
        emulator_options = [
            # Set the emulation mode for a camera facing back or front
            #  '-camera-back', 'emulated',
            #  '-camera-front', 'emulated',

            #  '-phone-number', str(self.phone) if self.phone else '0',

        ]

        if self.user_avd.timezone:
            emulator_options += ['-timezone', f"{self.user_avd.timezone}"]
        LOGGER.debug(f'Other options for emulator: {emulator_options}')
        return emulator_options

    def get_device(self):
        name = self.emulator_name

        #  LOGGER.debug(f'Start AVD: {name}')

        if not self.device:
            LOGGER.debug(f'Start AVD: ["emulator", "-avd", "{name}"] + '
                         f'{self.get_avd_options()}')
            self.device = subprocess.Popen(
                #  ["emulator", "-avd", f"{name}"],
                ["emulator", "-avd", f"{name}"] + self.get_avd_options(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            time.sleep(5)
            log_activity(
                self.user_avd.id,
                action_type="StartAvd",
                msg=f"Started AVD for {self.user_avd.name}",
                error=None,
            )

        if self.get_adb_device():
            self.get_device_retires = 0
            # self.get_adb_device().wait_boot_complete(timeout=100)
        else:
            self.device = False
            if self.get_device_retires >= 3:
                log_activity(
                    self.user_avd.id,
                    action_type="StartAvd",
                    msg=f"Failed to start AVD for {self.user_avd.name}",
                    error="Couldn't get device",
                )
                raise Exception("Couldn't get device.")

            self.get_device_retires += 1

            # kill all running devices/emulators
            print("killed in get_device")
            self.kill_bot_process(emulators=True)
            time.sleep(2)
            self.get_device()

        return self.device

    def check_apk_installation(self):
        LOGGER.debug('Check if Discord is installed')
        if not self.driver().is_app_installed("com.discord"):
            LOGGER.debug('Discord is not installed, now install it')
            self.install_apk(self.emulator_port, "discord")
            log_activity(
                self.user_avd.id,
                action_type="InstallDiscord",
                msg=f"Discord app installed successfully.",
                error=None,
            )
        
        LOGGER.debug('Check if cyberghost is installed')
        if not self.driver().is_app_installed("com.cyberghost.android"):
            self.install_apk(self.emulator_port, "cyberghost")
            log_activity(
                self.user_avd.id,
                action_type="CyberGhost",
                msg=f"SurfShrak app installed successfully.",
                error=None,
            )

    def get_adb_device(self):
        LOGGER.debug('Get adb device')
        for x in range(20):
            if self.adb.devices():
                try:
                    response = self.adb.devices()[0].shell("getprop sys.boot_completed | tr -d '\r'")
                    if "1" in response:
                        self.emulator_port = self.adb.devices()[0].serial.split("-")[-1]
                        return self.adb.devices()[0]
                except Exception as e:
                    print(e)
                    LOGGER.error(e)
            time.sleep(x)

    def start_driver(self):
        try:
            opts = {
                "platformName": "Android",
                "automationName": "uiautomator2",
                "noSign": True,
                "noVerify": True,
                "ignoreHiddenApiPolicyError": True,
            }

            LOGGER.debug('Start appium driver')
            LOGGER.debug(f'Driver capabilities: {opts}')

            self.app_driver = webdriver.Remote(
                "http://localhost:4724/wd/hub",
                desired_capabilities=opts,
                keep_alive=True,
            )
            self.start_driver_retires = 0
            log_activity(
                self.user_avd.id,
                action_type="ConnectAppium",
                msg=f"Driver started successfully",
                error=None,
            )
        except Exception as e:
            tb = traceback.format_exc()
            if self.start_driver_retires > 5:
                print("================ Couldn't start driverCouldn't start driver")
                log_activity(
                    self.user_avd.id,
                    action_type="ConnectAppium",
                    msg=f"Error while connecting with appium server",
                    error=tb,
                )
                raise Exception("Couldn't start driver")
            print("killed in start_driver")
            self.kill_bot_process(True, True)
            self.service = self.start_appium(port=4724)

            self.start_driver_retires += 1
            print(f"appium server starting retries: {self.start_driver_retires}")
            log_activity(
                self.user_avd.id,
                action_type="ConnectAppium",
                msg=f"Error while connecting with appium server",
                error=f"Failed to connect with appium server retries_value: {self.start_driver_retires}",
            )
            self.driver()

    def driver(self, check_verification=True):
        LOGGER.debug('Get driver')
        assert self.get_device(), "Device Didn't launch."

        try:
            session = self.app_driver.session
        except Exception as e:
            tb = traceback.format_exc()
            log_activity(
                self.user_avd.id,
                action_type="ConnectAppium",
                msg=f"Connect with Appium server",
                error=tb,
            )
            self.start_driver()

        # check and bypass google captcha
        #  random_sleep()
        popup = self.app_driver.find_elements_by_android_uiautomator(
            'new UiSelector().text("Wait")'
        )
        popup[0].click() if popup else None
        return self.app_driver

    @staticmethod
    def create_avd(avd_name, package=None, device=None):
        default_package = "system-images;android-28;default;x86"

        try:
            if not package:
                cmd = f'avdmanager create avd --name {avd_name} --package "{default_package}"'
            else:
                cmd = f'avdmanager create avd --name {avd_name} --package "{package}"'

            if device:
                #  cmd += f" --device {device}"
                cmd += f" --device \"{device}\""

            LOGGER.info(f'AVD command: {cmd}')
            p = subprocess.Popen(
                [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
            )
            time.sleep(1)
            p.communicate(input=b"\n")
            p.wait()
            return True

        except Exception as e:
            print(e)
            return False

    def install_apk(self, port, app_name):
        try:
            if app_name.lower() == "instagram":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/instagram.apk')}"
                log_activity(
                    self.user_avd.id,
                    action_type="InstallInstagramApk",
                    msg=f"Installation of instagram apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()

            elif app_name.lower() == "shadowsocks":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/shadowsocks.apk')}"
                log_activity(
                    self.user_avd.id,
                    action_type="InstallShadowsockApk",
                    msg=f"Installation of shadowsocks apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()

            elif app_name.lower() == "discord":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/discord.apk')}"
                LOGGER.debug(f'Install cmd: {cmd}')
                log_activity(
                    self.user_avd.id,
                    action_type="InstallDiscordApk",
                    msg=f"Installation of Discord apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()
            
            elif app_name.lower() == "cyberghost":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/cyberghost.apk')}"
                LOGGER.debug(f'Install cmd: {cmd}')
                log_activity(
                    self.user_avd.id,
                    action_type="InstallCyberGhostApk",
                    msg=f"Installation of CyberGhost apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()
            else:
                return False

            return True
        except Exception as e:
            print(e)
            return False

    def kill_process(self, port):
        try:
            cmd = f"lsof -t -i tcp:{port} | xargs kill -9"
            p = subprocess.Popen(
                [cmd],
                stdin=subprocess.PIPE,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log_activity(
                self.user_avd.id,
                action_type="KillProcess",
                msg=f"Kill process of given port: {port}",
                error=None,
            )
            return True
        except Exception as e:
            log_activity(
                self.user_avd.id,
                action_type="KillProcessError",
                msg=f"Failed to kill process of given port: {port}",
                error=traceback.format_exc(),
            )
            return False

    def start_appium(self, port):
        # start appium server
        LOGGER.debug(f'Start appium server, port: {port}')
        server = AppiumService()
        server.start(
            args=["--address", "127.0.0.1", "-p", str(port), "--session-override"]
        )
        if server.is_running and server.is_listening:
            log_activity(
                self.user_avd.id,
                action_type="StartAppiumServer",
                msg=f"Started Appium server for {self.user_avd.name}",
                error=None,
            )
            return server
        else:
            log_activity(
                self.user_avd.id,
                action_type="StartAppiumServer",
                msg=f"Failed to start Appium server for {self.user_avd.name}",
                error=f"server status is not running and listening.",
            )
            return False

    def kill_bot_process(self, appium=False, emulators=False):
        LOGGER.debug(f'Start to kill bot processes')
        LOGGER.debug(f'appium: {appium}, emulators: {emulators}')

        #  run_verbose = True
        run_verbose = False
        try:
            # Kill all running appium instances
            if appium:
                kill_cmd = "kill -9 $(pgrep -f appium)"
                run_cmd(kill_cmd, verbose=run_verbose)

                kill_cmd = "fuser -k -n tcp 4724"
                run_cmd(kill_cmd, verbose=run_verbose)

                log_activity(
                    self.user_avd.id,
                    action_type="KillAppiumServer",
                    msg=f"Killed appium server for {self.user_avd.name}",
                    error=None,
                )

            # Kill All emulators
            if emulators:
                self.device = None
                process_names = [
                    "qemu-system-x86_64",
                    "qemu-system-x86",
                    "emulator64-crash-service",
                    "adb",
                ]
                for process in process_names:
                    kill_cmd = f"pkill --signal TERM {process}"
                    run_cmd(kill_cmd, verbose=run_verbose)
                    pkill_process_after_waiting(process, success_code=1,
                                                verbose=run_verbose)

                # Logging process
                log_activity(
                    self.user_avd.id,
                    action_type="KillEmulator",
                    msg=f"Killed all available emulators for {self.user_avd.name}",
                    error=None,
                )

                # remove lock files to reinitiate device
                rm_cmd = f"rm {settings.AVD_DIR_PATH}/{self.emulator_name}.avd/*.lock"
                run_cmd(kill_cmd, verbose=run_verbose)


        except Exception as e:
            print("Error in killing bot instances", e)

    