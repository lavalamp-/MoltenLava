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
import random
import logging
import tornado.httpclient
import tornado.ioloop
import argparse
import sys
from lib import LavaLib
from datetime import datetime


class LavaURLRandomizer(object):

    _name_index = 0
    _extension_index = 0

    def __init__(
            self,
            url,
            ):
        self._base_names = [
            "index",
            "images",
            "download",
            "2006",
            "news",
            "crack",
            "serial",
            "warez",
            "full",
            "12",
            "contact",
            "about",
            "search",
            "spacer",
            "privacy",
            "11",
            "logo",
            "blog",
            "new",
            "10",
            "cgi-bin",
            "faq",
            "rss",
            "home",
            "img",
            "default",
            "2005",
            "products",
            "sitemap",
            "archives",
            "1",
            "09",
            "links",
            "01",
            "08",
            "06",
            "2",
            "07",
            "login",
            "articles",
            "support",
            "05",
            "keygen",
            "article",
            "04",
            "03",
            "help",
            "events",
            "archive",
            "02",
            "register",
            "en",
            "forum",
            "software",
            "downloads",
            "3",
            "security",
            "13",
            "category",
            "4",
            "content",
            "14",
            "main",
            "15",
            "press",
            "media",
            "templates",
            "services",
            "icons",
            "resources",
            "info",
            "profile",
            "16",
            "2004",
            "18",
            "docs",
            "contactus",
            "files",
            "features",
            "html",
            "20",
            "21",
            "5",
            "22",
            "page",
            "6",
            "misc",
            "19",
            "partners",
            "24",
            "terms",
            "2007",
            "23",
            "17",
            "i",
            "27",
            "top",
            "26",
            "9",
            "legal",
            "30",
            "banners",
            "xml",
            "29",
            "28",
            "7",
            "tools",
            "projects",
            "25",
            "0",
            "user",
            "feed",
            "themes",
            "linux",
            "forums",
            "jobs",
            "business",
            "8",
            "video",
            "email",
            "books",
            "banner",
            "reviews",
            "view",
            "graphics",
            "research",
            "feedback",
            "pdf",
            "print",
            "ads",
            "modules",
            "2003",
            "company",
            "blank",
            "pub",
            "games",
            "copyright",
            "common",
            "site",
            "comments",
            "people",
            "aboutus",
            "product",
            "sports",
            "logos",
            "buttons",
            "english",
            "story",
            "image",
            "uploads",
            "31",
            "subscribe",
            "blogs",
            "atom",
            "gallery",
            "newsletter",
            "stats",
            "careers",
            "music",
            "pages",
            "publications",
            "technology",
            "calendar",
            "stories",
            "photos",
            "papers",
            "community",
            "data",
            "history",
            "arrow",
            "submit",
            "www",
            "s",
            "web",
            "library",
            "wiki",
            "header",
            "education",
            "go",
            "internet",
            "b",
            "in",
            "advertise",
            "spam",
            "a",
            "nav",
            "mail",
            "users",
            "Images",
            "members",
            "topics",
            "disclaimer",
            "store",
            "clear",
            "feeds",
            "c",
            "awards",
            "2002",
            "Default",
            "general",
            "pics",
            "dir",
            "signup",
            "solutions",
            "map",
            "News",
            "public",
            "doc",
            "de",
            "weblog",
            "index2",
            "shop",
            "contacts",
            "fr",
            "homepage",
            "travel",
            "button",
            "pixel",
            "list",
            "viewtopic",
            "documents",
            "overview",
            "tips",
            "adclick",
            "contact_us",
            "movies",
            "wp-content",
            "catalog",
            "us",
            "p",
            "staff",
            "hardware",
            "wireless",
            "global",
            "screenshots",
            "apps",
            "online",
            "version",
            "directory",
            "mobile",
            "other",
            "advertising",
            "tech",
            "welcome",
            "admin",
            "t",
            "policy",
            "faqs",
            "link",
            "2001",
            "training",
            "releases",
            "space",
            "member",
            "static",
            "join",
            "health",
            "weather",
            "reports",
            "scripts",
            "browse",
            "windows",
            "FireFox_Reco",
            "showallsites",
            "programs",
            "EWbutton_GuestBook",
            "EWbutton_Community",
            "menu",
            "EuropeMirror",
            "2000",
            "entertainment",
            "newsletters",
            "Home",
            "pr",
            "32",
            "categories",
            "detail",
            "assets",
            "strona_20",
            "strona_19",
            "strona_18",
            "strona_17",
            "strona_16",
            "strona_15",
            "strona_14",
            "strona_13",
            "strona_12",
            "strona_11",
            "strona_10",
            "strona_9",
            "strona_8",
            "strona_7",
            "strona_6",
            "strona_5",
            "strona_4",
            "strona_3",
            "strona_2",
            "strona_1",
            "36",
            "registration",
            "strona_21",
            "kontakt",
            "40",
            "glossary",
            "showthread",
            "mailman",
            "cnt",
            "order",
            "tutorials",
            "listinfo",
            "33",
            "r",
            "35",
            "whitepapers",
            "network",
            "privacy_policy",
            "audio",
            "footer",
            "politics",
            "d",
            "it",
            "37",
            "eng",
            "podcasts",
            "php",
            "post",
            "text",
            "chat",
            "39",
            "nl",
            "34",
            "science",
            "adview",
            "intro",
            "account",
            "x",
            "FAQ",
            "42",
            "comment",
            "privacypolicy",
            "node",
            "sponsors",
            "uk",
            "viewforum",
            "dot",
            "affiliates",
            "testimonials",
            "forms",
            "corporate",
            "donate",
            "41",
            "upload",
            "flash",
        ]
        self._base_extensions = [
            ".asp",
            ".aspx",
            "/",
            ".jsp",
            ".cfm",
            ".cfc",
            ".php",
            ".html",
            ".htm",
            ".bac",
            ".BAC",
            ".backup",
            ".BACKUP",
            ".bak",
            ".BAK",
            ".conf",
            ".cs",
            ".csproj",
            ".gz",
            ".inc",
            ".INC",
            ".ini",
            ".java",
            ".log",
            ".lst",
            ".old",
            ".OLD",
            ".orig",
            ".ORIG",
            ".sav",
            ".save",
            ".tar",
            ".temp",
            ".tmp",
            ".TMP",
            ".vb",
            ".vbproj",
            ".zip",
            ".$$$",
            ".-OLD",
            ".-old",
            ".0",
            ".1",
            ".~1",
            ".~bk",
        ]
        logger.debug(
            "LavaURLRandomizer instantiated with URL of %s."
            % (url,)
        )
        if not url.endswith("/"):
            url = url + "/"
            logger.warning(
                "URL did not end with a /. New URL is %s."
                % (url)
            )
        self._url = url
        random.shuffle(self._base_names)
        random.shuffle(self._base_extensions)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    @property
    def url(self):
        return self._url

    def next(self):
        if self._name_index == len(self._base_names):
            raise StopIteration()
        to_return = self._url + self._base_names[self._name_index] + self._base_extensions[self._extension_index]
        self._extension_index += 1
        if self._extension_index == len(self._base_extensions):
            self._extension_index = 0
            self._name_index += 1
        return to_return


