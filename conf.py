# Configuration file
import logging
from pathlib import Path

# Project
PRJ_PATH = Path(__file__).parent

# Log
LOG_DIR = 'logs'
LOG_DIR_PATH = PRJ_PATH / 'logs'
LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist
LOG_LEVEL = logging.DEBUG
LOG_IN_ONE_FILE = True

# AVD
AVD_DEVICES = ["Nexus 10", "Nexus 4", "Nexus 5", "Nexus 5X", "Nexus 6",
               "Nexus 6P", "Nexus 7 2013", "Nexus 7", "Nexus 9",
               "pixel", "pixel_2", "pixel_2_xl", "pixel_3", "pixel_3_xl",
               "pixel_3a", "pixel_3a_xl", "pixel_4", "pixel_4_xl", "pixel_4a",
               "pixel_5", "pixel_xl", "pixel_c",
               ]
AVD_PACKAGES = ["system-images;android-28;default;x86",
                "system-images;android-28;default;x86_64",
                "system-images;android-29;default;x86",
                # "system-images;android-29;default;x86_64",
                # "system-images;android-30;default;x86_64",

                # cause some errors of twitter: (errors: timestamp out of bounds, code:135)
                #  "system-images;android-31;default;x86_64",
                ]

US_TIMEZONE = ['US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central',
               'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke',
               'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Samoa']

# time
WAIT_TIME = 30

# deathbycaptcha.com account
DBC_USERNAME = 'noborderz'
DBC_PASSWORD = '/+eQm@>;Q:Td8?MA'

# captcha
RECAPTCHA_ALL_RETRY_TIMES = 15  # the number of captcha images to resolve in all
FUNCAPTCHA_ALL_RETRY_TIMES = 20  # the number of captcha images to resolve in all
CAPTCHA_IMAGE_DIR_NAME = 'temp'
CAPTCHA_IMAGE_DIR = PRJ_PATH / CAPTCHA_IMAGE_DIR_NAME
CAPTCHA_IMAGE_DIR.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist


PACKAGES_DIR_NAME = 'apk'
PACKAGES_DIR = PRJ_PATH / PACKAGES_DIR_NAME
PACKAGES_DIR.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist
# cyberghostvpn
CYBERGHOSTVPN_APK = PACKAGES_DIR / 'cyberghostvpn_8.6.4.396.apk'
CYBERGHOSTVPN_SERVERS = {
    'Albania': [],
    'Algeria': [],
    'Andorra': [],
    'Argentina': [],
    'Armenia': [],
    'Australia': ['Melbourne', 'Sydney'],
    'Austria': [],
    'Bahamas': [],
    'Bangladesh': [],
    'Belarus': [],
    'Belgium': [],
    'Bosnia & Herzegovina': [],
    'Brazil': [],
    'Bulgaria': [],
    'Cambodia': [],
    'Canada': ['Montreal', 'Toronto', 'Vancouver'],
    'Chile': [],
    'China': [],
    'Colombia': [],
    'Costa Rica': [],
    'Croatia': [],
    'Cyprus': [],
    'Czechia': [],
    'Denmark': [],
    'Egypt': [],
    'Estonia': [],
    'Finland': [],
    'France': ['Paris', 'Strasbourg'],
    'Georgia': [],
    'Germany': ['Berlin', 'Dusseldorf', 'Frankfurt'],
    'Greece': [],
    'Greenland': [],
    'Hong Kong': [],
    'Hungary': [],
    'Iceland': [],
    'India': [],
    'Indonesia': [],
    'Iran': [],
    'Ireland': [],
    'Isle of Man': [],
    'Israel': [],
    'Italy': ['Milano', 'Rome'],
    'Japan': [],
    'Kazakhstan': [],
    'Kenya': [],
    'Latvia': [],
    'Liechtenstein': [],
    'Lithuania': [],
    'Luxembourg': [],
    'Macau': [],
    'Macedonia (FYROM)': [],
    'Malaysia': [],
    'Malta': [],
    'Mexico': [],
    'Moldova': [],
    'Monaco': [],
    'Mongolia': [],
    'Montenegro': [],
    'Morocco': [],
    'Netherlands': [],
    'New Zealand': [],
    'Nigeria': [],
    'Norway': [],
    'Pakistan': [],
    'Panama': [],
    'Philippines': [],
    'Poland': [],
    'Portugal': [],
    'Qatar': [],
    'Romania': ['Bucharest', 'NoSpy Bucharest'],
    'Russia': [],
    'Saudi Arabia': [],
    'Serbia': [],
    'Singapore': [],
    'Slovakia': [],
    'Slovenia': [],
    'South Africa': [],
    'South Korea': [],
    'Spain': ['Barcelona', 'Madrid'],
    'Sri Lanka': [],
    'Sweden': [],
    'Switzerland': ['Huenenberg', 'Zurich'],
    'Taiwan': [],
    'Thailand': [],
    'Turkey': [],
    'Ukraine': [],
    'United Arab Emirates': [],
    'United Kingdom': ['Berkshire', 'London', 'Manchester'],
    'United States': [
        'Atlanta',
        'Chicago',
        'Dallas',
        'Las Vegas',
        'Los Angeles',
        'Miami',
        'New York',
        'Los Angeles',
        'Miami',
        'New York',
        'Phoenix',
        'San Francisco',
        'Seattle',
        'Washington'
    ],
    'Venezuela': [],
    'Vietnam': []
}
