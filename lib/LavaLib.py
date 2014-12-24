# -*- coding: utf-8 -*-
'''
@author: lavalamp

    Copyright 2014
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''
import logging


class LavaLogFormatter(logging.Formatter):

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    NONE = "\033[0m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[33m"

    CRITICAL = RED + "%(asctime)s [ C ] %(message)s" + NONE
    ERROR = "%(asctime)s [" + RED + " E " + NONE + "] %(message)s"
    WARNING = "%(asctime)s [" + YELLOW + " W " + NONE + "] %(message)s"
    INFO = "%(asctime)s [" + GREEN + " I " + NONE + "] %(message)s"
    DEBUG = "%(asctime)s [" + BLUE + " D " + NONE + "] %(message)s"

    def __init__(self):
        super(LavaLogFormatter, self).__init__(datefmt="[%m/%d %H:%M:%S]")
    # self.datefmt = "[%m/%d %H:%M:%S]"

    def format(self, record):
        if record.levelno == logging.CRITICAL:
            self._fmt = LavaLogFormatter.CRITICAL
        elif record.levelno == logging.ERROR:
            self._fmt = LavaLogFormatter.ERROR
        elif record.levelno == logging.WARNING:
            self._fmt = LavaLogFormatter.WARNING
        elif record.levelno == logging.INFO:
            self._fmt = LavaLogFormatter.INFO
        elif record.levelno == logging.DEBUG:
            self._fmt = LavaLogFormatter.DEBUG
        return super(LavaLogFormatter, self).format(record)


class LavaUIFactory(object):

    # Colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    # Effects
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    FAST_BLINK = 6

    # Escape codes
    ESCAPE_SEQUENCE = "\033[%sm"
    END_SEQUENCE = "\033[0m"

    # Lavalamp color map
    lavalamp_color_map = {
        "█": [
            CYAN,
            BOLD
        ],
        "▄": [
            CYAN
        ],
        "▀": [
            CYAN
        ],
        "▐": [
            CYAN
        ],
        "▒": [
            RED,
            BOLD
        ],
        "▓": [
            RED,
            BOLD
        ],
        "░": [
            RED
        ]
    }

    # Lavalamp splash
    lavalamp_splash = '''

     ██▓     ▄▄▄       ██▒   █▓ ▄▄▄       ██▓     ▄▄▄       ███▄ ▄███▓ ██▓███  
    ▓██▒    ▒████▄    ▓██░   █▒▒████▄    ▓██▒    ▒████▄    ▓██▒▀█▀ ██▒▓██░  ██▒
    ▒██░    ▒██  ▀█▄   ▓██  █▒░▒██  ▀█▄  ▒██░    ▒██  ▀█▄  ▓██    ▓██░▓██░ ██▓▒
    ▒██░    ░██▄▄▄▄██   ▒██ █░░░██▄▄▄▄██ ▒██░    ░██▄▄▄▄██ ▒██    ▒██ ▒██▄█▓▒ ▒
    ░██████▒ ▓█   ▓██▒   ▒▀█░   ▓█   ▓██▒░██████▒ ▓█   ▓██▒▒██▒   ░██▒▒██▒ ░  ░
    ░ ▒░▓  ░ ▒▒   ▓▒█░   ░ ▐░   ▒▒   ▓▒█░░ ▒░▓  ░ ▒▒   ▓▒█░░ ▒░   ░  ░▒▓▒░ ░  ░
    ░ ░ ▒  ░  ▒   ▒▒ ░   ░ ░░    ▒   ▒▒ ░░ ░ ▒  ░  ▒   ▒▒ ░░  ░      ░░▒ ░     
      ░ ░     ░   ▒        ░░    ░   ▒     ░ ░     ░   ▒   ░      ░   ░░       
        ░  ░      ░  ░      ░        ░  ░    ░  ░      ░  ░       ░            
                           ░                                                   

'''

    @classmethod
    def apply_text_effects(cls, input_text, input_effects):
        effects = ";".join([str(x) for x in input_effects])
        begin_sequence = cls.ESCAPE_SEQUENCE % effects
        return begin_sequence + input_text + cls.END_SEQUENCE

    @classmethod
    def get_colorized_lavalamp_splash(cls):
        to_return = cls.lavalamp_splash
        for cur_key in cls.lavalamp_color_map.keys():
            effect_char = cls.apply_text_effects(
                cur_key,
                cls.lavalamp_color_map[cur_key]
            )
            to_return = to_return.replace(cur_key, effect_char)
        return to_return


def configure_logging(logger, input_level="DEBUG"):
    if input_level == "INFO":
        lvl = logging.INFO
    elif input_level == "WARNING":
        lvl = logging.WARNING
    elif input_level == "ERROR":
        lvl = logging.ERROR
    elif input_level == "CRITICAL":
        lvl = logging.CRITICAL
    elif input_level == "DEBUG":
        lvl = logging.DEBUG
    logger.setLevel(lvl)
    formatter = LavaLogFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