class LavaURLsRandomizer(object):

    def __init__(
            self,
            urls
            ):
        logger.info(
            "LavaURLsRandomizer instantiated with total of %d URLs."
            % (len(urls))
        )
        self._urls = urls
        self._generators = []
        for cur_url in urls:
            self._generators.append(LavaURLRandomizer(cur_url))

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def burn_url(self, url):
        #TODO do this in a more pythonic way
        logger.warning(
            "Burning %s from list of URL generators."
            % (url,)
        )
        for cur_index in range(len(self._generators)):
            if self._generators[cur_index].url == url:
                del(self._generators[cur_index])
                break

    def next(self):
        while len(self._generators) > 0:
            index = random.randint(0, len(self._generators) - 1)
            try:
                to_return = self._generators[index].next()
                return to_return
            except StopIteration:
                logger.info(
                    "URL enumeration for target at %s exhausted!"
                    % (self._generators[index].url)
                )
                del(self._generators[index])
        if len(self._generators) == 0:
            logger.debug("LavaURLsRandomizer sequence exhausted.")
            raise StopIteration()


class LavaHTTPDiscoverer(object):

    def __init__(
            self,
            urls_randomizer,
            result_file,
            max_queue_size=1000,
            max_clients=50,
            maintenance_interval=30,
            ):
        # tornado.httpclient.AsyncHTTPClient.configure(
        #     "tornado.curl_httpclient.CurlAsyncHTTPClient"
        # )
        self._client = tornado.httpclient.AsyncHTTPClient(
            max_clients=max_clients
        )
        logger.debug(
            "LavaHTTPHandler instantiated with total of %d max clients."
            % (max_clients)
        )
        self._results = []
        self._num_outstanding = 0
        self._ready_for_stop = False
        self._write_queue = []
        self._last_report_time = None
        self._num_requests = 0
        self._num_200s = 0
        self._num_403s = 0
        self._num_500s = 0
        self._num_written = 0
        self._new_requests = 0
        self._max_queue_size = max_queue_size
        self._max_clients = max_clients
        self._urls_randomizer = urls_randomizer
        self._result_file = result_file
        self._maintenance_interval = maintenance_interval
        self.__prep_requests()
        self.__prep_output_file()
        self._io_loop = tornado.ioloop.IOLoop.instance()

    def __prep_output_file(self):
        with open(self._result_file, "w+") as f:
            f.write("#,CODE,URL\n")

    def __send_next(self):
        try:
            url = self._urls_randomizer.next()
            self.__send_request(url)
        except StopIteration:
            self._ready_for_stop = True

    def __handle_success(self, r_dict):
        logger.info(
            "URL at %s returned a %d!"
            % (r_dict['url'], r_dict['code'])
        )
        if r_dict['code'] == 200:
            self._num_200s += 1
        if r_dict['code'] == 403:
            self._num_403s += 1
        if r_dict['code'] == 500:
            self._num_500s += 1
        self._write_queue.append(r_dict)

    def __write_out_queue(self):
        logger.debug(
            "Now writing a total of %d results to file at %s."
            % (len(self._write_queue), self._result_file)
        )
        with open(self._result_file, "a") as f:
            for cur_dict in self._write_queue:
                self._num_written += 1
                f.write(str(self._num_written) + "," + str(cur_dict['code']) + "," + cur_dict['url'] + "\n")
        self._write_queue = []

    def __do_maintenance(self):
        now = datetime.now()
        if (now - self._last_report_time).seconds > self._maintenance_interval:
            logger.info(
                "Total requests sent: %d. Requests per second: %d. "
                "Total 200s: %d. Total 403s: %d. Total 500s: %d."
                %
                (
                    self._num_requests,
                    self._new_requests / self._maintenance_interval,
                    self._num_200s,
                    self._num_403s,
                    self._num_500s
                )
            )
            self.__write_out_queue()
            self._last_report_time = now
            self._new_requests = 0

    def __on_response(self, response):
        self._num_outstanding -= 1
        r_dict = self.__response_to_dict(response)
        if r_dict['code'] == 599:
            logger.debug(
                "Request for URL at %s returned 599."
                % (r_dict['url'],)
            )
            #TODO find out how to better handle 599s
            # might want to test the endpoints before firing off the Tornado ioloop
        elif r_dict['code'] != 404:
            self.__handle_success(r_dict)
        else:
            logger.debug(
                "URL at %s returned a 404."
                % (r_dict['url'])
            )
        self.__do_maintenance()
        if not self._ready_for_stop:
            self.__send_next()
        elif self._num_outstanding == 0:
            tornado.ioloop.IOLoop.instance().stop()

    def __prep_requests(self):
        for x in range(self._max_queue_size):
            if not self._ready_for_stop:
                self.__send_next()

    def __response_to_dict(self, response):
        return {
            'code': response.code,
            'url': response.request.url,
            'response_time': response.request_time
        }

    def __send_request(self, url):
        self._num_outstanding += 1
        self._num_requests += 1
        self._new_requests += 1
        self._client.fetch(
            url,
            callback=self.__on_response,
            validate_cert=False,
            method="HEAD"
        )

    def run(self):
        self._last_report_time = datetime.now()
        self._io_loop.start()


