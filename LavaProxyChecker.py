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
import requests
import argparse
from lib import LavaLib
from datetime import datetime


class LavaProxyChecker(object):

    def __init__(
            self,
            proxy_list,
            default_timeout=7,
            proxy_target="https://www.google.com/"
            ):
        self._proxy_list = proxy_list
        self._default_timeout = default_timeout
        self._target_url = proxy_target
        self._result = []

    def __do_test(self, proxy_target):
        logger.debug(
            "Now testing target at %s for proxy functionality."
            % (proxy_target,)
        )
        proxies = {
            'http': proxy_target,
            'https': proxy_target
        }
        try:
            requests.get(
                self._target_url,
                proxies=proxies,
                timeout=self._default_timeout
            )
        except requests.exceptions.Timeout:
            logger.error(
                "Request to %s through proxy %s failed due to timeout."
                % (self._target_url, proxy_target)
            )
            return False
        except requests.exceptions.ProxyError:
            logger.error(
                "Request to %s through proxy %s failed due to ProxyError/400."
                % (self._target_url, proxy_target)
            )
            return False
        return True

    def test_all(self):
        logger.info(
            "Now starting to test list of length %d for proxies."
            % (len(self._proxy_list))
        )
        for cur_proxy in self._proxy_list:
            if self.__do_test(cur_proxy):
                logger.info(
                    "Endpoint at %s appears to have proxy functionality!"
                )
                self._results.append(cur_proxy)
        logger.info(
            "Checking completed. A total of %d possible proxies were identified."
            % (len(self._results))
        )

    @property
    def results(self):
        return self._results


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="LavaProxyChecker - for finding those little cracks."
    )
    parser.add_argument(
        "--log-level",
        required=False,
        help="The log message level to receive when running the script. Valid "
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
        help="The path to a file containing proxy targets.",
        dest="input_path",
        action="store",
        type=str,
        metavar="/a/path/to/an/eyewitness/report/"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        help="The path where results of testing the "
             "input proxy list will be written.",
        dest="output_path",
        action="store",
        type=str,
        metavar="/a/path/to/store/the/output/to"
    )
    return parser.parse_args()


def print_greeting():
    print(LavaLib.LavaUIFactory.get_colorized_lavalamp_splash())
    print("                         /***************************\                             ")
    print("-= Presents the \033[31mLavaProxyChecker\033[0m, for finding all those little cracks =-")
    print("                         \***************************/                             ")
    print("")


def main():
    print_greeting()
    args = parse_arguments()
    LavaLib.configure_logging(logger, args.log_level)
    start_time = datetime.now()
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    with open(args.input_path, 'r') as f:
        proxy_targets = [x.strip() for x in f.read().strip().split("\n")]
    checker = LavaProxyChecker(proxy_targets)
    checker.test_all()
    if checker.results:
        logger.info(
            "Writing output to file at %s now."
            % (args.output_path)
        )
        with open(args.output_path, "w+") as f:
            f.write("\n".join(checker.results.keys()))
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


logger = logging.getLogger("LavaProxyChecker")

if __name__ == '__main__':
    main()