def main():
    print_greeting()
    args = parse_arguments()
    LavaLib.configure_logging(logger, args.log_level)
    LavaLib.configure_logging(logging.getLogger('tornado'), args.log_level)
    start_time = datetime.now()
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    with open(args.input_path, "r") as f:
        c_split = [x.strip() for x in f.read().strip().split("\n")]
    logger.info(
        "Total of %d endpoints read from file at %s."
        % (len(c_split), args.input_path)
    )
    randomizer = LavaURLsRandomizer(c_split)
    x = LavaHTTPDiscoverer(
        randomizer,
        args.output_path
    )
    x.run()
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="LavaContentDiscovery - for finding those hidden suckers"
    )
    parser.add_argument(
        "--log-level",
        required=False,
        help="The log message level to receive when running the script. Valid"
             "values are DEBUG, INFO, WARNING, ERROR, CRITICAL.",
        action="store",
        dest="log_level",
        metavar="<DEBUG|INFO|WARNING|ERROR|CRITICAL>",
        default="INFO",
        type=str
    )
    parser.add_argument(
        "--input-path",
        "-i",
        required=True,
        help="The path to a file containing a list of "
             "URL endpoints to test against.",
        dest="input_path",
        action="store",
        type=str,
        metavar="/a/path/to/an/endpoint/file"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        help="The path where results of content discovery will be written.",
        dest="output_path",
        action="store",
        type=str,
        metavar="/a/path/to/store/the/output/to"
    )
    return parser.parse_args()


def print_greeting():
    print(LavaLib.LavaUIFactory.get_colorized_lavalamp_splash())
    print("                         /***************************\                             ")
    print("-= Presents the \033[31mLavaContentDiscovery\033[0m, for finding those hidden suckers =-")
    print("                         \***************************/                             ")
    print("")

logger = logging.getLogger("LavaContentDiscovery")
start_time = None

if __name__ == "__main__":
    main()
